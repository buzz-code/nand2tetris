import unittest
from unittest.mock import MagicMock, patch
from vm_assembler import VmAssembler

class TestVmAssembler(unittest.TestCase):
    @patch('vm_assembler.Parser')
    @patch('vm_assembler.CodeWriter')
    def test_translate_arithmetic(self, MockCodeWriter, MockParser):
        # Setup
        mock_code_writer = MockCodeWriter.return_value
        mock_parser = MockParser.return_value
        mock_parser.get_command_type.return_value = "arithmetic"
        mock_parser.get_arg1.return_value = "add"
        
        input_file = 'test.vm'
        with patch('builtins.open', unittest.mock.mock_open(read_data='add\n')):
            vm_assembler = VmAssembler(input_file)
            vm_assembler.translate()
        
        # Assertions
        mock_parser.get_command_type.assert_called_once()
        mock_parser.get_arg1.assert_called_once()
        mock_code_writer.write_arithmetic.assert_called_once_with("add")
        mock_code_writer.close.assert_called_once()

    @patch('vm_assembler.Parser')
    @patch('vm_assembler.CodeWriter')
    def test_translate_push_pop(self, MockCodeWriter, MockParser):
        # Setup
        mock_code_writer = MockCodeWriter.return_value
        mock_parser = MockParser.return_value
        mock_parser.get_command_type.return_value = "push"
        mock_parser.get_arg1.return_value = "constant"
        mock_parser.get_arg2.return_value = "10"
        
        input_file = 'test.vm'
        with patch('builtins.open', unittest.mock.mock_open(read_data='push constant 10\n')):
            vm_assembler = VmAssembler(input_file)
            vm_assembler.translate()
        
        # Assertions
        mock_parser.get_command_type.assert_called_once()
        mock_parser.get_arg1.assert_called_once()
        mock_parser.get_arg2.assert_called_once()
        mock_code_writer.write_push_pop.assert_called_once_with("push", "constant", "10")
        mock_code_writer.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()