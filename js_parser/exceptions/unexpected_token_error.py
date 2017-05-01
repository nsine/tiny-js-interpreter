from js_parser.exceptions.js_parser_error import JsParserError

class UnexpectedTokenError(JsParserError):
    def __init__(self, token_value, line, position):
        super().__init__(line, position, 'Unexpected token')
        self.token = token_value

    def __str__(self):
        return "{} '{}' at line {}, position {}" \
               .format(self.message, self.token, self.line + 1, self.position + 1)
