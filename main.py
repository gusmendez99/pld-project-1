
from tokenization.tokenizer import Tokenizer
from tree.parser import TreeParser
from automata.nfa import NFA

def main():
    regex_input = 'a|b*'
    tokenizer = Tokenizer(regex_input)
    tokens = tokenizer.get_tokens()
    parser = TreeParser(tokens)
    tree = parser.parse()
    print('Tokens: ', tokens)
    print('Parsed Tree: ', tree)

    input_test = 'abbb'

    # NFA (with Thompson)
    nfa = NFA(tree, tokenizer.symbols_stream, input_test)
    print('NFA: ', nfa)
    
    nfa.simulate()
    print(f"NFA accepts input '{input_test}'? ", nfa.regex_accept_status)
    nfa.render_digraph()
    print('NFA digraph generated!')

    # TODO: NFA to DFA


if __name__ == '__main__':
    main()