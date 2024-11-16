import sys
import os
from parser import Parser
from code_writer import CodeWriter

class VmAssembler:
    def __init__(self, input_file):
        if input_file.endswith(".vm"):
            self.input_files = [input_file]
            self.output_file = input_file.replace(".vm", ".asm")
        else:
            self.input_files = [f"{input_file}/{f}" for f in os.listdir(input_file) if f.endswith(".vm")]
            folder_name = input_file.split("/")[-1]
            self.output_file = f"{input_file}/{folder_name}.asm"
        self.code_writer = CodeWriter(self.output_file)
    
    def translate(self):
        self.code_writer.init()
        for input_file in self.input_files:
            self.code_writer.set_file_name(input_file.split("/")[-1].split(".")[0])
            self.translate_file(input_file)
        self.code_writer.close()
    
    def translate_file(self, input_file):
        with open(input_file) as f:
            for line in f:
                parser = Parser(line.split("//")[0])
                command_type = parser.get_command_type()
                if command_type == "arithmetic":
                    self.code_writer.write_arithmetic(parser.get_arg1())
                elif command_type in ["push", "pop"]:
                    self.code_writer.write_push_pop(command_type, parser.get_arg1(), parser.get_arg2())
                elif command_type == "label":
                    self.code_writer.write_label(parser.get_arg1())
                elif command_type == "goto":
                    self.code_writer.write_goto(parser.get_arg1())
                elif command_type == "if-goto":
                    self.code_writer.write_if_goto(parser.get_arg1())
                elif command_type == "function":
                    self.code_writer.write_function(parser.get_arg1(), parser.get_arg2())
                elif command_type == "call":
                    self.code_writer.write_call(parser.get_arg1(), parser.get_arg2())
                elif command_type == "return":
                    self.code_writer.write_return()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python vm-assembler.py <file.vm or directory>')
        sys.exit(1)

    input_file = sys.argv[1]
    vm_assembler = VmAssembler(input_file)
    vm_assembler.translate()
