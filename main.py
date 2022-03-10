
from tokenization.tokenizer import Tokenizer
from tree.parser import TreeParser
from automata.nfa import NFA

def main():
    regex_input = 'a|b*'
    tokenizer = Tokenizer(regex_input)
    tokens = tokenizer.get_tokens()
    parser = TreeParser(tokens)
    tree = parser.parse()
    nfa_test = NFA(tree, tokenizer.symbols_stream, regex_input)
    
    print('Tokens: ', tokens)
    print('Parsed Tree: ', tree)
    print('NFA: ', nfa_test)


if __name__ == '__main__':
    main()