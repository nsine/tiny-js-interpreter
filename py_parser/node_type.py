class NodeType:
    Expr, Block, Program, \
        Var, Set, \
        IntConst, FloatConst, StringConst, \
        Add, Sub, Mul, Div, \
        Equals, NotEquals, Greater, Lower, GreaterEq, LowerEq, \
        Point, \
        While, For, \
        If, IfWithElse, \
        DefaultFunction, \
        Attribute, Call, \
        Seq = range(27)


node_type_pretty = [
    'Expression', 'Block', 'Program',
    'Variable', 'Set',
    'Int constant', 'Float constant', 'String literal',
    'Add', 'Sub', 'Mul', 'Div',
    'Equals', 'NotEquals', 'Greater', 'Lower', 'GreaterEq', 'LowerEq', \
    'Point',
    'While', 'For',
    'If', 'IfWithElse',
    'DefaultFunction',
    'Attribute', 'Call',
    'Seq'
]
