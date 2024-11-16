segments = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT"
}
pointers = {
    0: "THIS",
    1: "THAT"
}

class CodeWriter:
    def __init__(self, output_file):
        self.file = open(output_file, 'w')
        self.label_counter = 0
        self.file_name = output_file.split('/')[-1].split('.')[0]

    def write_arithmetic(self, command):
        asm_commands = []
        asm_commands.append(f"// {command}")
        if command == "add":
            asm_commands.extend([
                "@SP",
                "AM=M-1",
                "D=M",
                "A=A-1",
                "M=D+M"
            ])
        elif command == "sub":
            asm_commands.extend([
                "@SP",
                "AM=M-1",
                "D=M",
                "A=A-1",
                "M=M-D"
            ])
        elif command == "neg":
            asm_commands.extend([
                "@SP",
                "A=M-1",
                "M=-M"
            ])
        elif command == "eq":
            asm_commands.extend(self._generate_comparison("JEQ"))
        elif command == "gt":
            asm_commands.extend(self._generate_comparison("JGT"))
        elif command == "lt":
            asm_commands.extend(self._generate_comparison("JLT"))
        elif command == "and":
            asm_commands.extend([
                "@SP",
                "AM=M-1",
                "D=M",
                "A=A-1",
                "M=D&M"
            ])
        elif command == "or":
            asm_commands.extend([
                "@SP",
                "AM=M-1",
                "D=M",
                "A=A-1",
                "M=D|M"
            ])
        elif command == "not":
            asm_commands.extend([
                "@SP",
                "A=M-1",
                "M=!M"
            ])
        self._write_to_file(asm_commands)

    def write_push_pop(self, command, segment, index):
        asm_commands = []
        asm_commands.append(f"// {command} {segment} {index}")
        if command == "push":
            if segment == "constant":
                asm_commands.extend([
                    f"@{index}",
                    "D=A",
                ])
            elif segment == "local" or segment == "argument" or segment == "this" or segment == "that":
                asm_commands.extend([
                    f"@{segments[segment]}",
                    "D=M",
                    f"@{index}",
                    "A=D+A",
                    "D=M"
                ])
            elif segment == "temp":
                asm_commands.extend([
                    f"@{5 + index}",
                    "D=M"
                ])
            elif segment == "static":
                asm_commands.extend([
                    f"@{self.file_name}.{index}",
                    "D=M"
                ])
            elif segment == "pointer":
                asm_commands.extend([
                    f"@{pointers[index]}",
                    "D=M"
                ])
            asm_commands.extend([
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"
            ])
        elif command == "pop":
            if segment == "local" or segment == "argument" or segment == "this" or segment == "that":
                asm_commands.extend([
                    f"@{segments[segment]}",
                    "D=M",
                    f"@{index}",
                    "D=D+A",
                    "@R13",
                    "M=D",
                    "@SP",
                    "AM=M-1",
                    "D=M",
                    "@R13",
                    "A=M",
                    "M=D"
                ])
            elif segment == "temp":
                asm_commands.extend([
                    "@SP",
                    "AM=M-1",
                    "D=M",
                    f"@{5 + index}",
                    "M=D"
                ])
            elif segment == "static":
                asm_commands.extend([
                    "@SP",
                    "AM=M-1",
                    "D=M",
                    f"@{self.file_name}.{index}",
                    "M=D"
                ])
            elif segment == "pointer":
                asm_commands.extend([
                    "@SP",
                    "AM=M-1",
                    "D=M",
                    f"@{pointers[index]}",
                    "M=D"
                ])
        self._write_to_file(asm_commands)

    def write_label(self, label):
        self._write_to_file([f"({label})"])

    def write_goto(self, label):
        self._write_to_file([f"@{label}", "0;JMP"])

    def write_if_goto(self, label):
        self._write_to_file([
            "@SP",
            "AM=M-1",
            "D=M",
            f"@{label}",
            "D;JNE"
        ])


    def _generate_comparison(self, jump_command):
        label_true = f"TRUE_{self.label_counter}"
        label_end = f"END_{self.label_counter}"
        self.label_counter += 1
        return [
            "@SP",
            "AM=M-1",
            "D=M",
            "A=A-1",
            "D=M-D",
            f"@{label_true}",
            f"D;{jump_command}",
            "@SP",
            "A=M-1",
            "M=0",
            f"@{label_end}",
            "0;JMP",
            f"({label_true})",
            "@SP",
            "A=M-1",
            "M=-1",
            f"({label_end})"
        ]

    def _write_to_file(self, commands):
        for command in commands:
            self.file.write(command + '\n')

    def close(self):
        self.write_label("END")
        self.write_goto("END")
        self.file.close()

# Example usage:
# writer = CodeWriter("/path/to/output.asm")
# writer.write_arithmetic("add")
# writer.write_push_pop("push", "constant", 10)
# writer.close()