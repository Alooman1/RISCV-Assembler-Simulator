# RISC-V Assembler and Instruction Set Simulator

## Overview

This project implements a custom RISC-V Assembler and Instruction Set Simulator in Python. The assembler translates RISC-V assembly programs into machine code, while the simulator executes the generated instructions and tracks register and memory states throughout execution.

## Features

### Assembler
- Two-pass assembly process with label resolution
- Translation of RISC-V assembly instructions into 32-bit machine code
- Register validation and instruction format checking
- Immediate value handling with two's complement representation
- Support for branch and jump labels
- Virtual halt instruction validation

### Simulator
- 32-register RISC-V architecture simulation
- Program Counter (PC) management
- Arithmetic and logical instruction execution
- Memory load/store operations
- Branch and jump instruction handling
- Register state tracing after every instruction
- Memory state dump generation

## Supported Instruction Types

### R-Type
- add
- sub
- slt
- srl
- and
- or

### I-Type
- addi
- lw
- jalr

### S-Type
- sw

### B-Type
- beq
- bne
- blt

### J-Type
- jal

## Project Structure

```
RISCV-Assembler-Simulator/
│
├── assembler/
│   └── assembler.py
│
├── simulator/
│   └── simulator.py
│
└── README.md
```

## Technologies Used

- Python
- RISC-V ISA
- Computer Architecture
- Assembly Language Programming

## Key Highlights

- Implemented support for 5 instruction formats (R, I, S, B, J)
- Simulated a complete 32-register RISC-V processor model
- Built instruction encoding, decoding, and execution pipelines
- Developed memory management and execution tracing functionality
- Enabled end-to-end assembly and execution of RISC-V programs

## Future Improvements

- Support for additional RISC-V instructions
- Pipeline simulation
- Hazard detection
- Cache memory simulation
- GUI-based visualization of execution flow

## Author

Dev Sharma