from lexer.lexer import Lexer
from parser.parser import Parser
from interpreter.interpreter import Interpreter

def main(file_path):
    # Read the source code
    with open(file_path, 'r') as file:
        code = file.read()

    # Lex the source code
    lexer = Lexer(code)
    # Parse the lexed tokens
    parser = Parser(lexer)
    # Parse the source code
    ast = parser.parse()
    # Interpret
    interpreter = Interpreter()
    # Visit the AST
    for i, expr in enumerate(ast, 1):
        interpreter.visit(expr)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python src/main.py <source_file.mordor>")
    else:
        main(sys.argv[1])
