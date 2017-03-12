import colorama

from py_lexer.py_lexer import PyLexer
from py_lexer.py_lexer_error import PyLexerError

def run():
    colorama.init()

    with open('./test/test.py') as program_file:
        program_text = program_file.read()

        py_lexer = PyLexer(program_text)

        try:
            tokens = py_lexer.get_tokens()
            for token in tokens:
                print(token)
        except PyLexerError as err:
            print(colorama.Fore.RED + str(err))
