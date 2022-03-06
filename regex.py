# Specify operator priorities
EPSILON = 'ε'
END_SYMBOL = '#'
OPERATOR_PRIORITIES = {
    '°' : 3,
    '|' : 2
    '(' : 1,
    ')' : 1,
    '*' : 0,
}

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
        return char not in OPERATOR_PRIORITIES.keys()

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
