import re
from lexer.python_token import PythonToken
from lexer.lexer_error import LexerError

RULES = [
    (r'\d+\.?\d*', 'NUMBER'),
    (r'\'.*?\'|".*?"', 'STRING'),
    (r'[a-zA-Z_]\w*', 'IDENTIFIER'),
    (r'\+|-|\*|\*\*|/|//|%|@|<<|>>|&|\||\^|~|<|>|<=|>=|==|!=', 'OPERATOR'),
    (r'=', 'EQUALS'),
    (r'\(|\)|\[|\]|\{|\}|,|:', 'DELIMITER'),
    (r'^ *', 'INDENTATION')
]


class Lexer(object):
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
        self.indent_regex = re.compile(r'^ +')

    def get_tokens(self):
        all_tokens = []

        indents = []
        indents.append(0)
        file_indent_size = None

        for i in range(len(self.lines)):
            self.current_line_number = i
            tokens = self._analyze_line(self.lines[i])
            if len(tokens) == 0:
                continue

            indent_size = 0
            if tokens[0].type == 'INDENTATION':
                indent_size = len(tokens[0].value)

            if indent_size != indents[-1]:
                if file_indent_size is None:
                    file_indent_size = indent_size
                    indents.append(indents[-1] + 1)
                    tokens[0].value = 1
                else:
                    if indent_size == (indents[-1]) * file_indent_size:
                        tokens.pop(0)
                    elif indent_size == (indents[-1] + 1) * file_indent_size:
                        tokens[0].value = 1
                        indents.append(indents[-1] + 1)
                    elif indent_size % file_indent_size == 0 and indent_size < indents[-1] * file_indent_size:
                        if tokens[0].type == 'INDENTATION':
                            tokens.pop(0)

                        while indents[-1] * file_indent_size > indent_size:
                            indents.pop()
                            tokens.insert(0, PythonToken('INDENTATION', -1, tokens[0].line, tokens[0].position))

            all_tokens = all_tokens + tokens
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

        if position == 0:
            match = self.indent_regex.search(line, position)
            if match:
                parsed_indent = PythonToken('INDENTATION', match.group(0), self.current_line_number, position)
                position = match.end()
                return (parsed_indent, position)

        match = self.skip_whitespaces_regex.search(line, position)

        if match:
            position = match.start()

        match = self.valid_token_regex.match(line, position)
        if match:
            groupname = match.lastgroup
            token_type = self.group_type[groupname]
            parsed_token = PythonToken(token_type, match.group(groupname), self.current_line_number, position)
            position = match.end()
            return (parsed_token, position)

        # if we're here, no rule matched
        raise LexerError('Invalid token', self.current_line_number, position, line[position])
