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
    Block,
    If,
    While,
)


class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent

    def define(self, name, value):
        self.values[name] = value

    def assign(self, name, value):
        if name in self.values:
            # If the variable already exists in this scope, update it
            self.values[name] = value
        else:
            # Always define new variables locally in this scope
            self.values[name] = value

    def get(self, name):
        if name in self.values:
            return self.values[name]
        elif self.parent is not None:
            return self.parent.get(name)
        else:
            raise Exception(f"Undefined variable: {name}")


class Interpreter:
    def __init__(self):
        # Initialize the global variables dictionary
        self.env = Environment()

    def visit(self, node):
        # Dispatch to the correct visit method based on node type
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.no_visit_method)
        return visitor(node)

    def no_visit_method(self, node):
        # Handle unsupported node types.
        raise Exception(f"No visit_{type(node).__name__} method defined.")

    def visit_Number(self, node: Number):
        # Return the numeric value from a Number node.
        return node.value

    def visit_BinaryOp(self, node: Boolean):
        # Evaluate BinaryOp nodes based on their operation (+, -, *, /).
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)

        if node.op == "+":
            # Handle both number addition and string concatenation
            if isinstance(left_value, str) or isinstance(right_value, str):
                return str(left_value) + str(right_value)
            return left_value + right_value
        elif node.op == "-":
            return left_value - right_value
        elif node.op == "*":
            return left_value * right_value
        elif node.op == "/":
            if right_value == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            return left_value / right_value
        else:
            raise Exception(f"Unknown operator: {node.op}")

    def visit_Boolean(self, node):
        # Return the boolean value from a Boolean node.
        return node.value

    def visit_CompareOp(self, node: CompareOp):
        # Evaluate CompareOp nodes based on their operation (==, !=, <, >, <=, >=).
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op == "==":
            return left == right
        elif node.op == "!=":
            return left != right
        elif node.op == "<":
            return left < right
        elif node.op == ">":
            return left > right
        elif node.op == "<=":
            return left <= right
        elif node.op == ">=":
            return left >= right
        else:
            raise Exception(f"Unknown operator: {node.op}")

    def visit_LogicalOp(self, node):
        # Evaluate LogicalOp nodes based on their operation (and, or, not).
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)

        if node.op == "agh":
            return left_value and right_value
        elif node.op == "and":
            return left_value and right_value
        elif node.op == "or":
            return left_value or right_value
        elif node.op == "urz":
            return left_value or right_value
        else:
            raise Exception(f"Unknown logical operator: {node.op}")

    def visit_UnaryOp(self, node):
        # Evaluate UnaryOp nodes based on their operation (not, -).
        operand_value = self.visit(node.operand)

        if node.op == "not":
            return not operand_value
        elif node.op == "-":
            return -operand_value  # Negation of the number
        else:
            raise Exception(f"Unknown unary operator: {node.op}")

    def visit_Assign(self, node: Assign):
        value = self.visit(node.expr)
        # Assign the variable in the current environment
        self.env.assign(node.var_name, value)
        return value

    def visit_Var(self, node: Var):
        return self.env.get(node.var_name)

    def visit_Print(self, node):
        # Print the value of the expression node.
        value = self.visit(node.expr)
        print(value)
        return value

    def visit_String(self, node):
        # Return the string value from a String node.
        return node.value

    def visit_If(self, node):
        # Evaluate the condition of the If node.
        condition_value = self.visit(node.condition)
        if condition_value:
            # If the condition is true, execute the then_branch.
            return self.visit(node.then_branch)
        elif node.else_branch is not None:
            # If the condition is false and an else_branch exists,
            # recursively evaluate it.
            return self.visit(node.else_branch)
        return None

    def visit_While(self, node):
        # Continue executing the loop body as long as the condition evaluates to True.
        while self.visit(node.condition):
            self.visit(node.body)
        return None

    def visit_Block(self, node: Block):
        # Create a new environment for this block, with the current one as its parent.
        previous_env = self.env
        self.env = Environment(previous_env)
        result = None
        for statement in node.statements:
            result = self.visit(statement)
        self.env = previous_env
        return result
