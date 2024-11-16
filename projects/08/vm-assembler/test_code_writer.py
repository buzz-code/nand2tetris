import unittest
from code_writer import CodeWriter
import os

class TestCodeWriter(unittest.TestCase):
    def setUp(self):
        self.test_file = "./test_output.asm"
        self.writer = CodeWriter(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
            
    def assertLinesEqual(self, lines, expected_lines):
        expected_lines.extend([
            "(END)\n",
            "@END\n",
            "0;JMP\n"
        ])
        self.assertEqual(lines, expected_lines)

    def test_write_arithmetic_add(self):
        self.writer.write_arithmetic("add")
        self.writer.close()
        with open(self.test_file, 'r') as file:
            lines = file.readlines()
        expected_lines = [
            "// add\n",
            "@SP\n",
            "AM=M-1\n",
            "D=M\n",
            "A=A-1\n",
            "M=D+M\n"
        ]
        self.assertLinesEqual(lines, expected_lines)

    def test_write_arithmetic_sub(self):
        self.writer.write_arithmetic("sub")
        self.writer.close()
        with open(self.test_file, 'r') as file:
            lines = file.readlines()
        expected_lines = [
            "// sub\n",
            "@SP\n",
            "AM=M-1\n",
            "D=M\n",
            "A=A-1\n",
            "M=M-D\n"
        ]
        self.assertLinesEqual(lines, expected_lines)

    def test_write_arithmetic_neg(self):
        self.writer.write_arithmetic("neg")
        self.writer.close()
        with open(self.test_file, 'r') as file:
            lines = file.readlines()
        expected_lines = [
            "// neg\n",
            "@SP\n",
            "A=M-1\n",
            "M=-M\n"
        ]
        self.assertLinesEqual(lines, expected_lines)

    def test_write_arithmetic_eq(self):
        self.writer.write_arithmetic("eq")
        self.writer.close()
        with open(self.test_file, 'r') as file:
            lines = file.readlines()
        self.assertIn("// eq\n", lines)

    def test_write_arithmetic_gt(self):
        self.writer.write_arithmetic("gt")
        self.writer.close()
        with open(self.test_file, 'r') as file:
            lines = file.readlines()
        self.assertIn("// gt\n", lines)

    def test_write_arithmetic_lt(self):
        self.writer.write_arithmetic("lt")
        self.writer.close()
        with open(self.test_file, 'r') as file:
            lines = file.readlines()
        self.assertIn("// lt\n", lines)

    def test_write_arithmetic_and(self):
        self.writer.write_arithmetic("and")
        self.writer.close()
        with open(self.test_file, 'r') as file:
            lines = file.readlines()
        expected_lines = [
            "// and\n",
            "@SP\n",
            "AM=M-1\n",
            "D=M\n",
            "A=A-1\n",
            "M=D&M\n"
        ]
        self.assertLinesEqual(lines, expected_lines)

    def test_write_arithmetic_or(self):
        self.writer.write_arithmetic("or")
        self.writer.close()
        with open(self.test_file, 'r') as file:
            lines = file.readlines()
        expected_lines = [
            "// or\n",
            "@SP\n",
            "AM=M-1\n",
            "D=M\n",
            "A=A-1\n",
            "M=D|M\n"
        ]
        self.assertLinesEqual(lines, expected_lines)

    def test_write_arithmetic_not(self):
        self.writer.write_arithmetic("not")
        self.writer.close()
        with open(self.test_file, 'r') as file:
            lines = file.readlines()
        expected_lines = [
            "// not\n",
            "@SP\n",
            "A=M-1\n",
            "M=!M\n"
        ]
        self.assertLinesEqual(lines, expected_lines)

    def test_write_push_constant(self):
        self.writer.write_push_pop("push", "constant", 10)
        self.writer.close()
        with open(self.test_file, 'r') as file:
            lines = file.readlines()
        expected_lines = [
            "// push constant 10\n",
            f"@10\n",
            "D=A\n",
            "@SP\n",
            "A=M\n",
            "M=D\n",
            "@SP\n",
            "M=M+1\n"
        ]
        self.assertLinesEqual(lines, expected_lines)
        
    def test_write_label(self):
        self.writer.write_label("LOOP")
        self.writer.close()
        with open(self.test_file, 'r') as file:
            lines = file.readlines()
        expected_lines = [
            "(LOOP)\n"
        ]
        self.assertLinesEqual(lines, expected_lines)
        
    def test_write_goto(self):
        self.writer.write_goto("LOOP")
        self.writer.close()
        with open(self.test_file, 'r') as file:
            lines = file.readlines()
        expected_lines = [
            "@LOOP\n",
            "0;JMP\n"
        ]
        self.assertLinesEqual(lines, expected_lines)
        
    def test_write_if(self):
        self.writer.write_if_goto("LOOP")
        self.writer.close()
        with open(self.test_file, 'r') as file:
            lines = file.readlines()
        expected_lines = [
            "@SP\n",
            "AM=M-1\n",
            "D=M\n",
            "@LOOP\n",
            "D;JNE\n"
        ]
        self.assertLinesEqual(lines, expected_lines)

if __name__ == '__main__':
    unittest.main()