from py_lexer.py_lexer import PyLexer
from py_parser.py_parser import PyParser

from py_parser.exceptions.py_parser_error import PyParserError
from py_lexer.py_lexer_error import PyLexerError

from semantics.semantic_analyzer import SemanticAnalyzer

class Interpreter:
    def __init__(self, program_text):
        self.py_lexer = PyLexer(program_text)
        self.parser = PyParser(self.py_lexer)

    def execute(self):
        try:
            syntax_tree = self.parser.parse()
        except (PyParserError, PyLexerError) as err:
            return {
                'success': False,
                'error': str(err)
            }

