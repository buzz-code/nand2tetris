
from parser import Parser, InstructionType
from code import Code
from symbol_table import SymbolTable

class Assembler:
    def __init__(self):
        self.parser = Parser()
        self.code = Code()
        self.symbol_table = SymbolTable()

    def process_assembly_line(self, line):
        """Process a single line of assembly code."""
        line = line.strip()
        instr_type = self.parser.instruction_type(line)
        
        if instr_type == InstructionType.A_INSTRUCTION:
            value = self.parser.parse_a_instruction(line)
            return f'0{self.code.number_or_symbol_to_binary(value, self.symbol_table)}'
        elif instr_type == InstructionType.C_INSTRUCTION:
            dest, comp, jump = self.parser.parse_c_instruction(line)
            comp_bits = self.code.comp_to_binary(comp)
            dest_bits = self.code.dest_to_binary(dest)
            jump_bits = self.code.jump_to_binary(jump)
            return f'111{comp_bits}{dest_bits}{jump_bits}'
        return None

    def first_pass(self, input_file):
        with open(input_file, 'r') as asm_file:
            instr_count = 0
            for line in asm_file:
                line = line.split('//')[0].strip()
                if not line:
                    continue
                
                instr_type = self.parser.instruction_type(line)
                if instr_type == InstructionType.L_INSTRUCTION:
                    label = self.parser.parse_label(line)
                    self.symbol_table.set_symbol(label, instr_count)
                else:
                    instr_count += 1

    def second_pass(self, input_file, output_file):
        with open(input_file, 'r') as asm_file, open(output_file, 'w') as hack_file:
            for line in asm_file:
                line = line.split('//')[0].strip()
                if not line:
                    continue
                
                binary = self.process_assembly_line(line)
                if binary:
                    hack_file.write(binary + '\n')

    def assemble(self, input_file, output_file):
        """Convert assembly file to hack binary code."""
        self.first_pass(input_file)
        self.second_pass(input_file, output_file)