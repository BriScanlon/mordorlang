import re

# define our tokens/Tolkiens as constants

TOLKIEN_TYPES = {
    "NUMBER": "NUMBER",
    "PLUS": "PLUS",
    "MINUS": "MINUS",
    "MULTI": "MULTI",
    "DIV": "DIV",
    "LPAREN": "LPAREN",
    "RPAREN": "RPAREN",
    "SEMI": "SEMI",
    "BOOLEAN": "BOOLEAN",
    "AND": "AND",
    "OR": "OR",
    "NOT": "NOT",
    "EQ": "EQ",
    "NEQ": "NEQ",
    "LT": "LT",
    "GT": "GT",
    "LTE": "LTE",
    "GTE": "GTE",
    "EOF": "EOF",
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

    def peek(self):
        # Look at the next character without moving the pointer
        peek_pos = self.pos + 1
        return self.text[peek_pos] if peek_pos < len(self.text) else None

    def skip_whitecity_space(self):
        # Skip white space
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        # this handles our multi digit numbers and floats if needed
        result = ""
        while self.current_char is not None and (
            self.current_char.isdigit() or self.current_char == "."
        ):
            result += self.current_char
            self.advance()
        if "." in result:
            return Tolkien(TOLKIEN_TYPES["NUMBER"], float(result))
        return Tolkien(TOLKIEN_TYPES["NUMBER"], int(result))

    def identifier(self):
        # Handle identifiers (true, false)
        result = ""
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        if result == "true":
            return Tolkien(TOLKIEN_TYPES["BOOLEAN"], True)
        elif result == "false":
            return Tolkien(TOLKIEN_TYPES["BOOLEAN"], False)
        else:
            raise Exception(f"The Eye does not recognize this: {result}")

    def get_next_tolkien(self):
        # Analyse and break our input down into Tolkiens
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitecity_space()
                continue
            
            if self.text[self.pos].startswith("true"):
                for _ in range(4): self.advance()
                return Tolkien(TOLKIEN_TYPES["BOOLEAN"], True)
            
            if self.text[self.pos].startswith("false"):
                for _ in range(5): self.advance()
                return Tolkien(TOLKIEN_TYPES["BOOLEAN"], False)
            
            if self.text[self.pos].startswith("and"):
                for _ in range(3): self.advance()
                return Tolkien(TOLKIEN_TYPES["AND"], "and")
            
            if self.text[self.pos].startswith("or"):
                for _ in range(2): self.advance()
                return Tolkien(TOLKIEN_TYPES["OR"], "or")
            
            if self.text[self.pos].startswith("not"):
                for _ in range(3): self.advance()
                return Tolkien(TOLKIEN_TYPES["NOT"], "not")
            
            if self.tet[self.pos].startswith("!"):
                self.advance()
                return Tolkien(TOLKIEN_TYPES["NOT"], "not")

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha():
                return self.identifier()

            if self.current_char == "=":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Tolkien(TOLKIEN_TYPES["EQ"], "==")
                raise Exception("Single '=' is not allowed yet, use '==' instead")

            if self.current_char == "!":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Tolkien(TOLKIEN_TYPES["NEQ"], "!=")
                raise Exception(
                    f"Saruman speaks lies: '{self.current_char}' not valid here."
                )

            if self.current_char == "<":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Tolkien(TOLKIEN_TYPES["LTE"], "<=")
                return Tolkien(TOLKIEN_TYPES["LT"], "<")

            if self.current_char == ">":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Tolkien(TOLKIEN_TYPES["GTE"], ">=")
                return Tolkien(TOLKIEN_TYPES["GT"], ">")

            if self.current_char == "+":
                self.advance()
                return Tolkien(TOLKIEN_TYPES["PLUS"], "+")

            if self.current_char == "-":
                self.advance()
                return Tolkien(TOLKIEN_TYPES["MINUS"], "-")

            if self.current_char == "*":
                self.advance()
                return Tolkien(TOLKIEN_TYPES["MULTI"], "*")

            if self.current_char == "/":
                self.advance()
                return Tolkien(TOLKIEN_TYPES["DIV"], "/")

            if self.current_char == "(":
                self.advance()
                return Tolkien(TOLKIEN_TYPES["LPAREN"], "(")

            if self.current_char == ")":
                self.advance()
                return Tolkien(TOLKIEN_TYPES["RPAREN"], ")")

            if self.current_char == ";":
                self.advance()
                return Tolkien(TOLKIEN_TYPES["SEMI"], ";")

            raise Exception(
                f"The Nine are abroad, this is not part of the Fellowship: {self.current_char}"
            )

        return Tolkien(TOLKIEN_TYPES["EOF"], None)
