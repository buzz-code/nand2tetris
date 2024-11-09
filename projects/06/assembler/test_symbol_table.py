
import unittest
from symbol_table import SymbolTable

class TestSymbolTable(unittest.TestCase):
    def setUp(self):
        self.symbol_table = SymbolTable()

    def test_predefined_symbols(self):
        # Test predefined RAM locations
        self.assertEqual(self.symbol_table.get_symbol('R0'), 0)
        self.assertEqual(self.symbol_table.get_symbol('R15'), 15)
        
        # Test predefined pointers
        self.assertEqual(self.symbol_table.get_symbol('SP'), 0)
        self.assertEqual(self.symbol_table.get_symbol('LCL'), 1)
        self.assertEqual(self.symbol_table.get_symbol('ARG'), 2)
        self.assertEqual(self.symbol_table.get_symbol('THIS'), 3)
        self.assertEqual(self.symbol_table.get_symbol('THAT'), 4)
        
        # Test predefined I/O pointers
        self.assertEqual(self.symbol_table.get_symbol('SCREEN'), 16384)
        self.assertEqual(self.symbol_table.get_symbol('KBD'), 24576)

    def test_set_and_get_symbol(self):
        # Test setting new symbols
        self.symbol_table.set_symbol('LOOP', 50)
        self.assertEqual(self.symbol_table.get_symbol('LOOP'), 50)
        
        # Test overwriting existing symbol
        self.symbol_table.set_symbol('LOOP', 60)
        self.assertEqual(self.symbol_table.get_symbol('LOOP'), 60)

    def test_auto_address_allocation(self):
        # Test automatic address allocation for new variables
        first_var = self.symbol_table.get_symbol('first')
        self.assertEqual(first_var, 16)  # First variable should get address 16
        
        second_var = self.symbol_table.get_symbol('second')
        self.assertEqual(second_var, 17)  # Second variable should get address 17
        
        # Test that same variable returns same address
        self.assertEqual(self.symbol_table.get_symbol('first'), 16)

if __name__ == '__main__':
    unittest.main()