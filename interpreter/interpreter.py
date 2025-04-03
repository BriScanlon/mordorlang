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
    Fun,
    FunctionCall,
    Return,
)


class ReturnException(Exception):
    """
    Custom exception to handle 'return' control flow.
    When a return statement is encountered, we raise this,
    and the function call visitor catches it.
    """

    def __init__(self, value):
        self.value = value


class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent

    def define(self, name, value):
        # Create or overwrite a binding in this environment
        self.values[name] = value

    def assign(self, name, value):
        if name in self.values:
            self.values[name] = value
        elif self.parent is not None:
            self.parent.assign(name, value)
        else:
            self.values[name] = value

    def get(self, name):
        # Lookup variable in this scope, otherwise check parent
        if name in self.values:
            return self.values[name]
        elif self.parent is not None:
            return self.parent.get(name)
        else:
            raise Exception(f"Undefined variable: {name}")


class Interpreter:
    def __init__(self):
        self.env = Environment()

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.no_visit_method)
        return visitor(node)

    def no_visit_method(self, node):
        raise Exception(f"No visit_{type(node).__name__} method defined.")


    #   Basic AST Visitors
    def visit_Number(self, node: Number):
        return node.value

    def visit_BinaryOp(self, node: BinaryOp):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        if node.op == "+":
            # Support addition of strings or numbers
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

    def visit_Boolean(self, node: Boolean):
        return node.value

    def visit_CompareOp(self, node: CompareOp):
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
            raise Exception(f"Unknown compare operator: {node.op}")

    def visit_LogicalOp(self, node: LogicalOp):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        if node.op in ("agh", "and"):
            return left_value and right_value
        elif node.op in ("urz", "or"):
            return left_value or right_value
        else:
            raise Exception(f"Unknown logical operator: {node.op}")

    def visit_UnaryOp(self, node: UnaryOp):
        operand_value = self.visit(node.operand)
        if node.op == "not":
            return not operand_value
        elif node.op == "-":
            # Negation of the number
            return -operand_value
        else:
            raise Exception(f"Unknown unary operator: {node.op}")

    def visit_String(self, node: String):
        return node.value

    # Variables and Assign
    def visit_Assign(self, node: Assign):
        value = self.visit(node.expr)
        self.env.assign(node.var_name, value)
        return value

    def visit_Var(self, node: Var):
        return self.env.get(node.var_name)

    # Print & Block
    def visit_Print(self, node: Print):
        value = self.visit(node.expr)
        print(value)
        return value

    def visit_Block(self, node: Block):
        # Create a new environment for the block
        previous_env = self.env
        self.env = Environment(parent=previous_env)
        result = None

        for statement in node.statements:
            result = self.visit(statement)
        self.env = previous_env
        return result

    # If & While
    def visit_If(self, node: If):
        condition_value = self.visit(node.condition)
        if condition_value:
            return self.visit(node.then_branch)
        elif node.else_branch is not None:
            return self.visit(node.else_branch)
        return None

    def visit_While(self, node: While):
        while self.visit(node.condition):
            self.visit(node.body)
        return None

    # Function & Return
    def visit_Fun(self, node: Fun):
        """
        If your parser produces a 'Fun' node for function definitions.
        We store the node in the environment under its name.
        """
        self.env.define(node.name, node)
        return None  # Defining a function doesn't produce a value

    def visit_Fun(self, node: Fun):
        """
        If your parser uses a 'FunctionDef' node.
        Similar logic: store node in environment.
        """
        self.env.define(node.name, node)
        return None

    def visit_FunctionCall(self, node: FunctionCall):
        """
        1. Look up the function node (Fun or FunctionDef) by name
        2. Create a new environment for the call
        3. Evaluate arguments and bind them to parameters
        4. Execute the function body
        5. Catch ReturnException for an early return
        """
        # Retrieve the function from environment
        func_node = self.env.get(node.func_name)

        # Distinguish between 'Fun' or 'FunctionDef' or raise error if not found
        if not (hasattr(func_node, "params") and hasattr(func_node, "body")):
            raise Exception(f"'{node.func_name}' is not a function.")

        # Check argument count
        if len(node.arguments) != len(func_node.params):
            raise Exception("Argument count mismatch.")

        # Create a new environment for the function call
        previous_env = self.env
        self.env = Environment(parent=previous_env)

        # Assign parameters
        for param_name, arg_expr in zip(func_node.params, node.arguments):
            arg_value = self.visit(arg_expr)
            self.env.define(param_name, arg_value)

        # Execute body
        result = None
        try:
            result = self.visit(func_node.body)
        except ReturnException as re:
            result = re.value

        # Restore environment
        self.env = previous_env
        return result

    def visit_Return(self, node: Return):
        """
        Raise ReturnException to unwind the function body.
        If node.expr is None, return None.
        """
        value = self.visit(node.expr) if node.expr else None
        raise ReturnException(value)
