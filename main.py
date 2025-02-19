from lexer.lexer import Lexer
from parser.parser import Parser
from interpreter.interpreter import Interpreter

def main(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    # Lexing, Parsing, Interpreting
    lexer = Lexer(code)
    parser = Parser(lexer)
    ast = parser.parse()

    interpreter = Interpreter()
    for i, expr in enumerate(ast, 1):
        result = interpreter.visit(expr)
        print(f"Result for expression {i}: {result}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python src/main.py <source_file.mordor>")
    else:
        main(sys.argv[1])
