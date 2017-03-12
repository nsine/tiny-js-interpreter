from py_parser.exceptions.py_parser_error import PyParserError

class ExpectedButFoundTokenError(PyParserError):
    def __init__(self, expected_token_value, found_token_value, line, position):
        super().__init__(line, position, 'Unexpected token')
        self.expected_token = expected_token_value
        self.found_token = found_token_value

    def __str__(self):
        return "Expected '{}' but found '{}' at line {}, position {}" \
               .format(self.expected_token, self.found_token, self.line + 1, self.position + 1)
