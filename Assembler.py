class Register:
    REGISTER_MAP = {
        '$0': 0, '$at': 1, '$v0': 2, '$v1': 3, '$a0': 4, '$a1': 5, '$a2': 6, '$a3': 7,
        '$t0': 8, '$t1': 9, '$t2': 10, '$t3': 11, '$t4': 12, '$t5': 13, '$t6': 14, '$t7': 15,
        '$s0': 16, '$s1': 17, '$s2': 18, '$s3': 19, '$s4': 20, '$s5': 21, '$s6': 22, '$s7': 23,
        '$t8': 24, '$t9': 25, '$k0': 26, '$k1': 27, '$gp': 28, '$sp': 29, '$fp': 30, '$ra': 31
    }

    @staticmethod
    def get_register_code(register):
        return Register.REGISTER_MAP.get(register, None)


class Instruction:
    INSTRUCTION_EXPANSIONS = {
        'ble': 2,  # ble expands to slt + beq
        'la': 2    # la expands to lui + ori
    }

    @staticmethod
    def get_expansion(instruction):
        return Instruction.INSTRUCTION_EXPANSIONS.get(instruction, 1)


class Encoder:
    @staticmethod
    def r_format(opcode, rs, rt, rd, shamt, funct):
        return f"{opcode:06b}{rs:05b}{rt:05b}{rd:05b}{shamt:05b}{funct:06b}"

    @staticmethod
    def i_format(opcode, rs, rt, imm):
        imm = imm & 0xFFFF  # Ensure immediate is 16 bits
        return f"{opcode:06b}{rs:05b}{rt:05b}{imm:016b}"

    @staticmethod
    def j_format(opcode, address):
        return f"{opcode:06b}{address:026b}"


class Assembler:
    def __init__(self, source_file):
        self.source_file = source_file
        self.data_labels = {}
        self.text_labels = {}
        self.instructions = []
        self.data_address = 0x10010000  # Starting address for data segment
        self.text_address = 0x00400000  # Starting address for text segment

    def parse_file(self):
        in_data_section = False
        in_text_section = False

        with open(self.source_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.split('#')[0].strip()  # Remove comments
                if not line:
                    continue  # Skip empty lines

                if line == '.data':
                    in_data_section = True
                    in_text_section = False
                    continue
                elif line == '.text':
                    in_data_section = False
                    in_text_section = True
                    continue

                if in_data_section and ':' in line:
                    # Handle data labels
                    label, value = line.split(':', 1)
                    label = label.strip()
                    self.data_labels[label] = self.data_address
                    self.data_address += 4  # Assume each data item is 4 bytes
                elif in_text_section:
                    if ':' in line:
                        # Handle text labels
                        label, instruction = line.split(':', 1)
                        label = label.strip()
                        self.text_labels[label] = self.text_address
                        if instruction.strip():
                            # Handle instructions after labels
                            instr = instruction.strip().split()[0]
                            expansion = Instruction.get_expansion(instr)
                            self.instructions.append((self.text_address, instruction.strip()))
                            self.text_address += 4 * expansion
                    else:
                        # Handle standalone instructions
                        instr = line.split()[0]
                        expansion = Instruction.get_expansion(instr)
                        self.instructions.append((self.text_address, line))
                        self.text_address += 4 * expansion

    def encode_instructions(self):
        machine_code = []
        current_address = 0x00400000

        for addr, line in self.instructions:
            parts = line.replace(',', ' ').split()
            instruction = parts[0]

            if instruction == 'li':
                # Load immediate
                register = parts[1]
                immediate = int(parts[2])
                binary = Encoder.i_format(0x09, 0, Register.get_register_code(register), immediate)
            elif instruction == 'ble':
                # Branch if less than or equal (pseudo-instruction)
                rs = parts[1]
                rt = parts[2]
                label = parts[3]
                target_address = self.text_labels[label]
                # slt $at, rs, rt
                binary_slt = Encoder.r_format(0, Register.get_register_code(rs), Register.get_register_code(rt), 1, 0, 0x2A)
                machine_code.append((current_address, binary_slt))
                current_address += 4
                # beq $at, $0, label
                offset = (target_address - (current_address + 4)) // 4
                binary_beq = Encoder.i_format(0x04, 1, 0, offset)
                binary = binary_beq
            elif instruction == 'la':
                # Load address (pseudo-instruction)
                register = parts[1]
                label = parts[2]
                label_address = self.data_labels[label]
                # lui $at, upper(label_address)
                hi = (label_address >> 16) & 0xFFFF
                binary_lui = Encoder.i_format(0x0F, 0, 1, hi)
                machine_code.append((current_address, binary_lui))
                current_address += 4
                # ori $reg, $at, lower(label_address)
                lo = label_address & 0xFFFF
                binary_ori = Encoder.i_format(0x0D, 1, Register.get_register_code(register), lo)
                binary = binary_ori
            elif instruction == 'jal':
                # Jump and link
                label = parts[1]
                target_address = self.text_labels[label]
                address = (target_address >> 2) & 0x3FFFFFF
                binary = Encoder.j_format(0x03, address)
            elif instruction == 'j':
                # Jump
                label = parts[1]
                target_address = self.text_labels[label]
                address = (target_address >> 2) & 0x3FFFFFF
                binary = Encoder.j_format(0x02, address)
            elif instruction == 'addi':
                # Add immediate
                rt = parts[1]
                rs = parts[2]
                immediate = int(parts[3])
                binary = Encoder.i_format(0x08, Register.get_register_code(rs), Register.get_register_code(rt), immediate)
            elif instruction == 'or':
                # Bitwise OR
                rd = parts[1]
                rs = parts[2]
                rt = parts[3]
                binary = Encoder.r_format(0, Register.get_register_code(rs), Register.get_register_code(rt), Register.get_register_code(rd), 0, 0x25)
            elif instruction == 'andi':
                # Bitwise AND immediate
                rt = parts[1]
                rs = parts[2]
                immediate = int(parts[3])
                binary = Encoder.i_format(0x0C, Register.get_register_code(rs), Register.get_register_code(rt), immediate)
            elif instruction == 'bne':
                # Branch if not equal
                rs = parts[1]
                rt = parts[2]
                label = parts[3]
                target_address = self.text_labels[label]
                offset = (target_address - (current_address + 4)) // 4
                binary = Encoder.i_format(0x05, Register.get_register_code(rs), Register.get_register_code(rt), offset)
            elif instruction == 'srl':
                # Shift right logical
                rd = parts[1]
                rt = parts[2]
                shamt = int(parts[3])
                binary = Encoder.r_format(0, 0, Register.get_register_code(rt), Register.get_register_code(rd), shamt, 0x02)
            elif instruction == 'beq':
                # Branch if equal
                rs = parts[1]
                rt = parts[2]
                label = parts[3]
                target_address = self.text_labels[label]
                offset = (target_address - (current_address + 4)) // 4
                binary = Encoder.i_format(0x04, Register.get_register_code(rs), Register.get_register_code(rt), offset)
            elif instruction == 'sub':
                # Subtract
                rd = parts[1]
                rs = parts[2]
                rt = parts[3]
                binary = Encoder.r_format(0, Register.get_register_code(rs), Register.get_register_code(rt), Register.get_register_code(rd), 0, 0x22)
            elif instruction == 'sllv':
                # Shift left logical variable
                rd = parts[1]
                rt = parts[2]
                rs = parts[3]
                binary = Encoder.r_format(0, Register.get_register_code(rs), Register.get_register_code(rt), Register.get_register_code(rd), 0, 0x04)
            elif instruction == 'syscall':
                # System call
                binary = '00000000000000000000000000001100'
            elif instruction == 'jr':
                # Jump register
                rs = parts[1]
                binary = Encoder.r_format(0, Register.get_register_code(rs), 0, 0, 0, 0x08)
            elif instruction == 'add':
                # Add
                rd = parts[1]
                rs = parts[2]
                rt = parts[3]
                binary = Encoder.r_format(0, Register.get_register_code(rs), Register.get_register_code(rt), Register.get_register_code(rd), 0, 0x20)
            elif instruction == 'sll':
                # Shift left logical
                rd = parts[1]
                rt = parts[2]
                shamt = int(parts[3])
                binary = Encoder.r_format(0, 0, Register.get_register_code(rt), Register.get_register_code(rd), shamt, 0x00)
            elif instruction == 'lw':
                # Load word
                rt = parts[1]
                offset_rs = parts[2]
                offset_str, rs_str = offset_rs.split('(')
                offset = int(offset_str)
                rs = Register.get_register_code(rs_str[:-1])
                binary = Encoder.i_format(0x23, rs, Register.get_register_code(rt), offset)
            elif instruction == 'sw':
                # Store word
                rt = parts[1]
                offset_rs = parts[2]
                offset_str, rs_str = offset_rs.split('(')
                offset = int(offset_str)
                rs = Register.get_register_code(rs_str[:-1])
                binary = Encoder.i_format(0x2B, rs, Register.get_register_code(rt), offset)
            elif instruction == 'slt':
                # Set less than
                rd = parts[1]
                rs = parts[2]
                rt = parts[3]
                binary = Encoder.r_format(0, Register.get_register_code(rs), Register.get_register_code(rt), Register.get_register_code(rd), 0, 0x2A)
            else:
                print(f"Unknown instruction: {instruction}")
                exit(1)

            machine_code.append((current_address, binary))
            current_address += 4

        return machine_code


def main():
    source_file = input("Enter the name of the file: ")
    if not source_file.endswith('.asm'):
        source_file += '.asm'

    # Create an assembler instance
    assembler = Assembler(source_file)

    # Parse the file
    assembler.parse_file()

    # Encode instructions into machine code
    machine_code = assembler.encode_instructions()

    # Write machine code to output file
    with open('MachineCode.txt', 'w') as output_file:
        for _, binary in machine_code:
            output_file.write(binary + '\n')

    print("Assembly successful!")


if __name__ == '__main__':
    main()