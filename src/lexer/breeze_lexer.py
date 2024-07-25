import ply.lex as lex

# List of token names
tokens = [
    'ID', 'NUMBER', 'STRING', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'ASSIGN', 'SEMICOLON', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'LT', 'GT', 'COMMA', 'COLON', 'CHANNEL', 'COMMENT'
]

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LT = r'<'
t_GT = r'>'
t_COMMA = r','
t_COLON = r':'
t_CHANNEL = r'<-'

# Regular expression for identifiers and reserved words
reserved = {
    'let': 'LET',
    'var': 'VAR',
    'fn': 'FN',
    'gpu': 'GPU',
    'actor': 'ACTOR',
    'service': 'SERVICE',
    'endpoint': 'ENDPOINT',
    'receive': 'RECEIVE',
    'case': 'CASE',
    'Int': 'INT_TYPE',
    'Float': 'FLOAT_TYPE',
    'String': 'STRING_TYPE',
    'Bool': 'BOOL_TYPE',
    'Void': 'VOID_TYPE',
    'channel': 'CHANNEL_TYPE',
}

tokens += list(reserved.values())

# Regular expression rules for complex tokens
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

# Define a rule for comments (to be ignored)
def t_COMMENT(t):
    r'//.*'
    pass

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
