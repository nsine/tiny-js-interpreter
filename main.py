from lexer.lexer import Lexer
from lexer.lexer_error import LexerError

with open('./test/test.py') as program_file:
    program_text = program_file.read()

    lexer = Lexer(program_text)
    tokens = lexer.get_tokens()

    try:
        for token in tokens:
            print(token)
    except LexerError as err:
        print('LexerError at position %s' % err.position)
