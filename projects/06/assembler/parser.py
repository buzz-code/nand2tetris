from enum import Enum

class InstructionType(Enum):
    A_INSTRUCTION = 'A'  # @value
    C_INSTRUCTION = 'C'  # dest=comp;jump
    L_INSTRUCTION = 'L'  # (LABEL)

class Parser:
    def __init__(self):
        pass

    def parse_a_instruction(self, instruction: str) -> str:
        """Parse A-instruction (@value) and return the value as integer"""
        if not instruction.startswith('@'):
            raise ValueError("Not an A-instruction")
        
        # Remove @
        return instruction[1:]

    def parse_c_instruction(self, instruction: str) -> tuple[str, str, str]:
        """Parse C-instruction (dest=comp;jump) and return (dest, comp, jump)"""
        # Initialize default values
        dest = ''
        comp = ''
        jump = ''

        # Split by '=' first
        parts = instruction.split('=', 1)
        if len(parts) == 2:
            dest = parts[0]
            instruction = parts[1]
        else:
            instruction = parts[0]

        # Split remaining by ';'
        parts = instruction.split(';', 1)
        comp = parts[0]
        if len(parts) == 2:
            jump = parts[1]

        return (dest, comp, jump)
    
    def parse_label(self, instruction: str) -> str:
        """Parse L-instruction ((LABEL)) and return the label name"""
        if not (instruction.startswith('(') and instruction.endswith(')')):
            raise ValueError("Not a label instruction")
        return instruction[1:-1]
    
    def instruction_type(self, instruction: str) -> InstructionType:
        if instruction.startswith('@'):
            return InstructionType.A_INSTRUCTION
        elif instruction.startswith('(') and instruction.endswith(')'):
            return InstructionType.L_INSTRUCTION
        else:
            return InstructionType.C_INSTRUCTION