from .js_runtime_error import JsRuntimeError

class JsTypeError(JsRuntimeError):
    def __init__(self, message='Incorrect type', position=None):
        super().__init__(message, position)

    def __str__(self):
        if self.position is not None:
            return 'TypeError: {} at line {}, position {}' \
                .format(self.message, self.position.line + 1, self.position.column + 1)
        else:
            return 'TypeError: {}' \
                .format(self.message)