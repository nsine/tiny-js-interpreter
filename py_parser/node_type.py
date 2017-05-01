class NodeType:
    Expr, Block, Program, \
        Var, Set, \
        IntConst, FloatConst, StringConst, ArrayConst, Undefined, \
        Add, Sub, Mul, Div, \
        Equals, NotEquals, Greater, Lower, GreaterEq, LowerEq, \
        Point, ByIndex, \
        While, For, \
        If, IfWithElse, \
        DefaultFunction, \
        Attribute, Call, \
        Seq, Decl = range(31)


node_type_pretty = [
    'Expression', 'Block', 'Program',
    'Variable', 'Assignment',
    'IntLiteral', 'FloatLiteral', 'StringLiteral', 'ArrayLiteral', 'Undefined'
    'Add', 'Sub', 'Mul', 'Div',
    'Equals', 'NotEquals', 'Greater', 'Lower', 'GreaterEq', 'LowerEq',
    'Point', 'ByIndex',
    'While', 'For',
    'If', 'IfWithElse',
    'DefaultFunction',
    'Attribute', 'Call',
    'Sequence', 'Declaration'
]
