from .js_token import JsToken

class IdentifierToken(JsToken):
    def __init__(self, value, position):
        super().__init__(value, position)
        self.kind = 'IDENTIFIER'

class NumberToken(JsToken):
    def __init__(self, value, position):
        super().__init__(value, position)
        self.kind = 'NUMBER'

class StringToken(JsToken):
    def __init__(self, value, position):
        super().__init__(value, position)
        self.kind = 'STRING'

class KeywordToken(JsToken):
    def __init__(self, value, position):
        super().__init__(value, position)
        self.kind = 'KEYWORD'

class SemicolonToken(JsToken):
    def __init__(self, value, position):
        super().__init__(value, position)
        self.kind = 'SEMICOLON'

class OperatorToken(JsToken):
    def __init__(self, value, position):
        super().__init__(value, position)
        self.kind = 'OPERATOR'

class MathOperatorToken(JsToken):
    def __init__(self, value, position):
        super().__init__(value, position)
        self.kind = 'MATH_OPERATOR'

class CompareOperatorToken(JsToken):
    def __init__(self, value, position):
        super().__init__(value, position)
        self.kind = 'COMPARE_OPERATOR'

class DelimiterToken(JsToken):
    def __init__(self, value, position):
        super().__init__(value, position)
        self.kind = 'DELIMITER'

class EqualsToken(JsToken):
    def __init__(self, value, position):
        super().__init__(value, position)
        self.kind = 'EQUALS'

class ColonToken(JsToken):
    def __init__(self, value, position):
        super().__init__(value, position)
        self.kind = 'COLON'

class EofToken(JsToken):
    def __init__(self, value, position):
        super().__init__(value, position)
        self.kind = 'EOF'

class DefaultFunctionToken(JsToken):
    def __init__(self, value, position):
        super().__init__(value, position)
        self.kind = 'DEFAULT_FUNCTION'
