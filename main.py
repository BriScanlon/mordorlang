from lexer.lexer import Lexer
from parser.parser import Parser

def main(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    lexer = Lexer(code)
    parser = Parser(lexer)
    ast = parser.parse()
    for i, expr in enumerate(ast, 1):
        print(f"AST for expression {i}: {expr}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python src/main.py <source_file.mordor>")
    else:
        main(sys.argv[1])
