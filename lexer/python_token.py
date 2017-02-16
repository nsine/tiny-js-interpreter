class PythonToken(object):
    def __init__(self, token_type, value, line, position):
        self.type = token_type
        self.value = value
        self.line = line
        self.position = position

    def __str__(self):
        return '%s at (%d, %d) - %s' % (self.type, self.line, self.position, self.value)