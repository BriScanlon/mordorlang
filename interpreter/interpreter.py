from async_s_t.nodes import Number, BinaryOp

class Interpreter:
    def visit(self, node):
        # Dispatch to the correct visit method based on node type
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.no_visit_method)
        return visitor(node)

    def no_visit_method(self, node):
        # Handle unsupported node types.
        raise Exception(f"No visit_{type(node).__name__} method defined.")

    def visit_Number(self, node: Number):
        # Return the numeric value from a Number node.
        return node.value

    def visit_BinaryOp(self, node: BinaryOp):
        #Evaluate BinaryOp nodes based on their operation (+, -, *, /).
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)

        if node.op == '+':
            return left_value + right_value
        elif node.op == '-':
            return left_value - right_value
        elif node.op == '*':
            return left_value * right_value
        elif node.op == '/':
            if right_value == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            return left_value / right_value
        else:
            raise Exception(f"Unknown operator: {node.op}")
