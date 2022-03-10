
from tokenization.tokenizer import Tokenizer
from tree.parser import TreeParser

def main():
    tokenizer = Tokenizer('a|b*')
    tokens = tokenizer.get_tokens()
    parser = TreeParser(tokens)
    tree = parser.parse()
    print('Tokens: ', tokens)
    print('Parsed Tree: ', tree)

if __name__ == '__main__':
    main()