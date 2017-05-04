class JsToken:
    def __init__(self, value, position):
        self.kind = 'TOKEN'
        self.value = value
        self.position = position

    def __str__(self):
        return '%s\t(%s) at line %d, position %d' % \
            (self.value, self.kind, self.position.line + 1, self.position.column + 1)
