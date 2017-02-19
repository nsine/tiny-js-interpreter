class PyToken(object):
    def __init__(self, token_type, value, line, position):
        self.type = token_type
        self.value = value
        self.line = line
        self.position = position

    def __str__(self):
        return '%s\t(%s) at line %d, position %d' % (self.value, self.type, self.line, self.position)