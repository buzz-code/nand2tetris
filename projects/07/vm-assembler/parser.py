class Parser:
    def __init__(self, command):
        self.command = command.strip()
        self.command_type = None
        self.arg1 = None
        self.arg2 = None
        self.parse_command()

    def parse_command(self):
        parts = self.command.split()
        if not parts:
            return

        command = parts[0]
        if command in ["push", "pop"]:
            self.command_type = command
            self.arg1 = parts[1]
            self.arg2 = int(parts[2])
        else:
            self.command_type = "arithmetic"
            self.arg1 = command

    def get_command_type(self):
        return self.command_type

    def get_arg1(self):
        return self.arg1

    def get_arg2(self):
        return self.arg2