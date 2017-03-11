class PyToken:
    def __init__(self, value, line, position):
        self.kind = 'TOKEN'
        self.value = value
        self.line = line
        self.position = position

    def __str__(self):
        return '%s\t(%s) at line %d, position %d' % (self.value, self.kind, self.line, self.position)