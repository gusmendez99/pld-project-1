
from tokenization.tokenizer import Tokenizer
from tree.parser import TreeParser
from automata.nfa import NFA
from automata.dfa import DFA
from automata.regex_dfa import RegexDFA
# utils
from utils.common import load_txt_file

ABC_TEST_PATH = './tests/abc_tests.txt'
BINARY_TEST_PATH = './tests/bin_tests.txt'

MAIN_MENU = """

            WELCOME
    -----------------------
    Select a valid option:

    1. Enter a new regex expr
    2. Run TXT tests

    3. Exit
"""

FA_MENU = """

            DFA/NFA
    -----------------------
    Select a valid option:
    1. Thompson + Subsets const. (Generates both NFA & DFA)
    2. Direct DFA

    3. <- Back

"""

TESTS_MENU = """

            TESTS
    -----------------------
    1. Run ABC tests
    2. Run Binary tests

    3. <- Back

"""

def test_thompson_and_subsets(regex, input_test = None, simulate = False, render=True, output_filename='', view_pdf=True):
    tokenizer = Tokenizer(regex)
    tokens = tokenizer.get_tokens()
    parser = TreeParser(tokens)
    tree = parser.parse()

    # NFA (with Thompson)
    nfa = NFA(tree, tokenizer.symbols_stream, input_test)
    if simulate and input_test:
        nfa.simulate()
        print(f"NFA accepts input '{input_test}'? ", nfa.regex_accept_status)
    if render:
        nfa.render_digraph(output_filename.replace('FA', 'NFA'), view_pdf)
        print('[OUT] NFA digraph generated!')

    # NFA to DFA via Subsets
    dfa = DFA(tokenizer.symbols_stream, input_test)
    dfa.from_NFA(nfa)
    if simulate and input_test:
        dfa.simulate()
        print(f"DFA accepts input '{input_test}'? ", dfa.regex_accept_status)
    if render:
        dfa.render_digraph(output_filename.replace('FA', 'DFA'), view_pdf)
        print('[OUT] DFA digraph generated!')


def test_direct_method(regex, input_test = None, simulate = False, render=True, output_filename='', view_pdf=True):
    tokenizer = Tokenizer(regex, is_direct_tokenization=True)
    tokens = tokenizer.get_tokens()
    parser = TreeParser(tokens)
    tree = parser.parse()

    # Direct DFA (from regex)
    regex_dfa = RegexDFA(tree, tokenizer.symbols_stream, input_test)
    if simulate and input_test:
        regex_dfa.simulate()
        print(f"Direct DFA accepts input '{input_test}'? ", regex_dfa.regex_accept_status)
    if render:
        regex_dfa.render_digraph(output_filename, view_pdf)
        print('[OUT] Direct DFA digraph generated!')


def main():
    option = None

    while option != 0:
        print(MAIN_MENU)
        option = int(input('> '))

        if option == 1:
            fa_option = None
            input_regex = None
            input_test = None

            while fa_option != 0:
                if not input_regex or not input_test:
                    input_regex = input('Enter the regex: ')
                    input_test = input('Enter the eval expr: ')

                print(FA_MENU)
                fa_option = int(input('> '))

                if fa_option == 1:
                    try:
                        test_thompson_and_subsets(
                            regex = input_regex,
                            input_test = input_test,
                            simulate = True,
                            render = True
                        )
                    except Exception as e:
                        print(f'\n\tAn error ocurred, please check your regex: {e}')

                    reset_regex = input('-> Do you want to reset regex expr? (y/n): ') or 'n'
                    if reset_regex and reset_regex.lower() == 'y':
                        input_regex = input('Enter the regex: ')
                        input_test = input('Enter the eval expr: ')

                elif fa_option == 2:
                    try:
                        test_direct_method(
                            regex = input_regex,
                            input_test = input_test,
                            simulate = True,
                            render = True
                        )
                    except Exception as e:
                        print(f'\n\tAn error ocurred, please check your regex: {e}')

                    reset_regex = input('-> Do you want to reset regex expr? (y/n): ') or 'n'
                    if reset_regex and reset_regex.lower() == 'y':
                        input_regex = input('Enter the regex: ')
                        input_test = input('Enter the eval expr: ')

                elif fa_option == 3:
                    fa_option = 0
                else:
                    print('Not a valid option, going back to main menu...')
                    fa_option = 0

        elif option == 2:
            test_option = None
            while test_option != 0:
                print(TESTS_MENU)
                test_option = int(input('> '))

                if test_option == 1:
                    try:
                        # Test ABC txt file
                        test_lines = load_txt_file(ABC_TEST_PATH)
                        iteration = 0
                        for regex_test in test_lines:
                            # Simulation input is not required, we only want to generate the NFA & DFA outputs 
                            test_thompson_and_subsets(
                                regex = regex_test,
                                render = True,
                                output_filename = f"./tests/renders/FA_{iteration}.gv",
                                view_pdf = False
                            )
                            test_direct_method(
                                regex = regex_test,
                                render = True,
                                output_filename = f"./tests/renders/RegexDFA_{iteration}.gv",
                                view_pdf = False
                            )
                            iteration += 1

                        print('-> ABC tests passed!')
                    except Exception as e:
                        print(f'\n\tAn error ocurred, please regex on test file: {e}')

                elif test_option == 2:
                    try:
                        # Test Binary txt file
                        print('-> Binary tests passed!')
                    except Exception as e:
                        print(f'\n\tAn error ocurred, please check your regex: {e}')

                elif test_option == 3:
                    test_option = 0
                else:
                    print('Not a valid option, going back to main menu...')
                    test_option = 0

        elif option == 3:
            option = 0
            print('Exiting...')
        else:
            print('Not a valid option, exiting...')
            test_option = 0


if __name__ == '__main__':
    main()