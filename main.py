import colorama

from lexer.lexer import Lexer
from lexer.lexer_error import LexerError

colorama.init()

with open('./test/test.py') as program_file:
    program_text = program_file.read()

    lexer = Lexer(program_text)

    try:
        tokens = lexer.get_tokens()
        for token in tokens:
            print(token)
    except LexerError as err:
        print(colorama.Fore.RED + str(err))
