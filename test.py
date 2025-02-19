from lexer.lexer import Lexer

with open('examples/arithmetic.mordor') as f:
    code = f.read()
    
lexer = Lexer(code)
tolkiens = []

while True:
    tolkien = lexer.get_next_tolkien()
    tolkiens.append(tolkien)
    if tolkien.type == 'EOF':
        break
    
for tolkien in tolkiens:
    print(tolkien)