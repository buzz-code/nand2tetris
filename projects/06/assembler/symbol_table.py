class SymbolTable:
    def __init__(self):
        # Initialize with predefined symbols
        self.table = {
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4,
            'R0': 0,
            'R1': 1,
            'R2': 2,
            'R3': 3,
            'R4': 4,
            'R5': 5,
            'R6': 6,
            'R7': 7,
            'R8': 8,
            'R9': 9,
            'R10': 10,
            'R11': 11,
            'R12': 12,
            'R13': 13,
            'R14': 14,
            'R15': 15,
            'SCREEN': 16384,
            'KBD': 24576
        }
        self.next_available_address = 16  # Variables start from address 16

    def set_symbol(self, symbol, value):
        """Set a symbol with a specific value in the table."""
        self.table[symbol] = value

    def get_symbol(self, symbol):
        """
        Get the value of a symbol. If it doesn't exist,
        assign it the next available address.
        """
        if symbol not in self.table:
            self.table[symbol] = self.next_available_address
            self.next_available_address += 1
        return self.table[symbol]
