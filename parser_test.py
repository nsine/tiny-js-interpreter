import colorama

from py_lexer.py_lexer import PyLexer
from py_parser.py_parser import PyParser
from py_parser.exceptions.py_parser_error import PyParserError
from py_lexer.py_lexer_error import PyLexerError

def run():
    colorama.init()

    with open('./test/test.py') as program_file:
        program_text = program_file.read()

        py_lexer = PyLexer(program_text)
        py_parse = PyParser(py_lexer)
        try:
            syntax_tree = py_parse.parse()
            print(syntax_tree)
        except (PyParserError, PyLexerError) as err:
            print(colorama.Fore.RED + str(err))
