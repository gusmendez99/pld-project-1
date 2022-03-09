from regex import *

class Tokenizer:
    def __init__(self, line):
        normalized_line = ''.join(line.split())
        self.line = iter(normalized_line)
        self.symbols_stream = set()
        self.active_item = None
        # First step, move to position 0
        self.move_reader()

    def move_reader(self):
        """ Use this function to change the buffer input position """
        try:
            self.active_item = next(self.line)
        except Exception:
            self.active_item = None

    def add_active_to_symbols_stream(self):
        self.symbols_stream.add(self.active_item)

    def get_tokens(self):
        tokens = []

        while self.active_item:
            # Check if char is in supported alphabet
            print('Element: ', self.active_item)
            if self.active_item not in SUPPORTED_ALPHABET:
                raise Exception(f"Read a unrecognized token, please check your input...")

            # Validate tokens
            if self.active_item in SUPPORTED_ALPHABET:
                self.add_active_to_symbols_stream()
                # Surround with parenthesis
                tokens.append(Token(Operator.L_PAR))
                tokens.append(Token(Operator.SYMBOL, self.active_item))

                # Move to read the following symbol
                self.move_reader()
                par_surround = False

                while self.active_item and self.active_item in SUPPORTED_ALPHABET:
                    if self.active_item == Operator.KLEENE:
                        tokens.append(Token(Operator.KLEENE))
                        tokens.append(Token(Operator.R_PAR))
                        par_surround = True
                    # TODO: Support to PLUS and QUESTION operators
                    elif self.active_item == Operator.SYMBOL:
                        self.add_active_to_symbols_stream
                        tokens.append(Token(Operator.CONCAT))
                        tokens.append(Token(Operator.SYMBOL, self.active_item))
                    
                    # Move again to read the following symbol
                    self.move_reader()

                    if self.active_item and self.active_item == Operator.L_PAR and par_surround:
                        # Means there is a concat operation
                        tokens.append(Token(Operator.CONCAT))

                if self.active_item and self.active_item == Operator.L_PAR and not par_surround: 
                    tokens.append(Token(Operator.R_PAR))
                    tokens.append(Token(Operator.CONCAT))
                elif not par_surround:
                    tokens.append(Token(Operator.R_PAR))
            
            elif self.active_item == Operator.OR:
                self.move_reader()
                tokens.append(Token(Operator.OR))

            elif self.active_item == Operator.L_PAR:
                self.move_reader()
                tokens.append(Token(Operator.L_PAR))

            # TODO: Support PLUS and QUESTION operators

        return tokens


if __name__ == '__main__':
    tokenizer = Tokenizer('a')
    print(tokenizer.get_tokens())
    print(tokenizer.symbols_stream)
