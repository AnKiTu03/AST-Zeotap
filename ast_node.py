class Node:
    def __init__(self, node_type, left=None, right=None, value=None, operator=None):
        self.type = node_type  # 'operator' or 'operand'
        self.left = left
        self.right = right
        self.value = value  # For operands
        self.operator = operator  # For operators

    def evaluate(self, data):
        if self.type == 'operator':
            if self.operator == 'AND':
                return self.left.evaluate(data) and self.right.evaluate(data)
            elif self.operator == 'OR':
                return self.left.evaluate(data) or self.right.evaluate(data)
            else:
                raise ValueError(f"Unknown operator: {self.operator}")
        elif self.type == 'operand':
            attr_value = data.get(self.value['attribute'])
            if attr_value is None:
                raise ValueError(f"Attribute '{self.value['attribute']}' not found in data")
            operator = self.value['operator']
            comparison_value = self.value['value']
            return compare(attr_value, operator, comparison_value)
        else:
            raise ValueError(f"Unknown node type: {self.type}")

def compare(a, operator, b):
    if operator == '>':
        return a > b
    elif operator == '<':
        return a < b
    elif operator == '>=':
        return a >= b
    elif operator == '<=':
        return a <= b
    elif operator == '==':
        return a == b
    elif operator == '!=':
        return a != b
    else:
        raise ValueError(f"Unknown comparison operator: {operator}")
