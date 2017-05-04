import re

import common.js_token.token_types as tt
from common.js_node import JsNode, NodeType
from common import PositionInFile
from .errors import UnexpectedTokenError, JsParserError, ExpectedButFoundTokenError

class JsParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = []
        self.token_index = -1
        self.token = None

    def callable(self, source_node):
        return JsNode(NodeType.Call, children=[source_node, self.sequence(')')])

    def attribute(self, source_node):
        if not isinstance(self.token, tt.IdentifierToken):
            raise ExpectedButFoundTokenError('attribute name', self.token.value, self.token.position)
        node = JsNode(NodeType.Attribute, self.token.value, children=[source_node], position=self.token.position)
        self._next_token()

        if (isinstance(self.token, tt.DelimiterToken) and self.token.value == '('):
            self._next_token()
            return self.callable(node)
        else:
            return node

    def sequence(self, end_seq_value):
        node = JsNode(NodeType.Seq)
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
                raise UnexpectedTokenError(self.token.value, self.token.position)

    def term(self):
        if isinstance(self.token, tt.DefaultFunctionToken):
            node = JsNode(NodeType.DefaultFunction, self.token.value, position=self.token.position)
            self._next_token()
            if isinstance(self.token, tt.DelimiterToken) and self.token.value == '(':
                self._next_token()
                node = self.callable(node)
            return node

        if isinstance(self.token, tt.DelimiterToken) and self.token.value == '[':
            self._next_token()
            return JsNode(NodeType.ArrayConst, children=[self.sequence(']')], position=self.token.position)

        if isinstance(self.token, tt.DelimiterToken) and self.token.value == '{':
            raise JsParserError(self.token.position, 'Objects are not supported :(')

        if isinstance(self.token, tt.KeywordToken) and (self.token.value == 'true' or self.token.value == 'false'):
            node = JsNode(NodeType.BooleanConst, self.token.value, position=self.token.position)
            self._next_token()
            return node

        if isinstance(self.token, tt.IdentifierToken):
            node = JsNode(NodeType.Var, self.token.value, position=self.token.position)
            self._next_token()

            if isinstance(self.token, tt.OperatorToken) and self.token.value == '.':
                self._next_token()
                node = self.attribute(node)
            elif isinstance(self.token, tt.DelimiterToken) and self.token.value == '(':
                self._next_token()
                node = self.callable(node)
            elif isinstance(self.token, tt.DelimiterToken) and self.token.value == '[':
                self._next_token()
                node = JsNode(NodeType.ByIndex, children=[node, self.expr()], position=self.token.position)
                if isinstance(self.token, tt.DelimiterToken) and self.token.value == ']':
                    self._next_token()
                else:
                    raise ExpectedButFoundTokenError(']', self.token.value, self.token.position)
            return node

        node_type = None
        node_value = self.token.value
        if isinstance(self.token, tt.IdentifierToken):
            node_type = NodeType.Var
        elif isinstance(self.token, tt.IntNumberToken):
            node_type = NodeType.IntConst
        elif isinstance(self.token, tt.FloatNumberToken):
            node_type = NodeType.FloatConst
        elif isinstance(self.token, tt.StringToken):
            node_type = NodeType.StringConst
            node_value = re.match(r'\'(.*)?\'', node_value).group(1)

        if node_type is not None:
            node = JsNode(node_type, node_value, position=self.token.position)
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
            raise UnexpectedTokenError(self.token.value, self.token.position)

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
                elif self.token.value == '%':
                    kind = NodeType.Mod
                else:
                    break
            else:
                break
            self._next_token()
            node = JsNode(kind, children=[node, self.term()], position=self.token.position)
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
            self._next_token()
            node = JsNode(kind, children=[node, self.math_expr()], position=self.token.position)
        return node

    def expr(self):
        if not isinstance(self.token, tt.IdentifierToken):
            return self.test()
        node = self.test()
        if node.kind == NodeType.Var and isinstance(self.token, tt.EqualsToken):
            self._next_token()
            node = JsNode(NodeType.Set, children=[node, self.expr()], position=self.token.position)
        return node

    def decl_expr(self):
        node = JsNode(NodeType.Decl, position=self.token.position)
        self._next_token()
        if not isinstance(self.token, tt.IdentifierToken):
            raise ExpectedButFoundTokenError('identifier', self.token.value, self.token.position)
        node.children.append(JsNode(NodeType.Var, self.token.value, position=self.token.position))

        var_init = self.expr_with_semicolon()
        node.children.append(var_init)
        return node

    def expr_with_semicolon(self):
        if isinstance(self.token, tt.KeywordToken) and self.token.value == 'var':
            return self.decl_expr()
        node = self.expr()
        if not isinstance(self.token, tt.SemicolonToken):
            raise ExpectedButFoundTokenError(';', self.token.value, self.token.position)
        self._next_token()
        return node

    def paren_expr(self):
        if not (isinstance(self.token, tt.DelimiterToken) and self.token.value == '('):
            raise ExpectedButFoundTokenError('(', self.token.value, self.token.position)
        self._next_token()
        node = self.expr()
        if not (isinstance(self.token, tt.DelimiterToken) and self.token.value == ')'):
            raise ExpectedButFoundTokenError(')', self.token.value, self.token.position)
        self._next_token()
        return node

    def if_statement(self):
        node = JsNode(NodeType.If, position=self.token.position)
        self._next_token()
        if_condition = self.paren_expr()
        if_body = self.block()

        node.children = [if_condition, if_body]

        if isinstance(self.token, tt.KeywordToken) and \
                self.token.value == 'else':
            node.kind = NodeType.IfWithElse
            self._next_token()
            node.children.append(self.block())

        return node

    def for_statement(self):
        node = JsNode(NodeType.For, position=self.token.position)
        self._next_token()

        if not (isinstance(self.token, tt.DelimiterToken) and self.token.value == '('):
            raise ExpectedButFoundTokenError('(', self.token.value, self.token.position)
        self._next_token()
        for_init = self.expr_with_semicolon()
        for_condition = self.expr_with_semicolon()
        for_step = self.expr()

        if not (isinstance(self.token, tt.DelimiterToken) and self.token.value == ')'):
            raise ExpectedButFoundTokenError(')', self.token.value, self.token.position)
        self._next_token()
        for_body = self.block()

        node.children = [for_init, for_condition, for_step, for_body]
        return node

    def while_statement(self):
        node = JsNode(NodeType.While, position=self.token.position)
        self._next_token()

        while_condition = self.paren_expr()
        while_body = self.block()

        node.children = [while_condition, while_body]
        return node

    def statement(self):
        if isinstance(self.token, tt.KeywordToken) and self.token.value == 'if':
            node = self.if_statement()
        elif isinstance(self.token, tt.KeywordToken) and self.token.value == 'while':
            node = self.while_statement()
        elif isinstance(self.token, tt.KeywordToken) and self.token.value == 'for':
            node = self.for_statement()
        else:
            node = JsNode(NodeType.Expr, children=[self.expr_with_semicolon()], position=self.token.position)
        return node

    def block(self):
        if isinstance(self.token, tt.DelimiterToken) and self.token.value == '{':
            node = JsNode(NodeType.Block, position=self.token.position)
            self._next_token()
            while True:
                if isinstance(self.token, tt.DelimiterToken) and self.token.value == '}':
                    self._next_token()
                    return node
                if isinstance(self.token, tt.EofToken):
                    raise JsParserError(None, 'Unexpected end of file')
                node.children.append(self.statement())

    def program(self):
        node = JsNode(NodeType.Program)
        while True:
            if isinstance(self.token, tt.EofToken):
                return node
            statement = self.statement()
            node.children.append(statement)

    def parse(self):
        self.tokens = self.lexer.get_tokens()
        self._next_token()
        node = self.program()
        if not isinstance(self.token, tt.EofToken):
            raise JsParserError(None, "Invalid syntax")
        return node

    def _next_token(self):
        self.token_index += 1
        self.token = self.tokens[self.token_index]
