class Node(object):
    def __init__(self, kind, value=None, op1=None, op2=None, op3=None):
        self._kind = kind
        self._value = value
        self._op1 = op1
        self._op2 = op2
        self._op3 = op3