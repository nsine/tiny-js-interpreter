class JsArgumentError(Exception):
    def __init__(self, message, position=None):
        self.message = message
        self.position = position

def __str__(self):
    if self.position is not None:
        return 'Argument error: {} at line {}, position {}' \
            .format(self.message, self.position['line'], self.position['position'])
    else:
        return 'Argument error: {}' \
            .format(self.message)