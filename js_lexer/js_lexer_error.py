class JsLexerError(Exception):
    def __init__(self, message, position, value):
        self.message = message
        self.position = position
        self.value = value

    def __str__(self):
        return "{} \'{}\' at line {}, position {}" \
               .format(self.message, self.value, self.position.line + 1, self.position.column + 1)
