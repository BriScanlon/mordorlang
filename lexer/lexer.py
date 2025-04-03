import re

# define our Tolkiens as constants
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
    "STRING": "STRING",
    "CONCAT": "CONCAT",
    "PRINT": "PRINT",
    "IDENTIFIER": "IDENTIFIER",
    "EQUALS": "EQUALS",
    "EOF": "EOF",
    "IF": "IF",
    "ELSE": "ELSE",
    "ELIF": "ELIF",
    "WHILE": "WHILE",
    "LBRACE": "LBRACE",
    "RBRACE": "RBRACE",
    "FUN": "FUN",
    "RETURN": "RETURN",
    "COMMA": "COMMA",
}


class Tolkien:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Tolkien({self.type}, {repr(self.value)})"


# Define Black Speech keywords
BLACK_SPEECH_KEYWORDS = {
    "true": Tolkien(TOLKIEN_TYPES["BOOLEAN"], True),
    "false": Tolkien(TOLKIEN_TYPES["BOOLEAN"], False),
    "goth": Tolkien(TOLKIEN_TYPES["BOOLEAN"], True),
    "burzum": Tolkien(TOLKIEN_TYPES["BOOLEAN"], False),
    "agh": Tolkien(TOLKIEN_TYPES["AND"], "agh"), 
    "and": Tolkien(TOLKIEN_TYPES["AND"], "and"),
    "urz": Tolkien(TOLKIEN_TYPES["OR"], "urz"), 
    "or": Tolkien(TOLKIEN_TYPES["OR"], "or"),
    "not": Tolkien(TOLKIEN_TYPES["NOT"], "not"),
    "print": Tolkien(TOLKIEN_TYPES["PRINT"], "print"),
    "krimp": Tolkien(TOLKIEN_TYPES["PRINT"], "krimp"), 
    "if": Tolkien(TOLKIEN_TYPES["IF"], "if"),
    "gul": Tolkien(TOLKIEN_TYPES["IF"], "gul"), 
    "else": Tolkien(TOLKIEN_TYPES["ELSE"], "else"),
    "skai": Tolkien(TOLKIEN_TYPES["ELSE"], "skai"),
    "gul-nakh": Tolkien(TOLKIEN_TYPES["ELIF"], "gul-nakh"),
    "elif": Tolkien(TOLKIEN_TYPES["ELIF"], "elif"),
    "while": Tolkien(TOLKIEN_TYPES["WHILE"], "while"),
    "arburz": Tolkien(TOLKIEN_TYPES["WHILE"], "arburz"),
    "fun": Tolkien(TOLKIEN_TYPES["FUN"], "fun"),
    "zagh": Tolkien(TOLKIEN_TYPES["RETURN"], "zagh"),
}


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def peek(self):
        peek_pos = self.pos + 1
        return self.text[peek_pos] if peek_pos < len(self.text) else None

    def skip_whitecity_space(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ""
        while self.current_char is not None and (
            self.current_char.isdigit() or self.current_char == "."
        ):
            result += self.current_char
            self.advance()
        if "." in result:
            return Tolkien(TOLKIEN_TYPES["NUMBER"], float(result))
        return Tolkien(TOLKIEN_TYPES["NUMBER"], int(result))

    def string(self):
        result = ""
        self.advance()
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == "\\":
                self.advance()
                if self.current_char == "n":
                    result += "\n"
                elif self.current_char == "t":
                    result += "\t"
                elif self.current_char == '"':
                    result += '"'
                else:
                    result += self.current_char
            else:
                result += self.current_char
            self.advance()

        if self.current_char != '"':
            raise Exception("The way is open, close the string literal!")
        self.advance()
        return Tolkien(TOLKIEN_TYPES["STRING"], result)

    def identifier(self):
        """Handles identifiers (variables and keywords, including Black Speech)."""
        result = ""
        while self.current_char is not None and (
            self.current_char.isalnum() or self.current_char == "_"
        ):
            result += self.current_char
            self.advance()

        # Check for Black Speech or standard keywords
        return BLACK_SPEECH_KEYWORDS.get(
            result, Tolkien(TOLKIEN_TYPES["IDENTIFIER"], result)
        )

    def get_next_tolkien(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitecity_space()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha():
                return self.identifier()

            if self.current_char == '"':
                return self.string()

            if self.current_char == "=":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    # Equality check
                    return Tolkien(TOLKIEN_TYPES["EQ"], "==")
                # Assignment operator
                return Tolkien(TOLKIEN_TYPES["EQUALS"], "=")

            if self.current_char == "!":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Tolkien(TOLKIEN_TYPES["NEQ"], "!=")
                else:
                    return Tolkien(TOLKIEN_TYPES["NOT"], "not")

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
            
            if self.current_char == ",":
                self.advance()
                return Tolkien(TOLKIEN_TYPES["COMMA"], ",")

            if self.current_char == ";":
                self.advance()
                return Tolkien(TOLKIEN_TYPES["SEMI"], ";")
            
            if self.current_char == "{":
                self.advance()
                return Tolkien(TOLKIEN_TYPES["LBRACE"], "{")
            if self.current_char == "}":
                self.advance()
                return Tolkien(TOLKIEN_TYPES["RBRACE"], "}")

            raise Exception(
                f"The Nine are abroad, this is not part of the Fellowship: {self.current_char}"
            )

        return Tolkien(TOLKIEN_TYPES["EOF"], None)
