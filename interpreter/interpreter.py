from js_lexer.js_lexer import JsLexer
from js_parser.js_parser import JsParser

from js_parser.exceptions.js_parser_error import JsParserError
from js_lexer.js_lexer_error import JsLexerError
from js_parser import NodeType
from .errors import JsRuntimeError, JsUndeclaredVariableError
from interpreter.scope import Scope
from interpreter.default_functions import default_functions
from .types import JsString, JsNumber, JsArray, JsBoolean, JsObject, JsUndefined

class Interpreter:
    def __init__(self, program_text):
        self.js_lexer = JsLexer(program_text)
        self.parser = JsParser(self.js_lexer)

    def execute(self):
        try:
            syntax_tree = self.parser.parse()

            scope = Scope()

            self._execute_node(syntax_tree, scope)
        except (JsParserError, JsLexerError) as err:
            return {
                'success': False,
                'error': str(err)
            }

    def _execute_node(self, node, scope):
        if node.kind == NodeType.Program:
            return self._execute_program(node, scope)
        elif node.kind == NodeType.Expr:
            return self._execute_expression(node, scope)
        elif node.kind == NodeType.Block:
            return self._execute_block(node, Scope(scope))
        elif node.kind == NodeType.If:
            return self._execute_if_statement(node, scope)
        elif node.kind == NodeType.IfWithElse:
            return self._execute_if_with_else_statement(node, scope)
        elif node.kind == NodeType.For:
            return self._execute_for_statement(node, scope)
        elif node.kind == NodeType.While:
            return self._execute_while_statement(node, scope)
        elif node.kind == NodeType.Decl:
            return self._execute_declaration_statement(node, scope)
        elif node.kind == NodeType.Set:
            return self._execute_assignment_statement(node, scope)
        elif node.kind == NodeType.DefaultFunction:
            pass
        elif node.kind == NodeType.Call:
            return self._execute_call(node, scope)
        elif node.kind == NodeType.StringConst:
            return self._execute_string(node)
        elif node.kind == NodeType.IntConst:
            return self._execute_int(node)
        elif node.kind == NodeType.FloatConst:
            return self._execute_float(node)
        elif node.kind == NodeType.ArrayConst:
            return self._execute_array(node, scope)

    def _execute_string(self, node):
        return JsString(node.value)

    def _execute_int(self, node):
        return JsNumber(int(node.value))

    def _execute_float(self, node):
        return JsNumber(float(node.value))

    def _execute_array(self, node, scope):
        arr_items = [self._execute_node(arr_item_node, scope) for arr_item_node in node.children[0].children]
        return JsArray(arr_items)

    def _execute_call(self, node, scope):
        callable_object = node.children[0]

        argument_nodes = node.children[1].children

        arguments = None
        if argument_nodes is not None:
            arguments = [self._execute_node(arg_node, scope) for arg_node in argument_nodes]

        if callable_object.kind == NodeType.DefaultFunction:
            if callable_object.value not in default_functions:
                raise JsRuntimeError('Undeclared function', callable_object.position)
            default_functions[callable_object.value](arguments)

    def _execute_assignment_statement(self, node, scope):
        variable_name = node.children[0].value

        variable_data = self._execute_node(node.children[1], scope)
        success = scope.update_variable(variable_name, variable_data)

        if not success:
            raise JsUndeclaredVariableError(variable_name, node.position)

    def _execute_declaration_statement(self, node, scope):
        variable_name = node.children[0].value

        is_var_added = scope.add_variable_if_not_exists(variable_name)
        if not is_var_added:
            raise JsRuntimeError('Undeclared variable {}'.format(variable_name), node.position)

        init_node = node.children[1]

        # Check what node creates when no initialization
        if not init_node.kind == NodeType.Var:
            init_data = self._execute_node(init_node, scope)
            scope.update_variable(variable_name, init_data)

    def _execute_while_statement(self, node, scope):
        new_scope = Scope(scope)

        while True:
            condition_satisfied = self._execute_node(node.children[0], new_scope)
            if condition_satisfied:
                self._execute_node(node.children[1], new_scope)
            else:
                break

    def _execute_for_statement(self, node, scope):
        new_scope = Scope(scope)

        self._execute_node(node.children[0], new_scope)
        while True:
            condition_satisfied = self._execute_node(node.children[1], new_scope)
            if condition_satisfied:
                self._execute_node(node.children[3], new_scope)
                self._execute_node(node.children[2], new_scope)
            else:
                break

    def _execute_if_statement(self, node, scope):
        condition_satisfied = self._execute_node(node.children[0], scope)
        if condition_satisfied:
            self._execute_node(node.children[1], scope)

    def _execute_if_with_else_statement(self, node, scope):
        condition_satisfied = self._execute_node(node.children[0], scope)
        if condition_satisfied:
            self._execute_node(node.children[1], scope)
        else:
            self._execute_node(node.children[2], scope)

    def _execute_program(self, node, scope):
        for child in node.children:
            self._execute_node(child, scope)

    def _execute_expression(self, node, scope):
        self._execute_node(node.children[0], scope)

    def _execute_block(self, node, scope):
        new_scope = Scope(scope)
        for child in node.children:
            self._execute_node(node, new_scope)
