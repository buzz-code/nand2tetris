
from symbol_table import SymbolTable

class Code:
    """A class to handle binary code conversion for the Hack assembly language."""
    
    def __init__(self):
        self._init_comp_table()
        self._init_jump_table()

    def _init_comp_table(self):
        """Initialize the computation mnemonic table."""
        self.comp_table = {
            '0':   '0101010',
            '1':   '0111111',
            '-1':  '0111010',
            'D':   '0001100',
            'A':   '0110000',
            'M':   '1110000',
            '!D':  '0001101',
            '!A':  '0110001',
            '!M':  '1110001',
            '-D':  '0001111',
            '-A':  '0110011',
            '-M':  '1110011',
            'D+1': '0011111',
            'A+1': '0110111',
            'M+1': '1110111',
            'D-1': '0001110',
            'A-1': '0110010',
            'M-1': '1110010',
            'D+A': '0000010',
            'D+M': '1000010',
            'D-A': '0010011',
            'D-M': '1010011',
            'A-D': '0000111',
            'M-D': '1000111',
            'D&A': '0000000',
            'D&M': '1000000',
            'D|A': '0010101',
            'D|M': '1010101'
        }

    def _init_jump_table(self):
        """Initialize the jump mnemonic table."""
        self.jump_table = {
            'null': '000',
            'JGT':  '001',
            'JEQ':  '010',
            'JGE':  '011',
            'JLT':  '100',
            'JNE':  '101',
            'JLE':  '110',
            'JMP':  '111'
        }

    def number_or_symbol_to_binary(self, value: str, symbol_table: SymbolTable) -> str:
        """Convert number or symbol to 16-bit binary."""
        if not value.isdigit():
            value = symbol_table.get_symbol(value)
        return format(int(value), '015b')

    def jump_to_binary(self, jump: str) -> str:
        """Convert jump mnemonic to 3-bit binary."""
        return self.jump_table.get(jump, '000')

    def dest_to_binary(self, dest: str) -> str:
        """Convert destination mnemonic to 3-bit binary."""
        dest_bits = ['0', '0', '0']  # A, D, M
        if dest is None or dest == 'null':
            return ''.join(dest_bits)
        if 'A' in dest: dest_bits[0] = '1'
        if 'D' in dest: dest_bits[1] = '1'
        if 'M' in dest: dest_bits[2] = '1'
        return ''.join(dest_bits)

    def comp_to_binary(self, comp: str) -> str:
        """Convert computation mnemonic to 7-bit binary."""
        return self.comp_table.get(comp, '0000000')
