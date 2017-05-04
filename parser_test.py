import colorama

from js_lexer.js_lexer import JsLexer
from js_parser.js_parser import JsParser
from js_parser.errors.js_parser_error import JsParserError
from js_lexer.js_lexer_error import JsLexerError

def run():
    colorama.init()

    with open('./test/test.js') as program_file:
        program_text = program_file.read()

        js_lexer = JsLexer(program_text)
        py_parse = JsParser(js_lexer)
        try:
            syntax_tree = py_parse.parse()
            print(syntax_tree)
        except (JsParserError, JsLexerError) as err:
            print(colorama.Fore.RED + str(err))
