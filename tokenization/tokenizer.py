from tokenization.regex import *

class Tokenizer:
    def __init__(self, line="", is_direct_tokenization = False):
        normalized_line = ''.join(line.split())
        # Special case: remove innecessary concat input symbol (you must know why...)
        normalized_line = normalized_line.replace(OperatorRepr.CONCAT.value, EMPTY)
        self.line = iter(normalized_line)
        self.symbols_stream = set()
        self.active_item = None

        # Just for direct tokenization
        self.is_direct_tokenization = is_direct_tokenization
        self.needs_par_surround = False

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
            if self.active_item not in SUPPORTED_ALPHABET and self.active_item not in SUPPORTED_OPERATORS:
                raise Exception(f"Read a unrecognized token, please check your input...")

            # Validate tokens
            if self.active_item in SUPPORTED_ALPHABET:
                self.add_active_to_symbols_stream()

                # Surround with parenthesis
                if not self.is_direct_tokenization:
                    tokens.append(Token(Operator.L_PAR, OperatorRepr.L_PAR))
                tokens.append(Token(Operator.SYMBOL, self.active_item))

                # Move to read the following symbol
                self.move_reader()

                # Surround with parenthesis
                if self.is_direct_tokenization:
                    # Add token if needed
                    if self.active_item and (
                        self.active_item == OperatorRepr.L_PAR or self.active_item in SUPPORTED_ALPHABET
                    ):
                        tokens.append(Token(Operator.CONCAT))

                else:
                    par_surround = False

                    while self.active_item and (self.active_item in SUPPORTED_ALPHABET or self.active_item in SPECIAL_OPERATORS):
                        if self.active_item == OperatorRepr.KLEENE:
                            tokens.append(Token(Operator.KLEENE, OperatorRepr.KLEENE))
                            tokens.append(Token(Operator.R_PAR, OperatorRepr.R_PAR))
                            par_surround = True
                        elif self.active_item == OperatorRepr.PLUS:
                            tokens.append(Token(Operator.PLUS, OperatorRepr.PLUS))
                            tokens.append(Token(Operator.R_PAR, OperatorRepr.R_PAR))
                            par_surround = True
                        elif self.active_item == OperatorRepr.NULLABLE:
                            tokens.append(Token(Operator.NULLABLE, OperatorRepr.NULLABLE))
                            tokens.append(Token(Operator.R_PAR, OperatorRepr.R_PAR))
                            par_surround = True
                        elif self.active_item in SUPPORTED_ALPHABET:
                            self.add_active_to_symbols_stream()
                            tokens.append(Token(Operator.CONCAT))
                            tokens.append(Token(Operator.SYMBOL, self.active_item))
                        
                        # Move again to read the following symbol
                        self.move_reader()

                        if self.active_item and self.active_item == OperatorRepr.L_PAR and par_surround:
                            # Means there is a concat operation
                            tokens.append(Token(Operator.CONCAT))

                    if self.active_item and self.active_item == OperatorRepr.L_PAR and not par_surround: 
                        tokens.append(Token(Operator.R_PAR, OperatorRepr.R_PAR))
                        tokens.append(Token(Operator.CONCAT))
                    elif not par_surround:
                        tokens.append(Token(Operator.R_PAR, OperatorRepr.R_PAR))
            
            elif self.active_item == OperatorRepr.OR:
                self.move_reader()
                tokens.append(Token(Operator.OR))

                if self.is_direct_tokenization:
                    if self.active_item and not (
                        self.active_item == OperatorRepr.L_PAR or self.active_item == OperatorRepr.R_PAR
                    ):
                        tokens.append(Token(Operator.L_PAR))

                        while self.active_item and (
                            self.active_item != OperatorRepr.L_PAR or self.active_item not in SPECIAL_OPERATORS
                        ):
                            if self.active_item in SUPPORTED_ALPHABET:
                                self.add_active_to_symbols_stream()
                                tokens.append(Token(Operator.SYMBOL, self.active_item))

                                self.move_reader()
                                if self.active_item and (
                                    self.active_item in SUPPORTED_ALPHABET or self.active_item == Operator.L_PAR
                                ):
                                    tokens.append(Token(Operator.CONCAT))

                        if self.active_item and self.active_item in SPECIAL_OPERATORS:
                            self.needs_par_surround = True
                        else:
                            tokens.append(Token(Operator.R_PAR))

            elif self.active_item == OperatorRepr.L_PAR:
                self.move_reader()
                tokens.append(Token(Operator.L_PAR))

            elif self.active_item == OperatorRepr.R_PAR or self.active_item in SPECIAL_OPERATORS:
                if self.active_item == OperatorRepr.R_PAR:
                    self.move_reader()
                    tokens.append(Token(Operator.R_PAR))
                elif self.active_item == OperatorRepr.KLEENE:
                    self.move_reader()
                    tokens.append(Token(Operator.KLEENE))
                elif self.active_item == OperatorRepr.PLUS:
                    self.move_reader()
                    tokens.append(Token(Operator.PLUS))
                elif self.active_item == OperatorRepr.NULLABLE:
                    self.move_reader()
                    tokens.append(Token(Operator.NULLABLE))
                
                elif self.is_direct_tokenization and self.needs_par_surround:
                    tokens.append(Token(Operator.R_PAR))
                    self.needs_par_surround = False
                
                if self.active_item and (self.active_item in SUPPORTED_ALPHABET or self.active_item == OperatorRepr.L_PAR):
                    tokens.append(Token(Operator.CONCAT))

        
        if self.is_direct_tokenization:
            tokens.append(Token(Operator.CONCAT))
            tokens.append(Token(Operator.SYMBOL, END_SYMBOL))
        return tokens
