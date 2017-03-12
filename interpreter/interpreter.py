from py_lexer.py_lexer import py_lexer
from parser.parser import Parser

class Interpreter:
    def __init__(self, program_text):
        self.py_lexer = py_lexer(program_text)
        self.parser = Parser()

    def execute(self):
        syntax_tree = self.parser.parse()
        return syntax_tree
