class JsTypeError(Exception):
    def __init__(self, message='Incorrect type', position=None):
        self.message = message
        self.position = position

def __str__(self):
    if self.position is not None:
        return 'Type error: {} at line {}, position {}' \
            .format(self.message, self.position['line'], self.position['position'])
    else:
        return 'Type error: {}' \
            .format(self.message)