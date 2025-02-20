from abstract_syntax_tree.nodes import Number, BinaryOp, Boolean, CompareOp

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

    def visit_BinaryOp(self, node: Boolean):
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

    def visit_Boolean(self, node):
        return node.value
    
    def visit_CompareOp(self, node: CompareOp):
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        if node.op == '==':
            return left == right
        elif node.op == '!=':
            return left != right
        elif node.op == '<':
            return left < right
        elif node.op == '>':
            return left > right
        elif node.op == '<=':
            return left <= right
        elif node.op == '>=':
            return left >= right
        else:
            raise Exception(f"Unknown operator: {node.op}")
        
    def visit_LogicalOp(self, node):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)

        if node.op == 'agh':
            return left_value and right_value
        elif node.op == 'and':
            return left_value and right_value
        elif node.op == 'or':
            return left_value or right_value
        elif node.op == 'urz':
            return left_value or right_value
        else:
            raise Exception(f"Unknown logical operator: {node.op}")

    def visit_UnaryOp(self, node):
        operand_value = self.visit(node.operand)
        
        if node.op == 'not':
            return not operand_value
        elif node.op == '-':
            return -operand_value  # Negation of the number
        else:
            raise Exception(f"Unknown unary operator: {node.op}")