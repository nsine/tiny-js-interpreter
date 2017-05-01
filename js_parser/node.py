from js_parser.node_type import node_type_pretty

class Node(object):
    def __init__(self, kind, value=None, children=None):
        self.kind = kind
        self.value = value

        self.position = {
            'line': 0,
            'position': 0
        }

        if children is None:
            self.children = []
        else:
            self.children = children

    def __str__(self):
        return self._str_with_indent(0)

    def _str_with_indent(self, indent):
        result = ''
        result += node_type_pretty[self.kind]
        if self.value is not None:
            result += '({})'.format(self.value)

        result += '\n'

        child_indent = '|-'
        child_strings = [((' ' * indent) + child_indent + child._str_with_indent(indent + 2))
                         for child in self.children]
        result += ''.join(child_strings)

        return result
