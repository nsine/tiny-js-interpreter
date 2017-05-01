class JsRuntimeError(Exception):
    def __init__(self, message, position):
        self.message = message
        self.position = position

def __str__(self):
    return 'Runtime error: {} at line {}, position {}' \
           .format(self.message, self.position['line'], self.position['position'])