
from tokenization.tokenizer import Tokenizer
from tree.parser import TreeParser
from automata.nfa import NFA
from automata.dfa import DFA

RENDER_TO_PDF = True

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
    
    nfa.simulate()
    print(f"NFA accepts input '{input_test}'? ", nfa.regex_accept_status)

    if RENDER_TO_PDF:
        nfa.render_digraph()
        print('[OUT] NFA digraph generated!')

    # NFA to DFA
    dfa = DFA(tokenizer.symbols_stream, input_test)
    dfa.from_NFA(nfa)
    dfa.simulate()
    print(f"DFA accepts input '{input_test}'? ", dfa.regex_accept_status)

    if RENDER_TO_PDF:
        dfa.render_digraph()
        print('[OUT] DFA digraph generated!')


if __name__ == '__main__':
    main()