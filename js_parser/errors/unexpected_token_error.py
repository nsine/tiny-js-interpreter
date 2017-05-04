from .js_parser_error import JsParserError

class UnexpectedTokenError(JsParserError):
    def __init__(self, token_value, position):
        super().__init__(position, 'Unexpected token')
        self.token = token_value

    def __str__(self):
        return "{} '{}' at line {}, position {}" \
               .format(self.message, self.token, self.position.line + 1, self.position.column + 1)
