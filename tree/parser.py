"""
 Tree models
"""
from tokenization.regex import Operator
from tree.node import NodeFactory


class TreeParser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.active_token = None
        # First step, move to position 0
        self.move_token_reader()

    def move_token_reader(self):
        """ Use this function to change the buffer token position """
        try:
            self.active_token = next(self.tokens)
        except Exception:
            self.active_token = None

    def parse(self):
        return None if not self.active_token else self.extract_expression()

    def extract_symbol(self):
        temp_token = self.active_token
        if temp_token.type == Operator.L_PAR:
            self.move_token_reader()
            expr = self.extract_expression()

            if self.active_token.type != Operator.R_PAR:
                raise Exception("Parenthesis issue! I'm not able to return a valid symbol...")

            # Set the new active token & return current expr
            self.move_token_reader()
            return expr

        elif temp_token.type == Operator.SYMBOL:
            self.move_token_reader()
            return NodeFactory.create_node(node_type="symbol", symbol=temp_token.value)

    def extract_expression(self):
        operator = self.extract_operator()

        while self.active_token and self.active_token.type in (
            Operator.OR, Operator.CONCAT
        ):
            if self.active_token.type == Operator.OR:
                self.move_token_reader()
                operator = NodeFactory.create_node(node_type="or", x=operator, y=self.extract_operator())
            elif self.active_token.type == Operator.CONCAT:
                self.move_token_reader()
                operator = NodeFactory.create_node(node_type="concat", x=operator, y=self.extract_operator())
        
        return operator
    
    def extract_operator(self):
        symbol = self.extract_symbol()

        while self.active_token and self.active_token.type in (
            Operator.KLEENE, Operator.PLUS, Operator.NULLABLE
        ):
            if self.active_token.type == Operator.KLEENE:
                self.move_token_reader()
                symbol = NodeFactory.create_node("kleene", x=symbol)
            elif self.active_token.type == Operator.NULLABLE:
                self.move_token_reader()
                symbol = NodeFactory.create_node("nullable", x=symbol)
            else:
                self.move_token_reader()
                symbol = NodeFactory.create_node("plus", x=symbol)
        return symbol
