class Number:
    def __init__(self, value):
        self.value = value
        
    def __repr__(self):
        return f"Number({self.value})"
    
class BinaryOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
        
    def __repr__(self):
        return f"BinaryOp({self.left}, {self.op}, {self.right})"