class JsRuntimeError(Exception):
    def __init__(self, message, position):
        self.message = message
        self.position = position

    def __str__(self):
        return 'RuntimeError: {} at line {}, position {}' \
            .format(self.message, self.position.line + 1, self.position.column + 1)