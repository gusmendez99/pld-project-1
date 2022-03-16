from enum import Enum
from string import ascii_letters, digits

# Extras
EPSILON = 'e' # We can't print unicode 'ɛ'... 
END_SYMBOL = '#'
EMPTY = ''

class Operator(Enum):
    """ Map every op with its own precedence """
    R_PAR = 7
    L_PAR = 6
    NULLABLE = 5
    PLUS = 4
    KLEENE = 3
    OR = 2
    CONCAT = 1
    SYMBOL = 0

class OperatorRepr(Enum):
    R_PAR = ")"
    L_PAR = "("
    NULLABLE = '?'
    PLUS = '+'
    KLEENE = "*"
    OR = "|"
    CONCAT = "."

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other
        
        try:
            return str(self.value) == str(other)
        except:
            pass
        return NotImplemented

    def __str__(self):
        return self.value
    

# Language support (Question: do we need to include epsilon? idk)
# Use class conventions: [a-z] + [A-Z] + [0-9] + .
SUPPORTED_ALPHABET = ascii_letters + digits + '.'
SUPPORTED_OPERATORS = ''.join([e.value for e in OperatorRepr])
SPECIAL_OPERATORS = ''.join([OperatorRepr.KLEENE.value, OperatorRepr.PLUS.value, OperatorRepr.NULLABLE.value ])

class Token:
    """ Represent identified token, value must be None if it's an operator """
    def __init__(self, token_type: Operator, value=None):
        self.type = token_type
        self.value = value

    def get_precedence(self):
        return self.type.value

    def __repr__(self):
        return f'{self.type.name}: {self.value if self.value else OperatorRepr[self.type.name].value}'
