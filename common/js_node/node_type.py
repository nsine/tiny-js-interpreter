class NodeType:
    Expr, Block, Program, \
        Var, Set, \
        NumberConst, StringConst, ArrayConst, BooleanConst, Undefined, \
        Add, Sub, Mul, Div, Mod, \
        Equals, NotEquals, Greater, Lower, GreaterEq, LowerEq, \
        Point, ByIndex, \
        While, For, \
        If, IfWithElse, \
        DefaultFunction, \
        Attribute, Call, \
        Seq, Decl = range(32)


node_type_pretty = [
    'Expression', 'Block', 'Program',
    'Variable', 'Assignment',
    'NumberLiteral', 'StringLiteral', 'ArrayLiteral', 'BooleanConst', 'Undefined',
    'Add', 'Sub', 'Mul', 'Div', 'Mod',
    'Equals', 'NotEquals', 'Greater', 'Lower', 'GreaterEq', 'LowerEq',
    'Point', 'ByIndex',
    'While', 'For',
    'If', 'IfWithElse',
    'DefaultFunction',
    'Attribute', 'Call',
    'Sequence', 'Declaration'
]
