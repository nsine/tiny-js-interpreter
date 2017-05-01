import re
from js_lexer.js_lexer_error import JsLexerError
import js_token.token_types as token_class

KEYWORDS = [
    'if', 'else',
    'while', 'for', 'break', 'continue',
    'return', 'function', 'var', 'undefined'
]

DEFAULT_FUNCTIONS = [
    'input', 'print', 'parseInt', 'parseFloat'
]

RULES = [
    (r'(\d+)(\b|[^\w])', 'INT_NUMBER'),
    (r'(\d+\.?\d*)(\b|[^\w])', 'FLOAT_NUMBER'),
    (r'\'.*?\'|".*?"', 'STRING'),
    ('|'.join([r'\b{}\b'.format(word) for word in DEFAULT_FUNCTIONS]), 'DEFAULT_FUNCTION'),
    ('|'.join(r'\b{}\b'.format(word) for word in KEYWORDS), 'KEYWORD'),
    (r'[a-zA-Z_]\w*', 'IDENTIFIER'),
    (r';', 'SEMICOLON'),
    (r'\+|-|\*|/|<=|>=|<|>|==|!=|\.|,|&&|\|\||!', 'OPERATOR'),
    (r'=', 'EQUALS'),
    (r'\(|\)|\[|\]|\{|\}', 'DELIMITER'),
    (r':', 'COLON'),
    (r'^ +', 'INDENTATION')
]

TOKEN_CLASSES = {
    'INT_NUMBER': token_class.IntNumberToken,
    'FLOAT_NUMBER': token_class.FloatNumberToken,
    'STRING': token_class.StringToken,
    'KEYWORD': token_class.KeywordToken,
    'IDENTIFIER': token_class.IdentifierToken,
    'SEMICOLON': token_class.SemicolonToken,
    'OPERATOR': token_class.OperatorToken,
    'EQUALS': token_class.EqualsToken,
    'DELIMITER': token_class.DelimiterToken,
    'COLON': token_class.ColonToken,
    'DEFAULT_FUNCTION': token_class.DefaultFunctionToken
}

class JsLexer(object):
    def __init__(self, text):
        self.text = text
        self.lines = text.split('\n')

        self.current_line_number = 0
        self.tokens = []

        group_index = 1
        regex_parts = []
        self.group_type = {}

        for regex, token_type in RULES:
            groupname = 'GROUP%s' % group_index
            regex_parts.append('(?P<%s>%s)' % (groupname, regex))
            self.group_type[groupname] = token_type
            group_index += 1

        self.valid_token_regex = re.compile('|'.join(regex_parts))
        self.skip_whitespaces_regex = re.compile(r'\S+')

    def get_tokens(self):
        all_tokens = []

        indents = []
        indents.append(0)

        for i in range(len(self.lines)):
            self.current_line_number = i
            tokens = self._analyze_line(self.lines[i])
            if len(tokens) == 0:
                continue

            indent_size = 0
            if isinstance(tokens[0], token_class.IndentationToken):
                indent_size = len(tokens[0].value)

            if indent_size != indents[-1]:
                if file_indent_size is None:
                    file_indent_size = indent_size
                    indents.append(indents[-1] + 1)
                    tokens[0] = token_class.IndentToken(None, tokens[0].line, tokens[0].position)
                else:
                    if indent_size == (indents[-1]) * file_indent_size:
                        tokens.pop(0)
                    elif indent_size == (indents[-1] + 1) * file_indent_size:
                        tokens[0] = token_class.IndentToken(None, tokens[0].line,
                                                            tokens[0].position)
                        indents.append(indents[-1] + 1)
                    elif indent_size % file_indent_size == 0 and \
                            indent_size < indents[-1] * file_indent_size:
                        if isinstance(tokens[0], token_class.IndentationToken):
                            tokens.pop(0)

                        while indents[-1] * file_indent_size > indent_size:
                            indents.pop()
                            tokens.insert(0, token_class.DedentToken(None, tokens[0].line,
                                                                     tokens[0].position))
                    else:
                        raise JsLexerError('Incorrect indent size', self.current_line_number,
                                           0, indent_size)

            all_tokens = all_tokens + tokens

        all_tokens.append(token_class.EofToken(None, self.current_line_number, 0))
        return all_tokens

    def _analyze_line(self, line):
        tokens = []
        position = 0
        while True:
            token, position = self._get_token(line, position)
            if token is None:
                break
            else:
                tokens.append(token)

        return tokens

    def _get_token(self, line, position):
        if position >= len(line):
            return (None, position)

        match = self.skip_whitespaces_regex.search(line, position)

        if match:
            position = match.start()

        match = self.valid_token_regex.match(line, position)
        if match:
            groupname = match.lastgroup
            token_type = self.group_type[groupname]
            parsed_token = TOKEN_CLASSES[token_type](match.group(groupname),
                                                     self.current_line_number,
                                                     position)
            position = match.end()
            return (parsed_token, position)

        # if we're here, no rule matched
        raise JsLexerError('Invalid token', self.current_line_number, position, line[position])
