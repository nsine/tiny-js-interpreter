from .js_parser_error import JsParserError

class ExpectedButFoundTokenError(JsParserError):
    def __init__(self, expected_token_value, found_token_value, position):
        super().__init__(position, 'Unexpected token')
        self.expected_token = expected_token_value
        self.found_token = found_token_value

    def __str__(self):
        return "Expected '{}' but found '{}' at line {}, position {}" \
               .format(self.expected_token, self.found_token, self.position.line + 1, self.position.column + 1)
