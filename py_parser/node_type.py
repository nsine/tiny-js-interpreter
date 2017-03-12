class NodeType:
    Expr, Block, Program, \
        Var, Set, \
        IntConst, FloatConst, StringConst, ArrayConst, \
        Add, Sub, Mul, Div, \
        Equals, NotEquals, Greater, Lower, GreaterEq, LowerEq, \
        Point, ByIndex, \
        While, For, \
        If, IfWithElse, \
        DefaultFunction, \
        Attribute, Call, \
        Seq = range(29)


node_type_pretty = [
    'Expression', 'Block', 'Program',
    'Variable', 'Assignment',
    'IntLiteral', 'FloatLiteral', 'StringLiteral', 'ArrayLiteral',
    'Add', 'Sub', 'Mul', 'Div',
    'Equals', 'NotEquals', 'Greater', 'Lower', 'GreaterEq', 'LowerEq',
    'Point', 'ByIndex',
    'While', 'For',
    'If', 'IfWithElse',
    'DefaultFunction',
    'Attribute', 'Call',
    'Sequence'
]
