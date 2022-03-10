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
    


"""
 Tree Nodes for DFA & RegexDFA
"""

class VisitorNode:
    def __init__(self, state, next_states):
        self.state = state
        self.has_been_visited = False
        self.next_states = next_states

    def __repr__(self):
        return f"""
            state: {self.state}
            -------------------------------
            -> visited?: {self.has_been_visited}
            -> next state(s): {self.next_states}'
        """
class RegexDFANode:
    def __init__(self, id, first_pos=None, last_pos=None, nullable=False, value=None, c1=None, c2=None):
        self.id = id
        self.first_pos = first_pos
        self.last_pos = last_pos
        self.follow_pos = []
        self.nullable = nullable
        self.value = value
        self.c1 = c1
        self.c2 = c2

    def __repr__(self):
        return f"""
            value: ({self.id}, {self.value})
            ---------------------------------
            -> first_pos: {self.first_pos}
            -> last_pos: {self.last_pos}
            -> follow_pos: {self.follow_pos}
            -> nullabe: {self.nullable}
        """