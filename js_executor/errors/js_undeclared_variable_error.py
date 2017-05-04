from .js_runtime_error import JsRuntimeError

class JsUndeclaredVariableError(JsRuntimeError):
    def __init__(self, variable_name, position):
        super().__init__("Undeclared variable '{}'".format(variable_name), position)

    def __str__(self):
        return 'ReferenceError: {} at line {}, position {}' \
            .format(self.message, self.position.line + 1, self.position.column + 1)