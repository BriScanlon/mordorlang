class Number:
    # Number nodes represent numeric values in the AST.
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"


class BinaryOp:
    # BinaryOp nodes represent binary operations in the AST.
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinaryOp({self.left}, {self.op}, {self.right})"


class Boolean:
    # Boolean nodes represent boolean values in the AST.
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Boolean({self.value})"


class CompareOp:
    # CompareOp nodes represent comparison operations in the AST.
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"CompareOp({self.left}, {self.op}, {self.right})"


class LogicalOp:
    # LogicalOp nodes represent logical operations in the AST.
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"LogicalOp({self.left}, {self.op}, {self.right})"


class UnaryOp:
    # UnaryOp nodes represent unary operations in the AST.
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    def __repr__(self):
        return f"UnaryOp({self.op}, {self.operand})"

class String:
    # String nodes represent string values in the AST.
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'String("{self.value}")'