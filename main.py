
from tokenization.tokenizer import Tokenizer
from tree.parser import TreeParser

def main():
    tokenizer = Tokenizer('a|b*')
    parser = TreeParser(tokenizer.get_tokens())
    tree = parser.parse()
    print(tree)

if __name__ == '__main__':
    main()