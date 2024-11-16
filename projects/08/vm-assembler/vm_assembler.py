import sys
from parser import Parser
from code_writer import CodeWriter

class VmAssembler:
    def __init__(self, input_file):
        self.input_file = input_file
        output_file = input_file.replace(".vm", ".asm")
        self.code_writer = CodeWriter(output_file)
    
    def translate(self):
        with open(self.input_file) as f:
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
        self.code_writer.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python vm-assembler.py <file.vm>')
        sys.exit(1)

    input_file = sys.argv[1]
    vm_assembler = VmAssembler(input_file)
    vm_assembler.translate()
