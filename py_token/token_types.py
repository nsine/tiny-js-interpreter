from py_token.py_token import PyToken

class IdentifierToken(PyToken):
    def __init__(self, value, line, position):
        super().__init__(value, line, position)
        self.kind = 'IDENTIFIER'

class IntNumberToken(PyToken):
    def __init__(self, value, line, position):
        super().__init__(value, line, position)
        self.kind = 'INT_NUMBER'

class FloatNumberToken(PyToken):
    def __init__(self, value, line, position):
        super().__init__(value, line, position)
        self.kind = 'FLOAT_NUMBER'

class StringToken(PyToken):
    def __init__(self, value, line, position):
        super().__init__(value, line, position)
        self.kind = 'STRING'

class KeywordToken(PyToken):
    def __init__(self, value, line, position):
        super().__init__(value, line, position)
        self.kind = 'KEYWORD'

class EndlineToken(PyToken):
    def __init__(self, value, line, position):
        super().__init__(value, line, position)
        self.kind = 'ENDLINE'

class OperatorToken(PyToken):
    def __init__(self, value, line, position):
        super().__init__(value, line, position)
        self.kind = 'OPERATOR'

class DelimiterToken(PyToken):
    def __init__(self, value, line, position):
        super().__init__(value, line, position)
        self.kind = 'DELIMITER'

class IndentationToken(PyToken):
    def __init__(self, value, line, position):
        super().__init__(value, line, position)
        self.kind = 'INDENTATION'

class IndentToken(IndentationToken):
    def __init__(self, value, line, position):
        super().__init__(value, line, position)
        self.kind = 'INDENT'

class DedentToken(IndentationToken):
    def __init__(self, value, line, position):
        super().__init__(value, line, position)
        self.kind = 'DEDENT'

class EqualsToken(PyToken):
    def __init__(self, value, line, position):
        super().__init__(value, line, position)
        self.kind = 'EQUALS'

class ColonToken(PyToken):
    def __init__(self, value, line, position):
        super().__init__(value, line, position)
        self.kind = 'COLON'