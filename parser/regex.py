from enum import Enum
from string import ascii_lowercase, ascii_uppercase, digits

# Extras
EPSILON = 'ε'
END_SYMBOL = '#'

class Operator(Enum):
    """ Map every op with its own precedence """
    R_PAR = 5
    L_PAR = 4
    KLEENE = 3
    OR = 2
    CONCAT = 1
    SYMBOL = 0

class OperatorRepr(Enum):
    R_PAR = ")"
    L_PAR = "("
    KLEENE = "*"
    PLUS = '+'
    QUESTION = '?'
    OR = "|"
    CONCAT = "°"


# Language support (Question: do we need to include epsilon? idk)
SUPPORTED_ALPHABET = ascii_lowercase + ascii_uppercase + digits + (
    ''.join([e.value for e in OperatorRepr])
)

class Token:
    """ Represent identified token, value must be None if it's an operator """
    def __init__(self, token_type: Operator, value=None):
        self.type = token_type
        self.value = value

    def get_precedence(self):
        return self.type.value

    def __repr__(self):
        return f'{self.type.name}: {self.value if self.value else Operator[self.type.name].value}'

# TODO: Evaluate & replece if not needed...
class RegularExpression:
    def __init__(self, regex):
        self.regex = regex

    def thompson_construction(self):
        """ parse regex to NFA """
        self.insert_concat_symbol()
        regular_expr = self.parse_infix_to_postfix()
        # TODO: parse regex from infix to postfix

    def is_symbol(char):
        """ checks if the character is a symbol and not an operator """
        # return char not in OPERATOR_PRIORITIES.keys()
        pass

    def insert_concat_symbol(self):
        """ TODO: add concar symbol """
        pass

    def parse_infix_to_postfix(self):
        """ TODO: postfix form of the expression """
        pass

    def create_tree_representation(self):
        """ TODO: implement tree parsing method """
        pass

    def create_automaton(self):
        """ TODO: project requirement, parse tree of regex to a DFA repr """
        pass
