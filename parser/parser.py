from lexer.lexer import Lexer
from abstract_syntax_tree.nodes import Number, BinaryOp

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_tolkien = lexer.get_next_tolkien()
        
    def error(self, expected):
        raise Exception(f"You speak with the charmed tongue of Saruman: Expected {expected}, but got {self.current_tolkien}")
    
    def eat(self, tolkien_type):
        # Consume the current tolkien if it meets the expected type, otherwise raise an error
        if self.current_tolkien.type == tolkien_type:
            self.current_tolkien = self.lexer.get_next_tolkien()
        else:
            self.error(tolkien_type)
            
    def parse(self):
        """Parse the entire program (single expression followed by semicolon and EOF)."""
        node = self.program()
        if self.current_tolkien.type != 'EOF':
            self.error('EOF')
        return node
    
    def program(self):
        """
        program → (expr SEMI)* EOF
        Handles multiple expressions separated by semicolons.
        """
        expressions = []
        while self.current_tolkien.type != 'EOF':
            node = self.expr()
            self.eat('SEMI')
            expressions.append(node)
        return expressions
    
    def expr(self):
        """
        expr → term ((PLUS | MINUS) term)*
        Handles addition and subtraction.
        """
        node = self.term()
        
        while self.current_tolkien.type in ('PLUS', 'MINUS'):
            tolkien = self.current_tolkien
            self.eat(tolkien.type)
            node = BinaryOp(left=node, op=tolkien.value, right=self.term())
            
        return node
    
    def term(self):
        """
        term → factor ((MULT | DIV) factor)*
        Handles multiplication and division.
        """
        node = self.factor()
        
        while self.current_tolkien.type in ('MULTI', 'DIV'):
            tolkien = self.current_tolkien
            self.eat(tolkien.type)
            node = BinaryOp(left=node, op=tolkien.value, right=self.factor())
            
        return node
    
    def factor(self):
        """
        factor → NUMBER | LPAREN expr RPAREN
        Handles numbers and parentheses.
        """
        tolkien = self.current_tolkien
        if tolkien.type == 'NUMBER':
            self.eat('NUMBER')
            return Number(tolkien.value)
        elif tolkien.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
            return node
        else:
            self.error('NUMBER or LPAREN')