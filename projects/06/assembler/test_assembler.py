
import unittest
import os
from assembler import Assembler

class TestAssembler(unittest.TestCase):
    def setUp(self):
        self.assembler = Assembler()
        self.test_asm = "test.asm"
        self.test_hack = "test.hack"

    def tearDown(self):
        # Clean up test files after tests
        for file in [self.test_asm, self.test_hack]:
            if os.path.exists(file):
                os.remove(file)

    def test_process_assembly_line(self):
        # Test A-instruction
        self.assertEqual(
            self.assembler.process_assembly_line("@100"),
            "0000000001100100"
        )

        # Test C-instruction
        self.assertEqual(
            self.assembler.process_assembly_line("D=M"),
            "1111110000010000"
        )
        
        # Test more complex C-instruction
        self.assertEqual(
            self.assembler.process_assembly_line("AMD=D+1;JMP"),
            "1110011111111111"
        )

        # Test label instruction (should return None)
        self.assertIsNone(
            self.assembler.process_assembly_line("(LOOP)")
        )

    def test_full_assembly_process(self):
        # Create a test assembly file
        test_program = """
// Simple test program
@100
D=A
@200
D=D+A
(LOOP)
@LOOP
0;JMP
"""
        with open(self.test_asm, "w") as f:
            f.write(test_program)

        # Assemble the test program
        self.assembler.assemble(self.test_asm, self.test_hack)

        # Check the output
        expected_output = [
            "0000000001100100",  # @100
            "1110110000010000",  # D=A
            "0000000011001000",  # @200
            "1110000010010000",  # D=D+A
            "0000000000000100",  # @LOOP
            "1110101010000111"   # 0;JMP
        ]

        with open(self.test_hack, "r") as f:
            actual_output = [line.strip() for line in f.readlines()]

        self.assertEqual(actual_output, expected_output)

    def test_symbol_handling(self):
        # Test program with symbols
        test_program = """
@i
M=0
(LOOP)
@i
M=M+1
@LOOP
0;JMP
"""
        with open(self.test_asm, "w") as f:
            f.write(test_program)

        self.assembler.assemble(self.test_asm, self.test_hack)

        # Verify symbol table handling
        with open(self.test_hack, "r") as f:
            lines = f.readlines()
            # Check that the symbol 'LOOP' was properly handled
            self.assertIn("0000000000000010\n", lines)  # @LOOP should point to instruction 2

if __name__ == '__main__':
    unittest.main()