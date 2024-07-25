import ply.yacc as yacc
from breeze_lexer import tokens

# Define the abstract syntax tree (AST) nodes
class Program:
    def __init__(self, statements):
        self.statements = statements

class Let:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class Var:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class Function:
    def __init__(self, name, params, return_type, body):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body

class GpuFunction:
    def __init__(self, name, params, return_type, body):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body

class Parameter:
    def __init__(self, name, type):
        self.name = name
        self.type = type

class Expression:
    pass

class BinOp(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Number(Expression):
    def __init__(self, value):
        self.value = value

class String(Expression):
    def __init__(self, value):
        self.value = value

class Bool(Expression):
    def __init__(self, value):
        self.value = value

class Identifier(Expression):
    def __init__(self, name):
        self.name = name

# Grammar rules
def p_program(p):
    'program : statement_list'
    p[0] = Program(p[1])

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : variableDeclaration
                 | functionDeclaration
                 | actorDeclaration
                 | serviceDeclaration
                 | gpuFunctionDeclaration
                 | expressionStatement
                 | importStatement'''
    p[0] = p[1]

def p_importStatement(p):
    'importStatement : IMPORT modulePath SEMICOLON'
    p[0] = ('import', p[2])

def p_modulePath(p):
    'modulePath : ID (DOT ID)*'
    p[0] = '.'.join(p[1:])

def p_variableDeclaration(p):
    '''variableDeclaration : LET ID ASSIGN expression SEMICOLON
                           | VAR ID ASSIGN expression SEMICOLON'''
    if p[1] == 'let':
        p[0] = Let(p[2], p[4])
    else:
        p[0] = Var(p[2], p[4])

def p_functionDeclaration(p):
    'functionDeclaration : FN ID LPAREN parameterList RPAREN ARROW type LBRACE statementList RBRACE'
    p[0] = Function(p[2], p[4], p[7], p[9])

def p_gpuFunctionDeclaration(p):
    'gpuFunctionDeclaration : GPU FN ID LPAREN parameterList RPAREN ARROW type LBRACE statementList RBRACE'
    p[0] = GpuFunction(p[3], p[5], p[8], p[10])

def p_templateParameters(p):
    'templateParameters : ID (COMMA ID)*'
    p[0] = [p[1]] + p[2]

def p_parameterList(p):
    '''parameterList : parameterList COMMA parameter
                     | parameter
                     | empty'''
    if len(p) == 2:
        p[0] = [] if p[1] is None else [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_parameter(p):
    'parameter : ID COLON type'
    p[0] = Parameter(p[1], p[3])

def p_type(p):
    '''type : INT_TYPE
            | FLOAT_TYPE
            | STRING_TYPE
            | BOOL_TYPE
            | VOID_TYPE
            | CHANNEL_TYPE LT type GT
            | ID (LT type (COMMA type)* GT)?'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f'Channel<{p[3]}>'

def p_expressionStatement(p):
    'expressionStatement : expression SEMICOLON'
    p[0] = p[1]

def p_expression(p):
    '''expression : primary
                  | expression binaryOperator expression
                  | ID LPAREN argumentList RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = BinOp(p[1], p[2], p[3])
    else:
        p[0] = ('call', p[1], p[3])

def p_primary(p):
    '''primary : ID
               | NUMBER
               | STRING
               | BOOL
               | LPAREN expression RPAREN'''
    if p[1] == '(':
        p[0] = p[2]
    else:
        if isinstance(p[1], str):
            p[0] = Identifier(p[1])
        elif isinstance(p[1], int):
            p[0] = Number(p[1])
        elif isinstance(p[1], bool):
            p[0] = Bool(p[1])

def p_argumentList(p):
    '''argumentList : expression (COMMA expression)*'''
    p[0] = [p[1]] + p[2]

def p_binaryOperator(p):
    '''binaryOperator : PLUS
                      | MINUS
                      | TIMES
                      | DIVIDE
                      | EQ
                      | NEQ
                      | LT
                      | GT
                      | LEQ
                      | GEQ'''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    p[0] = None

# Error rule for syntax errors
def p_error(p):
    print(f"Syntax error at '{p.value}'")

# Build the parser
parser = yacc.yacc()
