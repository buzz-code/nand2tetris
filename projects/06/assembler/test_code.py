
import unittest
from code import Code
from symbol_table import SymbolTable

class TestCode(unittest.TestCase):
    def setUp(self):
        self.code = Code()
        self.symbol_table = SymbolTable()

    def test_number_to_binary(self):
        self.assertEqual(self.code.number_or_symbol_to_binary("0", self.symbol_table), "000000000000000")
        self.assertEqual(self.code.number_or_symbol_to_binary("15", self.symbol_table), "000000000001111")
        self.assertEqual(self.code.number_or_symbol_to_binary("16383", self.symbol_table), "011111111111111")
        # Test symbol table lookup
        self.symbol_table.set_symbol("test_var", 42)
        self.assertEqual(self.code.number_or_symbol_to_binary("test_var", self.symbol_table), "000000000101010")

    def test_jump_to_binary(self):
        self.assertEqual(self.code.jump_to_binary("null"), "000")
        self.assertEqual(self.code.jump_to_binary("JGT"), "001")
        self.assertEqual(self.code.jump_to_binary("JMP"), "111")
        self.assertEqual(self.code.jump_to_binary("invalid"), "000")  # Test invalid jump

    def test_dest_to_binary(self):
        self.assertEqual(self.code.dest_to_binary("null"), "000")
        self.assertEqual(self.code.dest_to_binary("M"), "001")
        self.assertEqual(self.code.dest_to_binary("D"), "010")
        self.assertEqual(self.code.dest_to_binary("MD"), "011")
        self.assertEqual(self.code.dest_to_binary("A"), "100")
        self.assertEqual(self.code.dest_to_binary("AM"), "101")
        self.assertEqual(self.code.dest_to_binary("AD"), "110")
        self.assertEqual(self.code.dest_to_binary("AMD"), "111")

    def test_comp_to_binary(self):
        # Test zero and one
        self.assertEqual(self.code.comp_to_binary("0"), "0101010")
        self.assertEqual(self.code.comp_to_binary("1"), "0111111")
        
        # Test register operations
        self.assertEqual(self.code.comp_to_binary("D"), "0001100")
        self.assertEqual(self.code.comp_to_binary("A"), "0110000")
        self.assertEqual(self.code.comp_to_binary("M"), "1110000")
        
        # Test arithmetic operations
        self.assertEqual(self.code.comp_to_binary("D+1"), "0011111")
        self.assertEqual(self.code.comp_to_binary("A-1"), "0110010")
        self.assertEqual(self.code.comp_to_binary("D+A"), "0000010")
        
        # Test invalid computation
        self.assertEqual(self.code.comp_to_binary("invalid"), "0000000")

if __name__ == '__main__':
    unittest.main()