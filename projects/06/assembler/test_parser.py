import unittest
from parser import Parser, InstructionType

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_instruction_type(self):
        self.assertEqual(self.parser.instruction_type("@100"), InstructionType.A_INSTRUCTION)
        self.assertEqual(self.parser.instruction_type("@i"), InstructionType.A_INSTRUCTION)
        self.assertEqual(self.parser.instruction_type("(LOOP)"), InstructionType.L_INSTRUCTION)
        self.assertEqual(self.parser.instruction_type("D=M"), InstructionType.C_INSTRUCTION)
        self.assertEqual(self.parser.instruction_type("0;JMP"), InstructionType.C_INSTRUCTION)

    def test_parse_a_instruction(self):
        self.assertEqual(self.parser.parse_a_instruction("@100"), "100")
        self.assertEqual(self.parser.parse_a_instruction("@variable"), "variable")
        self.assertEqual(self.parser.parse_a_instruction("@R0"), "R0")
        
        with self.assertRaises(ValueError):
            self.parser.parse_a_instruction("D=M")

    def test_parse_c_instruction(self):
        # Test dest=comp
        self.assertEqual(self.parser.parse_c_instruction("D=M"), ("D", "M", ""))
        
        # Test comp;jump
        self.assertEqual(self.parser.parse_c_instruction("0;JMP"), ("", "0", "JMP"))
        
        # Test dest=comp;jump
        self.assertEqual(self.parser.parse_c_instruction("AMD=D+1;JGT"), ("AMD", "D+1", "JGT"))
        
        # Test comp only
        self.assertEqual(self.parser.parse_c_instruction("D+1"), ("", "D+1", ""))

    def test_parse_label(self):
        self.assertEqual(self.parser.parse_label("(LOOP)"), "LOOP")
        self.assertEqual(self.parser.parse_label("(END)"), "END")
        
        with self.assertRaises(ValueError):
            self.parser.parse_label("@100")
        with self.assertRaises(ValueError):
            self.parser.parse_label("LOOP")

if __name__ == '__main__':
    unittest.main()
