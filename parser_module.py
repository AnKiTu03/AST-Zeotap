import re
from ast_node import Node

def tokenize(rule_string):
    tokens = []
    token_specification = [
        ('NUMBER',   r'\d+(\.\d*)?'),
        ('AND',      r'AND\b'),
        ('OR',       r'OR\b'),
        ('NOT',      r'NOT\b'),
        ('EQ',       r'=='),
        ('NEQ',      r'!='),
        ('LE',       r'<='),
        ('GE',       r'>='),
        ('LT',       r'<'),
        ('GT',       r'>'),
        ('LPAREN',   r'\('),
        ('RPAREN',   r'\)'),
        ('STRING',   r'\'[^\']*\''),
        ('IDENT',    r'[A-Za-z_][A-Za-z0-9_]*'),
        ('SKIP',     r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    for mo in re.finditer(tok_regex, rule_string):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            tokens.append(('NUMBER', float(value)))
        elif kind == 'STRING':
            tokens.append(('STRING', value.strip("'")))
        elif kind in ('AND', 'OR', 'NOT', 'EQ', 'NEQ', 'LE', 'GE', 'LT', 'GT', 'LPAREN', 'RPAREN'):
            tokens.append((kind, value))
        elif kind == 'IDENT':
            tokens.append(('IDENT', value))
        elif kind == 'SKIP':
            pass
        else:
            raise SyntaxError(f'Unexpected token: {value}')
    return tokens

class Parser:
    allowed_attributes = {'age', 'department', 'salary', 'experience'}

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        node = self.expr()
        if self.pos < len(self.tokens):
            raise SyntaxError('Unexpected token at the end')
        return node

    def expr(self):
        node = self.term()
        while self.current_token() and self.current_token()[0] == 'OR':
            op = self.consume('OR')[1]
            right = self.term()
            node = Node('operator', left=node, right=right, operator=op)
        return node

    def term(self):
        node = self.factor()
        while self.current_token() and self.current_token()[0] == 'AND':
            op = self.consume('AND')[1]
            right = self.factor()
            node = Node('operator', left=node, right=right, operator=op)
        return node

    def factor(self):
        token = self.current_token()
        if token[0] == 'LPAREN':
            self.consume('LPAREN')
            node = self.expr()
            self.consume('RPAREN')
            return node
        else:
            return self.condition()

    def condition(self):
        attr_token = self.consume('IDENT')
        if attr_token[1] not in self.allowed_attributes:
            raise SyntaxError(f"Attribute '{attr_token[1]}' is not allowed")
        op_token = self.consume_operator()
        value_token = self.consume_value()
        condition = {
            'attribute': attr_token[1],
            'operator': op_token[1],
            'value': value_token[1]
        }
        return Node('operand', value=condition)

    def consume(self, expected_type):
        token = self.current_token()
        if token and token[0] == expected_type:
            self.pos += 1
            return token
        else:
            raise SyntaxError(f"Expected token {expected_type}, got {token}")

    def consume_operator(self):
        token = self.current_token()
        if token and token[0] in ('EQ', 'NEQ', 'LE', 'GE', 'LT', 'GT'):
            self.pos += 1
            return token
        else:
            raise SyntaxError(f"Expected comparison operator, got {token}")

    def consume_value(self):
        token = self.current_token()
        if token and token[0] in ('NUMBER', 'STRING', 'IDENT'):
            self.pos += 1
            return token
        else:
            raise SyntaxError(f"Expected value, got {token}")

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        else:
            return None
