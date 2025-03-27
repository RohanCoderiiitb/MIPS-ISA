# MIPS Assembler and Example Programs  

## Overview  
This mini-project includes a Python-based MIPS assembler (`Assembler.py`) and two example MIPS assembly programs:  
- `BinarySearch.asm`: Implements a binary search algorithm in MIPS assembly.  
- `GCD.asm`: Computes the Greatest Common Divisor (GCD) using the Euclidean algorithm.  

The assembler reads a MIPS assembly file, converts it to machine code, and saves the output as `MachineCode.txt`.  

## Files  
1. **Assembler.py** - A Python script that assembles MIPS code into machine code.  
2. **BinarySearch.asm** - A MIPS assembly program for binary search.  
3. **GCD.asm** - A MIPS assembly program for computing the GCD of two numbers.  

## How to Use  

### Running the Assembler  
To assemble a MIPS program, run the Python script and enter the name of the `.asm` file (without the extension):  
```bash  
python Assembler.py  
```
The script will:  
1. Prompt you to enter the name of the assembly file (e.g., `BinarySearch`).  
2. Automatically append `.asm` to the filename.  
3. Convert the MIPS assembly code into machine code.  
4. Save the output as `MachineCode.txt`, overwriting any previous output.  

### Example  
If you enter `GCD` when prompted, the script will process `GCD.asm` and create a `MachineCode.txt` file with the corresponding machine code.  

### Requirements  
- Python 3.x  
- A MIPS simulator (e.g., [QtSPIM](https://sourceforge.net/projects/spimsimulator/) or [Mars](http://courses.missouristate.edu/KenVollmar/MARS/)) to run the assembly programs  

## About `Assembler.py`  

`Assembler.py` is a Python script that acts as a simple MIPS assembler. It processes MIPS assembly code and converts it into machine-readable binary format. The script follows these steps:  

1. **File Handling**  
   - Takes user input for the `.asm` filename.  
   - Reads the assembly file line by line.  

2. **Instruction Parsing**  
   - Splits each line into operation (opcode) and operands.  
   - Identifies instruction type (R-type, I-type, J-type).  
   - Maps registers and immediate values to their respective binary representations.  

3. **Instruction Encoding**  
   - Converts parsed instructions into 32-bit binary format.  
   - Expands pseudo-instructions into actual MIPS instructions (e.g., `ble` into `slt` and `bne`).  

4. **Handling Labels**  
   - Extracts labels and maps them to instruction addresses.  
   - Replaces label references with correct jump/branch addresses.  

5. **Saving Output**  
   - Writes the converted machine code into `MachineCode.txt`.  
   - Overwrites any previous output in `MachineCode.txt`.  

## Example Programs  

### Binary Search (BinarySearch.asm)  
A MIPS assembly program that searches for a target element in a sorted array using binary search.  

### GCD Computation (GCD.asm)  
A MIPS assembly program that computes the Greatest Common Divisor (GCD) using the Euclidean algorithm.  

## Future Improvements  
- Extend assembler to support more MIPS instructions.  
- Improve error handling and debugging features.  
