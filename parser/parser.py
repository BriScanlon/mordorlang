from lexer.lexer import Lexer
from abstract_syntax_tree.nodes import (
    Number,
    BinaryOp,
    Boolean,
    CompareOp,
    LogicalOp,
    UnaryOp,
    String,
    Assign,
    Var,
    Print,
    If
)


class Parser:
    # The Parser reads Tolkiens from the Lexer and constructs an Abstract Syntax Tree (AST)
    def __init__(self, lexer: Lexer):
        # Initialize the parser with a lexer and the first token
        self.lexer = lexer
        self.current_tolkien = lexer.get_next_tolkien()

    def error(self, expected):
        # Raise an exception if the current token is not the expected type
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
        # Parse the input text and return the AST
        node = self.program()
        if self.current_tolkien.type != "EOF":
            self.error("EOF")
        return node

    def assignment(self):
        # assignment → IDENTIFIER EQUALS logical_expr
        var_name = self.current_tolkien.value
        self.eat("IDENTIFIER")  # Consume variable name
        self.eat("EQUALS")  # Consume '='
        value = self.logical_expr()  # Parse assigned value
        return Assign(var_name, value)


    def statement(self):
        if self.current_tolkien.type == "IF":
            return self.if_statement()
        # statement → assignment | print_statement | logical_expr
        elif self.current_tolkien.type == "WHILE":
            return self.while_statement()
        elif self.current_tolkien.type == "IDENTIFIER" and self.lexer.peek() == "=":
            return self.assignment()  # Recognizes assignment statements
        elif self.current_tolkien.type == "PRINT":
            return self.print_statement()  # Recognizes print statements
        else:
            return self.logical_expr()  # Default: process an expression

    def print_statement(self):
        # Allow both `print x;` and `print(x);`
        self.eat("PRINT")
        
        if self.current_tolkien.type == "LPAREN":  
            # Case: print(x)
            self.eat("LPAREN")
            expr = self.logical_expr()
            self.eat("RPAREN")
        else:
            # Case: print x;
            if self.current_tolkien.type == "IDENTIFIER":
                expr = self.variable_reference()
            else:
                expr = self.logical_expr()

        return Print(expr)


    def program(self):
        # program → (statement SEMI)* EOF
        expressions = []
        while self.current_tolkien.type != "EOF":
            node = self.statement() # Supports assignments & print
            self.eat("SEMI")  # Ensure semicolon after each statement
            expressions.append(node)
        return expressions

    def expr(self):
        # expr → term ((PLUS | MINUS) term)*, handling strings and numbers
        node = self.term()
        while self.current_tolkien.type in ("PLUS", "MINUS"):
            tolkien = self.current_tolkien
            self.eat(tolkien.type)
            right_node = self.term()
            node = BinaryOp(left=node, op=tolkien.value, right=right_node)

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
        elif tolkien.type == "STRING":
            self.eat("STRING")
            return String(tolkien.value)
        elif tolkien.type == "IDENTIFIER":
            return Var(self.variable_reference())
        else:
            self.error("NUMBER, BOOLEAN, MINUS or LPAREN")

    def variable_reference(self):
        # variable_reference → IDENTIFIER
        var_name = self.current_tolkien.value   
        self.eat("IDENTIFIER")
        return Var(var_name)

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
    
    def while_statement(self):
        # while_statement → WHILE logical_expr statement
        self.eat("WHILE")
        condition = self.logical_expr()
        body = self.statement()
        return While(condition, body)

    def if_statement(self):
        # Parse an if-statement: IF condition statement (if_statement_tail)?
        self.eat("IF")
        condition = self.logical_expr()
        then_branch = self.statement()
        else_branch = self.if_statement_tail()  # Process any ELIF or ELSE parts
        return If(condition, then_branch, else_branch)

    def if_statement_tail(self):
        # Parse the tail of an if-statement, which can be an ELIF chain or an ELSE branch.
        if self.current_tolkien.type == "ELIF":
            self.eat("ELIF")
            condition = self.logical_expr()
            then_branch = self.statement()
            else_branch = self.if_statement_tail()  # Allow for further ELIF or ELSE
            # Represent the ELIF as a nested If node in the else branch.
            return If(condition, then_branch, else_branch)
        elif self.current_tolkien.type == "ELSE":
            self.eat("ELSE")
            return self.statement()
        else:
            # No further branch; return None to indicate the end of the chain.
            return None