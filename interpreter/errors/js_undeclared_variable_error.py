class JsUndeclaredVariableError(Exception):
    def __init__(self, variable_name, position):
        self.variable_name = variable_name
        self.message = 'Undeclared variable {}'.format(variable_name)
        self.position = position

def __str__(self):
    return 'Error: {} at line {}, position {}' \
           .format(self.message, self.position['line'], self.position['position'])