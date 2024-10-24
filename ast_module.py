from parser_module import tokenize, Parser
from ast_node import Node, compare

def create_rule(rule_string):
    tokens = tokenize(rule_string)
    parser = Parser(tokens)
    ast = parser.parse()
    return ast

def combine_rules(rule_asts):
    if not rule_asts:
        return None
    root = rule_asts[0]
    for ast in rule_asts[1:]:
        root = Node('operator', left=root, right=ast, operator='OR')
    return root

def evaluate_rule(ast, data):
    return ast.evaluate(data)

def serialize_ast(node):
    if node is None:
        return None
    if node.type == 'operator':
        return {
            'type': 'operator',
            'operator': node.operator,
            'left': serialize_ast(node.left),
            'right': serialize_ast(node.right)
        }
    elif node.type == 'operand':
        return {
            'type': 'operand',
            'value': node.value
        }

def deserialize_ast(data):
    if data is None:
        return None
    if data['type'] == 'operator':
        left = deserialize_ast(data['left'])
        right = deserialize_ast(data['right'])
        return Node('operator', left=left, right=right, operator=data['operator'])
    elif data['type'] == 'operand':
        return Node('operand', value=data['value'])
