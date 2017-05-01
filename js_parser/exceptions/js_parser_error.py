class JsParserError(Exception):
    def __init__(self, line, position, message='Parser error'):
        self.message = message
        self.line = line
        self.position = position

    def unexpected(self, token_value, line, position):
        return JsParserError(
            line, position,
            "Unexpected token {}".format(token_value),
            token_value
        )

    def expected_but_found(self, token_value, line, position):
        return JsParserError(
            line, position,
            "Unexpected token {}".format(token_value),
            token_value
        )

    def __str__(self):
        result = self.message
        if self.line is not None:
            result += " at line {}".format(self.line + 1)
        if self.position is not None:
            result += ",position {}".format(self.position + 1)
        return result
