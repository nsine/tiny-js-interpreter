import colorama

from js_lexer.js_lexer import JsLexer
from js_lexer.js_lexer_error import JsLexerError

def run():
    colorama.init()

    with open('./test/test.js') as program_file:
        program_text = program_file.read()

        js_lexer = JsLexer(program_text)

        try:
            tokens = js_lexer.get_tokens()
            for token in tokens:
                print(token)
        except JsLexerError as err:
            print(colorama.Fore.RED + str(err))
