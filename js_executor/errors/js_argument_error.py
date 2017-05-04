from .js_runtime_error import JsRuntimeError

class JsArgumentError(JsRuntimeError):
    def __init__(self, message, position=None):
        super().__init__(message, position)

    def __str__(self):
        if self.position is not None:
            return 'ArgumentError: {} at line {}, position {}' \
                .format(self.message, self.position.line + 1, self.position.column + 1)
        else:
            return 'ArgumentError: {}' \
                .format(self.message)