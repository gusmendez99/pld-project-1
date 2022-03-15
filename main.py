
from tokenization.tokenizer import Tokenizer
from tree.parser import TreeParser
from automata.nfa import NFA
from automata.dfa import DFA

RENDER_TO_PDF = True
INPUT_TEST = 'aaaabbb'
INPUT_REGEX = '(a|b)*a(a|b)(a|b)+'

def main():
    tokenizer = Tokenizer(INPUT_REGEX)
    tokens = tokenizer.get_tokens()
    parser = TreeParser(tokens)
    tree = parser.parse()
    # print('Parsed Tree: ', tree)

    # NFA (with Thompson)
    nfa = NFA(tree, tokenizer.symbols_stream, INPUT_TEST)
    
    nfa.simulate()
    print(f"NFA accepts input '{INPUT_TEST}'? ", nfa.regex_accept_status)

    if RENDER_TO_PDF:
        nfa.render_digraph()
        print('[OUT] NFA digraph generated!')

    # NFA to DFA
    dfa = DFA(tokenizer.symbols_stream, INPUT_TEST)
    dfa.from_NFA(nfa)
    dfa.simulate()
    print(f"DFA accepts input '{INPUT_TEST}'? ", dfa.regex_accept_status)

    if RENDER_TO_PDF:
        dfa.render_digraph()
        print('[OUT] DFA digraph generated!')


if __name__ == '__main__':
    main()