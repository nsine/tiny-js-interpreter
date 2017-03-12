from py_parser.node import Node
from py_parser.node_type import NodeType
import py_token.token_types as tt
import sys
import copy

class PyParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = []
        self.token_index = -1
        self.token = None

    def error(self, msg):
        print('Parser error:', msg)
        sys.exit(1)

    def unexpected_token_error(self, value, line, position):
        print('Unexpected token {} at line {}, position {}:'.format(value, line, position))
        sys.exit(1)

    def expected_token_error(self, expected_value, found_value, line, position):
        print('Expected {}, but found {} at line {}, position {}:'
              .format(expected_value, found_value, line, position))
        sys.exit(1)

    def callable(self, source_node):
        return Node(NodeType.Call, children=[source_node, self.sequence(')')])

    def attribute(self, source_node):
        if not isinstance(self.token, tt.IdentifierToken):
            self.expected_token_error('attribute name', self.token.value,
                                      self.token.line, self.token.position)
        node = Node(NodeType.Attribute, self.token.value, children=[source_node])
        self._next_token()

        if (isinstance(self.token, tt.DelimiterToken) and self.token.value == '('):
            self._next_token()
            return self.callable(node)

    def sequence(self, end_seq_value):
        node = Node(NodeType.Seq)
        while True:
            if isinstance(self.token, tt.DelimiterToken) and self.token.value == end_seq_value:
                self._next_token()
                return node
            node.children.append(self.test())
            if isinstance(self.token, tt.OperatorToken) and self.token.value == ',':
                self._next_token()
            elif isinstance(self.token, tt.DelimiterToken) and self.token.value == end_seq_value:
                continue
            else:
                self.unexpected_token_error(self.token.value, self.token.line, self.token.position)

    def term(self):
        if isinstance(self.token, tt.DefaultFunctionToken):
            node = Node(NodeType.DefaultFunction, self.token.value)
            self._next_token()
            if isinstance(self.token, tt.DelimiterToken) and self.token.value == '(':
                self._next_token()
                node = self.callable(node)
            return node

        node_type = None
        if isinstance(self.token, tt.IdentifierToken):
            node_type = NodeType.Var
        elif isinstance(self.token, tt.IntNumberToken):
            node_type = NodeType.IntConst
        elif isinstance(self.token, tt.FloatNumberToken):
            node_type = NodeType.FloatConst
        elif isinstance(self.token, tt.StringToken):
            node_type = NodeType.StringConst

        if node_type is not None:
            node = Node(node_type, self.token.value)
            self._next_token()

            if isinstance(self.token, tt.OperatorToken) and self.token.value == '.':
                self._next_token()
                node = self.attribute(node)
            elif isinstance(self.token, tt.DelimiterToken) and self.token.value == '(':
                self._next_token()
                node = self.callable(node)
            return node
        elif isinstance(self.token, tt.DelimiterToken) and self.token.value == '(':
            return self.paren_expr()
        else:
            self.unexpected_token_error(self.token.value, self.token.line, self.token.position)

    def math_expr(self):
        node = self.term()
        while True:
            if isinstance(self.token, tt.OperatorToken):
                if self.token.value == '+':
                    kind = NodeType.Add
                elif self.token.value == '-':
                    kind = NodeType.Sub
                elif self.token.value == '*':
                    kind = NodeType.Mul
                elif self.token.value == '/':
                    kind = NodeType.Div
                else:
                    break
            else:
                break
            self._next_token()
            node = Node(kind, children=[node, self.term()])
        return node

    def test(self):
        node = self.math_expr()
        if isinstance(self.token, tt.OperatorToken):
            if self.token.value == '<':
                kind = NodeType.Lower
            elif self.token.value == '>':
                kind = NodeType.Greater
            elif self.token.value == '<=':
                kind = NodeType.LowerEq
            elif self.token.value == '>=':
                kind = NodeType.GreaterEq
            elif self.token.value == '==':
                kind = NodeType.Equals
            elif self.token.value == '!=':
                kind = NodeType.NotEquals
            else:
                return node
            node = Node(kind, children=[node, self.math_expr()])
        return node

    def expr(self):
        if not isinstance(self.token, tt.IdentifierToken):
            return self.test()
        node = self.test()
        if node.kind == NodeType.Var and isinstance(self.token, tt.EqualsToken):
            self._next_token()
            node = Node(NodeType.Set, children=[node, self.expr()])
        return node

    def paren_expr(self):
        if not (isinstance(self.token, tt.DelimiterToken) and self.token.value == '('):
            self.expected_token_error('(', self.token.value, self.token.line, self.token.position)
        self._next_token()
        node = self.expr()
        if not (isinstance(self.token, tt.DelimiterToken) and self.token.value == ')'):
            self.expected_token_error(')', self.token.value, self.token.line, self.token.position)
        self._next_token()
        return node

    def statement(self):
        if isinstance(self.token, tt.KeywordToken) and self.token.value == 'if':
            node = Node(NodeType.If)
            self._next_token()
            if_condition = self.paren_expr()
            if not isinstance(self.token, tt.ColonToken):
                prev_token = self.tokens[self.token_index - 1]
                self.error("':' excepted at line {}, position {}"
                           .format(prev_token.line, prev_token.position))
            self._next_token()
            if not isinstance(self.token, tt.EndlineToken):
                prev_token = self.tokens[self.token_index - 1]
                self.error("Body of the 'if' block cannot be on line (line {})"
                           .format(prev_token.line))
            self._next_token()

            if_body = self.block()

            node.children = [if_condition, if_body]

            if self.lexer.sym == isinstance(self.token, tt.KeywordToken) and \
                    self.token.value == 'else':
                node.kind = NodeType.IfWithElse
                self._next_token()
                node.children.append(self.block())
        elif isinstance(self.token, tt.KeywordToken) and self.token.value == 'while':
            node = Node(NodeType.While)
            self._next_token()

            while_condition = self.paren_expr()

            if not isinstance(self.token, tt.ColonToken):
                prev_token = self.tokens[self.token_index - 1]
                self.error("':' expected at line {}, position {}"
                           .format(prev_token.line, prev_token.position))
            self._next_token()
            if not isinstance(self.token, tt.EndlineToken):
                prev_token = self.tokens[self.token_index - 1]
                self.error("Body of the 'while' block cannot be on line (line {})"
                           .format(prev_token.line))
            self._next_token()

            while_body = self.block()

            node.children = [while_condition, while_body]
        else:
            node = Node(NodeType.Expr, children=[self.expr()])
            if not isinstance(self.token, tt.EndlineToken):
                prev_token = self.tokens[self.token_index - 1]
                self.error("Multiple statements at line {}".format(prev_token.line))
            self._next_token()
        return node

    def block(self):
        if isinstance(self.token, tt.IndentToken):
            node = Node(NodeType.Block)
            while True:
                self._next_token()
                if isinstance(self.token, tt.DedentToken) or \
                        isinstance(self.token, tt.EofToken):
                    return node
                node.children.append(self.statement())

    def program(self):
        node = Node(NodeType.Program)
        while True:
            if isinstance(self.token, tt.EofToken):
                return node
            statement = self.statement()
            node.children.append(copy.copy(statement))

    def parse(self):
        self.tokens = self.lexer.get_tokens()
        self._next_token()
        node = self.program()
        if not isinstance(self.token, tt.EofToken):
            self.error("Invalid statement syntax")
        return node

    def _next_token(self):
        self.token_index += 1
        self.token = self.tokens[self.token_index]