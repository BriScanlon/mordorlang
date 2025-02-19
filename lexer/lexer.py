import re

# define our tokens/Tolkiens as constants

TOLKIEN_TYPES = {
    'NUMBER': 'NUMBER',
    'PLUS': 'PLUS',
    'MINUS': 'MINUS',
    'MULTI': 'MULTI',
    'DIV': 'DIV',
    'LPAREN': 'LPAREN',
    'RPAREN': 'RPAREN',
    'SEMI': 'SEMI',
    'EOF': 'EOF'
}

class Tolkien:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
        
    def __repr__(self):
        return f"Tolkien({self.type}, {repr(self.value)})"
    
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
        
    def advance(self):
        # Advance to the next character in the input
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
        
    def skip_whitecity_space(self):
        # Skip white space
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
            
    def number(self):
        # this handles our multi digit numbers and floats if needed
        result = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        if '.' in result:
            return Tolkien(TOLKIEN_TYPES['NUMBER'], float(result))
        return Tolkien(TOLKIEN_TYPES['NUMBER'], int(result))
    
    def get_next_tolkien(self):
        # Analyse and break our input down into Tolkiens
        while self.current_char is not None:
            
            if self.current_char.isspace():
                self.skip_whitecity_space()
                continue
            
            if self.current_char.isdigit():
                return self.number()
            
            if self.current_char =='+':
                self.advance()
                return Tolkien(TOLKIEN_TYPES['PLUS'], '+')
            
            if self.current_char == '-':
                self.advance()
                return Tolkien(TOLKIEN_TYPES['MINUS'], '-')
            
            if self.current_char == '*':
                self.advance()
                return Tolkien(TOLKIEN_TYPES['MULTI'], '*')
            
            if self.current_char == '/':
                self.advance()
                return Tolkien(TOLKIEN_TYPES['DIV'], '/')
            
            if self.current_char == '(':
                self.advance()
                return Tolkien(TOLKIEN_TYPES['LPAREN'], '(')
            
            if self.current_char == ')':
                self.advance()
                return Tolkien(TOLKIEN_TYPES['RPAREN'], ')')
            
            if self.current_char == ';':
                self.advance()
                return Tolkien(TOLKIEN_TYPES['SEMI'], ';')
            
            raise Exception(f"The Nine are abroad, this is not part of the Fellowship: {self.current_char}")
        
        return Tolkien(TOLKIEN_TYPES['EOF'], None)