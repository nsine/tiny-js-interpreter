from js_parser.node_type import NodeType
from js_parser.checker import get_args, check
import subprocess
import re

class SemanticAnalyzer:
    def __init__(self, tree):
        self._root = tree
        self._variables = {}

        self._get_func_args_count = get_args
        self.check_internal = check

    def check(self):
        return self.check_internal(self._root)

    def check_internal(self, node):
        if len(node.children) == 0:
            self.add_variable_to_list(node)

            result = self._check_if_variable_declared(node)
            if result is not None:
                return result
            result = self._check_for_zero_division(node)
            if result is not None:
                return result
            result = self._check_function_args_count(node)
            if result is not None:
                return result
            result = self._check_types(node)
            if result is not None:
                return result

        for child in node.children:
            self.check_internal(child)

    def add_variable_to_list(self, node):
        if (node.kind == NodeType.Set):
            self._variables[node.value] = True
        return True

    def _check_if_variable_declared(self, node):
        if (node.kind == NodeType.Var):
            if (self._variables[node.value] is None):
                return 'Undefined variable \'{}\''.format(node.value)
        return True

    def _check_for_zero_division(self, node):
        if (node.kind == NodeType.Div):
            second_op = node.children[1]
            if (second_op == 0):
                return 'Division by zero'
        return None

    def _check_function_args_count(self, node):
        if node.kind == NodeType.Call or \
           node.kind == NodeType.DefaultFunction:

            if len(node.children[1]) != _get_func_args_count(node.children[0]):
                return 'No overload variant of "{}" matches argument types' \
                        .format(node.children[0])
        return None

    def _check_types(self, node):
        if node.kind in NodeType[
            Add, Sub, Mul, Div,
            Equals, NotEquals, Greater, Lower, GreaterEq, LowerEq
        ]:
            if node.childen[0].kind != node.children[1].kind:
                return 'Unsupported operand types for {} ("{}" and "{}")' \
                    .format(node.value, node.children[0].kind, node.children[1].kind)
        return None

