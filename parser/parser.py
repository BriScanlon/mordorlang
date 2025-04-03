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
    If,
    While,
    Fun,
    Return,
    Block,
    Fun,
    FunctionCall,
)


class Parser:
    # The Parser reads Tolkiens from the Lexer and constructs an Abstract Syntax Tree (AST).
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_tolkien = lexer.get_next_tolkien()

    def error(self, expected):
        raise Exception(
            f"You speak with the charmed tongue of Saruman: Expected {expected}, but got {self.current_tolkien}"
        )

    def eat(self, tolkien_type):
        if self.current_tolkien.type == tolkien_type:
            self.current_tolkien = self.lexer.get_next_tolkien()
        else:
            self.error(tolkien_type)

    def parse(self):
        node = self.program()
        if self.current_tolkien.type != "EOF":
            self.error("EOF")
        return node

    # --------------------------
    #      High-Level Rules
    # --------------------------

    def program(self):
        # program -> (statement SEMI)* EOF
        statements = []
        while self.current_tolkien.type != "EOF":
            stmt = self.statement()
            self.eat("SEMI")  # Every statement ends with a semicolon
            statements.append(stmt)
        return statements  # or wrap with a Block node if desired

    def statement(self):
        # Distinguish different statement types based on the current token.
        tok_type = self.current_tolkien.type

        if tok_type == "FUN":
            return self.fun_statement()

        elif tok_type == "RETURN":
            return self.return_statement()

        elif tok_type == "IF":
            return self.if_statement()

        elif tok_type == "WHILE":
            return self.while_statement()

        elif tok_type == "PRINT":
            return self.print_statement()

        elif tok_type == "ELSE":
            # 'else' should only appear as part of an if-statement tail
            return None

        elif tok_type == "IDENTIFIER":
            # We need to see if it's assignment or function call or just a Var reference.
            return self.identifier_statement()

        else:
            # If none of the above, parse an expression as a statement.
            return self.logical_expr()

    def identifier_statement(self):
        """
        Distinguish between 'x = expr;' (assignment), 'x(...);' (function call),
        or just a variable reference as an expression statement.
        """
        name = self.current_tolkien.value
        # Peek the next token to see if it is '=' or '(' or something else
        peeked = self.lexer.peek()

        if peeked == "=":
            # It's assignment
            return self.assignment()

        # Otherwise, we consume the IDENTIFIER now...
        self.eat("IDENTIFIER")

        from abstract_syntax_tree.nodes import FunctionCall

        if self.current_tolkien.type == "LPAREN":
            # It's a function call
            args = self.argument_list()
            return FunctionCall(name, args)
        else:
            # It's just a variable reference used as an expression statement
            # e.g. "x;" in the code
            from abstract_syntax_tree.nodes import Var

            return Var(name)

    # --------------------------
    #     Specific Statements
    # --------------------------

    def assignment(self):
        # assignment -> IDENTIFIER '=' logical_expr
        var_name = self.current_tolkien.value
        self.eat("IDENTIFIER")
        self.eat("EQUALS")
        value = self.logical_expr()
        return Assign(var_name, value)

    def fun_statement(self):
        """
        fun_statement -> FUN IDENTIFIER LPAREN (IDENTIFIER (COMMA IDENTIFIER)*)? RPAREN block
        Creates a 'Fun' or 'FunctionDef' node. Here we keep 'Fun' as you have in your code.
        """
        self.eat("FUN")
        fun_name = self.current_tolkien.value
        self.eat("IDENTIFIER")

        self.eat("LPAREN")
        parameters = []
        if self.current_tolkien.type == "IDENTIFIER":
            parameters.append(self.current_tolkien.value)
            self.eat("IDENTIFIER")
            while self.current_tolkien.type == "COMMA":
                self.eat("COMMA")
                parameters.append(self.current_tolkien.value)
                self.eat("IDENTIFIER")
        self.eat("RPAREN")

        body = self.block()
        return Fun(fun_name, parameters, body)

    def return_statement(self):
        # return_statement -> RETURN ( logical_expr )?
        self.eat("RETURN")
        from abstract_syntax_tree.nodes import Return

        # If the next token is a semicolon, '}', or EOF, there's no return value
        if self.current_tolkien.type in ("SEMI", "RBRACE", "EOF"):
            return Return(None)
        else:
            expr = self.logical_expr()
            return Return(expr)

    def if_statement(self):
        # if_statement -> IF ( logical_expr )? block if_statement_tail?
        self.eat("IF")
        # Optional parentheses around condition
        if self.current_tolkien.type == "LPAREN":
            self.eat("LPAREN")
            condition = self.logical_expr()
            self.eat("RPAREN")
        else:
            condition = self.logical_expr()

        then_branch = self.block()
        else_branch = self.if_statement_tail()

        return If(condition, then_branch, else_branch)

    def if_statement_tail(self):
        # if_statement_tail -> (ELIF ( ( logical_expr )? block ) | ELSE block )?
        if self.current_tolkien.type == "ELIF":
            self.eat("ELIF")
            if self.current_tolkien.type == "LPAREN":
                self.eat("LPAREN")
                condition = self.logical_expr()
                self.eat("RPAREN")
            else:
                condition = self.logical_expr()

            then_branch = self.block()
            else_branch = self.if_statement_tail()
            return If(condition, then_branch, else_branch)

        elif self.current_tolkien.type == "ELSE":
            self.eat("ELSE")
            return self.block()
        else:
            return None

    def while_statement(self):
        # while_statement -> WHILE ( logical_expr )? block
        self.eat("WHILE")
        if self.current_tolkien.type == "LPAREN":
            self.eat("LPAREN")
            condition = self.logical_expr()
            self.eat("RPAREN")
        else:
            condition = self.logical_expr()

        body = self.block()
        return While(condition, body)

    def print_statement(self):
        # print_statement -> PRINT expr | PRINT LPAREN expr RPAREN
        self.eat("PRINT")

        if self.current_tolkien.type == "LPAREN":
            self.eat("LPAREN")
            expr = self.logical_expr()
            self.eat("RPAREN")
        else:
            if self.current_tolkien.type == "IDENTIFIER":
                expr = self.variable_reference()
            else:
                expr = self.logical_expr()

        return Print(expr)

    def block(self):
        # block -> LBRACE (statement (SEMI)?)* RBRACE
        self.eat("LBRACE")
        statements = []
        while self.current_tolkien.type != "RBRACE":
            stmt = self.statement()
            statements.append(stmt)
            # If there's a semicolon, consume it; if next token is '}', that's allowed
            if self.current_tolkien.type == "SEMI":
                self.eat("SEMI")
            elif self.current_tolkien.type != "RBRACE":
                self.error("SEMI or RBRACE")

        self.eat("RBRACE")
        return Block(statements)

    # ---------------------------------
    #         Function Calls
    # ---------------------------------

    def argument_list(self):
        """
        argument_list -> LPAREN (logical_expr (COMMA logical_expr)*)? RPAREN
        Because we detect LPAREN before calling this, you can parse inside.
        """
        # NOTE: We already 'ate' the identifier in identifier_statement().
        # This method is invoked after we see 'LPAREN'.
        args = []
        self.eat("LPAREN")
        if self.current_tolkien.type != "RPAREN":
            # There's at least one argument
            args.append(self.logical_expr())
            while self.current_tolkien.type == "COMMA":
                self.eat("COMMA")
                args.append(self.logical_expr())
        self.eat("RPAREN")
        return args

    # ---------------------------------
    #       Expressions / Helpers
    # ---------------------------------

    def logical_expr(self):
        # logical_expr -> comparison ((AND | OR) comparison)*
        node = self.comparison()
        while self.current_tolkien.type in ("AND", "OR"):
            op_token = self.current_tolkien
            self.eat(op_token.type)
            right = self.comparison()
            node = LogicalOp(left=node, op=op_token.value, right=right)
        return node

    def comparison(self):
        # comparison -> expr ((== | != | < | <= | > | >=) expr)*
        node = self.expr()
        while self.current_tolkien.type in ("EQ", "NEQ", "LT", "LTE", "GT", "GTE"):
            op_token = self.current_tolkien
            self.eat(op_token.type)
            right = self.expr()
            node = CompareOp(left=node, op=op_token.value, right=right)
        return node

    def expr(self):
        # expr -> term ((PLUS | MINUS) term)*
        node = self.term()
        while self.current_tolkien.type in ("PLUS", "MINUS"):
            op_token = self.current_tolkien
            self.eat(op_token.type)
            right = self.term()
            node = BinaryOp(left=node, op=op_token.value, right=right)
        return node

    def term(self):
        # term -> unary_expr ((MULTI | DIV) unary_expr)*
        node = self.unary_expr()
        while self.current_tolkien.type in ("MULTI", "DIV"):
            op_token = self.current_tolkien
            self.eat(op_token.type)
            right = self.unary_expr()
            node = BinaryOp(left=node, op=op_token.value, right=right)
        return node

    def unary_expr(self):
        # unary_expr -> NOT unary_expr | factor
        if self.current_tolkien.type == "NOT":
            op_token = self.current_tolkien
            self.eat("NOT")
            operand = self.unary_expr()
            return UnaryOp(op=op_token.value, operand=operand)
        return self.factor()

    def factor(self):
        # factor -> MINUS factor | NUMBER | BOOLEAN | LPAREN comparison RPAREN | STRING | IDENTIFIER ...
        token = self.current_tolkien

        if token.type == "MINUS":
            self.eat("MINUS")
            return UnaryOp(op="-", operand=self.factor())

        elif token.type == "BOOLEAN":
            self.eat("BOOLEAN")
            return Boolean(token.value)

        elif token.type == "NUMBER":
            self.eat("NUMBER")
            return Number(token.value)

        elif token.type == "LPAREN":
            self.eat("LPAREN")
            node = self.comparison()
            self.eat("RPAREN")
            return node

        elif token.type == "STRING":
            self.eat("STRING")
            return String(token.value)

        elif token.type == "IDENTIFIER":
            return self.variable_reference()

        else:
            self.error("NUMBER, BOOLEAN, MINUS or LPAREN")

    def variable_reference(self):
        # variable_reference -> IDENTIFIER
        var_name = self.current_tolkien.value
        self.eat("IDENTIFIER")
        return Var(var_name)

    # ---------------------------------
    #  Optional: parameter_list method
    # ---------------------------------
    def parameter_list(self):
        # parameter_list -> ( IDENTIFIER (COMMA IDENTIFIER)* )?
        params = []
        if self.current_tolkien.type == "IDENTIFIER":
            params.append(self.current_tolkien.value)
            self.eat("IDENTIFIER")
            while self.current_tolkien.type == "COMMA":
                self.eat("COMMA")
                params.append(self.current_tolkien.value)
                self.eat("IDENTIFIER")
        return params
