class JsLexerError(Exception):
    def __init__(self, message, line, position, value):
        self.message = message
        self.line = line
        self.position = position
        self.value = value

    def __str__(self):
        return "{} \'{}\' at line {}, position {}" \
               .format(self.message, self.value, self.line + 1, self.position + 1)
