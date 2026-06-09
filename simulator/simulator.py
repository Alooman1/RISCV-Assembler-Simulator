import sys

registers = {
    "00000": 0,        
    "00001": 0,        
    "00010": 0x0000017C,  
    "00011": 0,        
    "00100": 0,       
    "00101": 0,        
    "00110": 0,       
    "00111": 0,      
    "01000": 0,       
    "01001": 0,   
    "01010": 0,      
    "01011": 0,      
    "01100": 0,      
    "01101": 0,        
    "01110": 0,        
    "01111": 0,       
    "10000": 0,       
    "10001": 0,      
    "10010": 0,        
    "10011": 0,       
    "10100": 0,       
    "10101": 0,        
    "10110": 0,    
    "10111": 0,        
    "11000": 0,      
    "11001": 0,       
    "11010": 0,      
    "11011": 0,     
    "11100": 0,        
    "11101": 0,        
    "11110": 0,       
    "11111": 0         
}

datamem = {0x00010000 + 4 * i: 0 for i in range(32)} 

R_type = ["0110011"]
I_type = ["0000011", "0010011", "1100111"]
S_type = ["0100011"]
B_type = ["1100011"]
J_type = ["1101111"]

def sext(binary, num_bits):
    value = int(binary, 2)
    if binary[0] == '1':
        value -= (1 << len(binary))
    return format(value & ((1 << num_bits) - 1), f'0{num_bits}b')

def dec_to_twocomp(decimal_num, num_bits):
    if decimal_num < 0:
        decimal_num += (1 << num_bits)
    return format(decimal_num, f'0{num_bits}b')

def twocomp_to_dec(binary):
    num_bits = len(binary)
    value = int(binary, 2)
    if binary[0] == '1':
        value -= (1 << num_bits)
    return value

def unsigned(val):
    return val & 0xffffffff

def add(instruction):
    rs1 = instruction[12:17]
    rs2 = instruction[7:12]
    rd = instruction[20:25]
    if rd != "00000":
        registers[rd] = registers[rs1] + registers[rs2]

def sub(instruction):
    rs1 = instruction[12:17]
    rs2 = instruction[7:12]
    rd = instruction[20:25]
    if rd != "00000":
        registers[rd] = registers[rs1] - registers[rs2]

def slt(instruction):
    rs1 = instruction[12:17]
    rs2 = instruction[7:12]
    rd = instruction[20:25]
    if rd != "00000":
        registers[rd] = 1 if registers[rs1] < registers[rs2] else 0

def and_(instruction):
    rs1 = instruction[12:17]
    rs2 = instruction[7:12]
    rd = instruction[20:25]
    if rd != "00000":
        registers[rd] = registers[rs1] & registers[rs2]

def or_(instruction):
    rs1 = instruction[12:17]
    rs2 = instruction[7:12]
    rd = instruction[20:25]
    if rd != "00000":
        registers[rd] = registers[rs1] | registers[rs2]

def srl(instruction):
    rs1 = instruction[12:17]
    rs2 = instruction[7:12]
    rd = instruction[20:25]
    if rd != "00000":
        shift_amount = registers[rs2] & 0b11111
        registers[rd] = (registers[rs1] & 0xFFFFFFFF) >> shift_amount

def lw(instruction):
    rs1 = instruction[12:17]
    rd = instruction[20:25]
    imm = instruction[0:12]
    imm_value = twocomp_to_dec(imm)
    addr = registers[rs1] + imm_value
    if rd != "00000":
        if addr % 4 == 0:
            registers[rd] = datamem.get(addr, 0) 
        else:
            registers[rd] = 0

def sw(instruction):
    rs2 = instruction[7:12]
    rs1 = instruction[12:17]
    imm_high = instruction[0:7]
    imm_low = instruction[20:25]
    imm = imm_high + imm_low
    addr = registers[rs1] + twocomp_to_dec(imm)
    if addr % 4 == 0:
        datamem[addr] = registers[rs2]

def addi(instruction):
    rs1 = instruction[12:17]
    rd = instruction[20:25]
    imm = instruction[0:12]
    if rd != "00000":
        registers[rd] = registers[rs1] + twocomp_to_dec(imm)

def beq(instruction, program_counter):
    rs1 = instruction[12:17]
    rs2 = instruction[7:12]
    imm = instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24] + '0'
    byte_offset = twocomp_to_dec(imm)
    instr_offset = byte_offset // 4
    return program_counter + instr_offset if registers[rs1] == registers[rs2] else program_counter + 1

def bne(instruction, program_counter):
    rs1 = instruction[12:17]
    rs2 = instruction[7:12]
    imm = instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24] + '0'
    byte_offset = twocomp_to_dec(imm)
    instr_offset = byte_offset // 4
    return program_counter + instr_offset if registers[rs1] != registers[rs2] else program_counter + 1

def jal(instruction, program_counter):
    rd = instruction[20:25]
    imm = instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11] + '0'
    byte_offset = twocomp_to_dec(imm)
    instr_offset = byte_offset // 4
    if rd != "00000":
        registers[rd] = (program_counter + 1) * 4
    return program_counter + instr_offset

program_counter = 0
instr_dict = {}
input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, "r") as f:
    lines = f.readlines()
    for i in range(len(lines)):
        instr_dict[i] = lines[i].strip()

virtual_halt = "00000000000000000000000001100011"

with open(output_file, "w") as file:
    while program_counter in instr_dict and instr_dict[program_counter] != virtual_halt:
        instruction = instr_dict[program_counter]
        opcode = instruction[25:32]

        if opcode in R_type:
            funct7 = instruction[0:7]
            funct3 = instruction[17:20]
            if funct7 == "0100000" and funct3 == "000":
                sub(instruction)
            else:
                if funct3 == "000":
                    add(instruction)
                elif funct3 == "010":
                    slt(instruction)
                elif funct3 == "101":
                    srl(instruction)
                elif funct3 == "110":
                    or_(instruction)
                elif funct3 == "111":
                    and_(instruction)
            program_counter += 1

        elif opcode in I_type:
            if opcode == "0000011":
                lw(instruction)
                program_counter += 1
            elif opcode == "0010011":
                addi(instruction)
                program_counter += 1
            elif opcode == "1100111":
                rs1 = instruction[12:17]
                rd = instruction[20:25]
                imm = instruction[0:12]
                imm_val = twocomp_to_dec(imm)
                target = (registers[rs1] + imm_val) & ~1
                if rd != "00000":
                    registers[rd] = (program_counter + 1) * 4
                program_counter = target // 4
            else:
                program_counter += 1

        elif opcode in S_type:
            sw(instruction)
            program_counter += 1

        elif opcode in B_type:
            funct3 = instruction[17:20]
            if funct3 == "000":
                program_counter = beq(instruction, program_counter)
            elif funct3 == "001":
                program_counter = bne(instruction, program_counter)

        elif opcode in J_type:
            program_counter = jal(instruction, program_counter)

        else:
            program_counter += 1

        current_pc = program_counter * 4
        file.write(f"0b{current_pc:032b} ")
        for reg in sorted(registers.keys()):
            file.write(f"0b{registers[reg] & 0xFFFFFFFF:032b} ")
        file.write("\n")

    
    if program_counter in instr_dict and instr_dict[program_counter] == virtual_halt:
        current_pc = program_counter * 4
        file.write(f"0b{current_pc:032b} ")
        for reg in sorted(registers.keys()):
            file.write(f"0b{registers[reg] & 0xFFFFFFFF:032b} ")
        file.write("\n")
with open(output_file, "a") as f:
    for addr in sorted(datamem.keys()): 
        f.write(f"0x{addr:08X}:0b{datamem[addr] & 0xFFFFFFFF:032b}\n")