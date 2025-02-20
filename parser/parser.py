from lexer.lexer import Lexer
from abstract_syntax_tree.nodes import (
    Number,
    BinaryOp,
    Boolean,
    CompareOp,
    LogicalOp,
    UnaryOp,
)


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_tolkien = lexer.get_next_tolkien()

    def error(self, expected):
        raise Exception(
            f"You speak with the charmed tongue of Saruman: Expected {expected}, but got {self.current_tolkien}"
        )

    def eat(self, tolkien_type):
        # Consume the current tolkien if it meets the expected type, otherwise raise an error
        if self.current_tolkien.type == tolkien_type:
            self.current_tolkien = self.lexer.get_next_tolkien()
        else:
            self.error(tolkien_type)

    def parse(self):
        """Parse the entire program (single expression followed by semicolon and EOF)."""
        node = self.program()
        if self.current_tolkien.type != "EOF":
            self.error("EOF")
        return node

    def program(self):
        """
        program → (logical_expr SEMI)* EOF
        Handles multiple logical, comparison, and arithmetic expressions separated by semicolons.
        """
        expressions = []
        while self.current_tolkien.type != "EOF":
            node = self.logical_expr()
            self.eat("SEMI")
            expressions.append(node)
        return expressions

    
    def expr(self):
        # expr → term ((PLUS | MINUS) term)*
        node = self.term()
        while self.current_tolkien.type in ("PLUS", "MINUS"):
            tolkien = self.current_tolkien
            self.eat(tolkien.type)
            node = BinaryOp(left=node, op=tolkien.value, right=self.term())
        return node

    def term(self):
        # term → unary_expr ((MULT | DIV) unary_expr)*
        node = self.unary_expr()
        while self.current_tolkien.type in ("MULTI", "DIV"):
            tolkien = self.current_tolkien
            self.eat(tolkien.type)
            node = BinaryOp(left=node, op=tolkien.value, right=self.unary_expr())
        return node

    def comparison(self):
        # comparison → expr ( (== | != | < | <= | > | >=) expr )*
        node = self.expr()
        while self.current_tolkien.type in ("EQ", "NEQ", "LT", "LTE", "GT", "GTE"):
            tolkien = self.current_tolkien
            self.eat(tolkien.type)
            node = CompareOp(left=node, op=tolkien.value, right=self.expr())
        return node

    def factor(self):
        # factor -> NOT factor | NUMBER | BOOLEAN | LPAREN comparison RPAREN
        # Handles Booleans, numbers and parentheses.
        tolkien = self.current_tolkien
        
        if tolkien.type == "MINUS":
            self.eat("MINUS")
            return UnaryOp(op="-", operand=self.factor())
        elif tolkien.type == "BOOLEAN":
            self.eat("BOOLEAN")
            return Boolean(tolkien.value)
        elif tolkien.type == "NUMBER":
            self.eat("NUMBER")
            return Number(tolkien.value)
        elif tolkien.type == "LPAREN":
            self.eat("LPAREN")
            node = self.comparison()
            self.eat("RPAREN")
            return node
        else:
            self.error("NUMBER, BOOLEAN, MINUS or LPAREN")

    def logical_expr(self):
        # logical_expr → comparison ( (AND | OR) comparison )*
        node = self.comparison()

        while self.current_tolkien.type in ("AND", "OR"):
            tolkien = self.current_tolkien
            self.eat(tolkien.type)
            node = LogicalOp(left=node, op=tolkien.value, right=self.comparison())

        return node

    def unary_expr(self):
        # unary_expr → NOT unary_expr | factor
        if self.current_tolkien.type == "NOT":
            tolkien = self.current_tolkien
            self.eat("NOT")
            return UnaryOp(op=tolkien.value, operand=self.unary_expr())
        return self.factor()
