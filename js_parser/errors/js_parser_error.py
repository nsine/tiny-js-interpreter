class JsParserError(Exception):
    def __init__(self, position, message='Parser error'):
        self.message = message
        self.position = position

    def __str__(self):
        result = self.message
        if self.position is not None:
            result += " at line {}, position {}".format(
                self.position.line + 1, self.position.column + 1
            )
        return result
