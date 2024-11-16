import unittest
from parser import Parser

class TestParser(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_command_type(self):
        parser = Parser("add")
        self.assertEqual(parser.get_command_type(), "arithmetic")

        parser = Parser("push constant 7")
        self.assertEqual(parser.get_command_type(), "push")

        parser = Parser("pop local 0")
        self.assertEqual(parser.get_command_type(), "pop")
        
        parser = Parser("label LOOP")
        self.assertEqual(parser.get_command_type(), "label")
        
        parser = Parser("goto LOOP")
        self.assertEqual(parser.get_command_type(), "goto")
        
        parser = Parser("if-goto LOOP")
        self.assertEqual(parser.get_command_type(), "if-goto")

    def test_get_arg1(self):
        parser = Parser("add")
        self.assertEqual(parser.get_arg1(), "add")

        parser = Parser("push constant 7")
        self.assertEqual(parser.get_arg1(), "constant")

        parser = Parser("pop local 0")
        self.assertEqual(parser.get_arg1(), "local")
        
        parser = Parser("label LOOP")
        self.assertEqual(parser.get_arg1(), "LOOP")
        
        parser = Parser("goto LOOP")
        self.assertEqual(parser.get_arg1(), "LOOP")
        
        parser = Parser("if-goto LOOP")
        self.assertEqual(parser.get_arg1(), "LOOP")

    def test_get_arg2(self):
        parser = Parser("add")
        self.assertEqual(parser.get_arg2(), None)

        parser = Parser("push constant 7")
        self.assertEqual(parser.get_arg2(), 7)

        parser = Parser("pop local 0")
        self.assertEqual(parser.get_arg2(), 0)
        
        parser = Parser("label LOOP")
        self.assertEqual(parser.get_arg2(), None)
        
        parser = Parser("goto LOOP")
        self.assertEqual(parser.get_arg2(), None)

        parser = Parser("if-goto LOOP")
        self.assertEqual(parser.get_arg2(), None)
