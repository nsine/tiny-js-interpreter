from js_lexer.js_lexer import JsLexer
from js_parser.js_parser import JsParser

from js_parser.errors import JsParserError
from js_lexer.js_lexer_error import JsLexerError
from common.js_node import NodeType
from .errors import JsRuntimeError, JsUndeclaredVariableError
from .scope import Scope
from .default_functions import default_functions
from .types import JsString, JsNumber, JsArray, JsBoolean, JsObject, JsUndefined

class JsExecutor:
    def __init__(self, program_text):
        self.js_lexer = JsLexer(program_text)
        self.parser = JsParser(self.js_lexer)

        self.executors = { }
        self._init_executors()

    def _init_executors(self):
        self.executors[NodeType.Program] = self._execute_program
        self.executors[NodeType.Expr] = self._execute_expression
        self.executors[NodeType.Block] = self._execute_block
        self.executors[NodeType.If] = self._execute_if_statement
        self.executors[NodeType.IfWithElse] = self._execute_if_with_else_statement
        self.executors[NodeType.For] = self._execute_for_statement
        self.executors[NodeType.While] = self._execute_while_statement
        self.executors[NodeType.Decl] = self._execute_declaration_statement
        self.executors[NodeType.Set] = self._execute_assignment_statement
        self.executors[NodeType.Call] = self._execute_call
        self.executors[NodeType.IntConst] = self._execute_int
        self.executors[NodeType.StringConst] = self._execute_string
        self.executors[NodeType.ArrayConst] = self._execute_array
        self.executors[NodeType.Var] = self._execute_var
        self.executors[NodeType.Undefined] = self._execute_undefined
        self.executors[NodeType.BooleanConst] = self._execute_boolean
        self.executors[NodeType.Add] = self._execute_add
        self.executors[NodeType.Sub] = self._execute_sub
        self.executors[NodeType.Mul] = self._execute_mul
        self.executors[NodeType.Div] = self._execute_div
        self.executors[NodeType.Mod] = self._execute_mod
        self.executors[NodeType.Equals] = self._execute_equals
        self.executors[NodeType.NotEquals] = self._execute_not_equals
        self.executors[NodeType.Greater] = self._execute_greater
        self.executors[NodeType.Lower] = self._execute_lower
        self.executors[NodeType.GreaterEq] = self._execute_greater_equals
        self.executors[NodeType.LowerEq] = self._execute_lower_equals
        self.executors[NodeType.Attribute] = self._execute_attribute
        self.executors[NodeType.ByIndex] = self._execute_by_index

    def execute(self):
        try:
            syntax_tree = self.parser.parse()

            scope = Scope()

            self._execute_node(syntax_tree, scope)
            return {
                'success': True
            }
        except (JsParserError, JsLexerError, JsRuntimeError) as err:
            return {
                'success': False,
                'error': str(err)
            }

    def _execute_node(self, node, scope):
        return self.executors[node.kind](node, scope)

    def _execute_by_index(self, node, scope):
        variable = self._execute_node(node.children[0], scope)
        index = self._execute_node(node.children[1], scope)

        return variable._js_by_index(index)

    def _execute_attribute(self, node, scope):
        variable = self._execute_node(node.children[0], scope)
        if node.value not in variable.properties:
            raise JsRuntimeError(
                '{} has no method or property {}'
                .format(node.children[0].value, node.value), node.position
            )
        return variable.properties[node.value]

    def _execute_equals(self, node, scope):
        operand1 = self._execute_node(node.children[0], scope)
        operand2 = self._execute_node(node.children[1], scope)

        return operand1 == operand2

    def _execute_not_equals(self, node, scope):
        operand1 = self._execute_node(node.children[0], scope)
        operand2 = self._execute_node(node.children[1], scope)

        return operand1 != operand2

    def _execute_lower(self, node, scope):
        operand1 = self._execute_node(node.children[0], scope)
        operand2 = self._execute_node(node.children[1], scope)

        return operand1 < operand2

    def _execute_lower_equals(self, node, scope):
        operand1 = self._execute_node(node.children[0], scope)
        operand2 = self._execute_node(node.children[1], scope)

        return operand1 <= operand2

    def _execute_greater(self, node, scope):
        operand1 = self._execute_node(node.children[0], scope)
        operand2 = self._execute_node(node.children[1], scope)

        return operand1 > operand2

    def _execute_greater_equals(self, node, scope):
        operand1 = self._execute_node(node.children[0], scope)
        operand2 = self._execute_node(node.children[1], scope)

        return operand1 >= operand2

    def _execute_mod(self, node, scope):
        operand1 = self._execute_node(node.children[0], scope)
        operand2 = self._execute_node(node.children[1], scope)

        return operand1 % operand2

    def _execute_add(self, node, scope):
        operand1 = self._execute_node(node.children[0], scope)
        operand2 = self._execute_node(node.children[1], scope)

        return operand1 + operand2

    def _execute_sub(self, node, scope):
        operand1 = self._execute_node(node.children[0], scope)
        operand2 = self._execute_node(node.children[1], scope)

        return operand1 - operand2

    def _execute_mul(self, node, scope):
        operand1 = self._execute_node(node.children[0], scope)
        operand2 = self._execute_node(node.children[1], scope)

        return operand1 * operand2

    def _execute_div(self, node, scope):
        operand1 = self._execute_node(node.children[0], scope)
        operand2 = self._execute_node(node.children[1], scope)

        return operand1 / operand2

    def _execute_boolean(self, node, scope):
        if node.value == 'true':
            return JsBoolean(True)
        elif node.value == 'false':
            return JsBoolean(False)
        else:
            raise Exception('Something went wrong')

    def _execute_undefined(self, scope):
        return JsUndefined()

    def _execute_var(self, node, scope):
        variable_data = scope.get_variable(node.value)
        if variable_data is None:
            raise JsUndeclaredVariableError(node.value, node.position)
        else:
            return variable_data

    def _execute_string(self, node, scope):
        return JsString(node.value)

    def _execute_int(self, node, scope):
        return JsNumber(int(node.value))

    def _execute_float(self, node, scope):
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

        if len(arguments) > 0 and isinstance(arguments[0], JsUndefined):
            print()

        if callable_object.kind == NodeType.DefaultFunction:
            if callable_object.value not in default_functions:
                raise JsRuntimeError('Undeclared function', callable_object.position)
            try:
                return default_functions[callable_object.value](arguments)
            except JsRuntimeError as err:
                err.position = callable_object.position
                raise
        elif callable_object.kind == NodeType.Attribute:
            prop = self._execute_node(callable_object, scope)
            if not callable(prop):
                raise JsRuntimeError('{} is not callable'.format(callable_object.value), callable_object.position)
            return prop(arguments)

    def _execute_assignment_statement(self, node, scope):
        variable_name = node.children[0].value

        variable_data = self._execute_node(node.children[1], scope)
        success = scope.update_variable(variable_name, variable_data)

        if not success:
            raise JsUndeclaredVariableError(variable_name, node.position)

        return variable_data

    def _execute_declaration_statement(self, node, scope):
        variable_name = node.children[0].value

        is_var_added = scope.add_variable_if_not_exists(variable_name)
        if not is_var_added:
            raise JsRuntimeError('Variable {} already declared'
                                 .format(variable_name), node.position)

        init_node = node.children[1]

        # Check if initialization is here
        if not init_node.kind == NodeType.Var:
            init_data = self._execute_node(init_node, scope)

        return JsUndefined()

    def _execute_while_statement(self, node, scope):
        new_scope = Scope(scope)

        while True:
            condition_satisfied = self._execute_node(node.children[0], new_scope)._js_to_boolean().value
            if condition_satisfied:
                self._execute_node(node.children[1], new_scope)
            else:
                break

    def _execute_for_statement(self, node, scope):
        new_scope = Scope(scope)

        self._execute_node(node.children[0], new_scope)
        while True:
            condition_satisfied = self._execute_node(node.children[1],
                new_scope)._js_to_boolean().value
            if condition_satisfied:
                self._execute_node(node.children[3], new_scope)
                self._execute_node(node.children[2], new_scope)
            else:
                break

    def _execute_if_statement(self, node, scope):
        condition_satisfied = self._execute_node(node.children[0], scope)._js_to_boolean().value
        if condition_satisfied:
            self._execute_node(node.children[1], scope)

    def _execute_if_with_else_statement(self, node, scope):
        condition_satisfied = self._execute_node(node.children[0], scope)._js_to_boolean().value
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
            self._execute_node(child, new_scope)
