from lexer.lexer import Lexer
from parser.parser import Parser

class Interpreter:
    def __init__(self, program_text):
        self.lexer = Lexer(program_text)
        self.parser = Parser()

    def execute(self):
        syntax_tree = self.parser.parse()
        return syntax_tree
