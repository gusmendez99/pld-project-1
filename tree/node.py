from tokenization.regex import OperatorRepr

"""
 Symbol & Expression (Compound Symbols) Nodes
"""

class SymbolNode:
    def __init__(self, symbol):
        self.symbol = symbol

    def __repr__(self):
        return f'{self.symbol}'

class CompoundNode():
    def __init__(self, x, y=None):
        self.x = x
        self.y = y

    def __repr__(self):
        if self.y != None:
            return f'{self.x}{self.y}'
        return f'{self.x}'

"""
 Operator Nodes
"""

class ConcatNode():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}{OperatorRepr.CONCAT}{self.y})'


class OrNode():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}{OperatorRepr.OR}{self.y})'


class KleeneNode():
    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return f'{self.x}{OperatorRepr.KLEENE}'


class PlusNode():
    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return f'{self.x}{OperatorRepr.PLUS}'


class NullableNode():
    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return f'{self.x}{OperatorRepr.NULLABLE}'


# Factory pattern
NODE_TYPES = {
    "symbol": SymbolNode,
    "expression": CompoundNode,
    "concat": ConcatNode,
    "or": OrNode,
    "kleene": KleeneNode,
    "plus": PlusNode,
    "nullable": NullableNode,
}

class NodeFactory(object):
    @staticmethod
    def create_node(node_type = "symbol", **kwargs):
        try:
            return NODE_TYPES[node_type.lower()](**kwargs)
        except Exception:
            return None
    