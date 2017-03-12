import colorama
import sys

from lexer.lexer import Lexer
from py_parser.py_parser import PyParser

def run():
    colorama.init()

    with open('./test/test.py') as program_file:
        program_text = program_file.read()

        lexer = Lexer(program_text)
        parser_instance = PyParser(lexer)
        syntax_tree = parser_instance.parse()
        print(syntax_tree)

        sys.exit(0)
