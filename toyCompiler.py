import sys
tokens = ( 'IDENTIFIER', 'LITERAL', 'PLUS', 'MINUS', 'TIMES', 'PAREN_OPEN', 'PAREN_CLOSE', 'SEMICOLON', 'EQ' )
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_LITERAL  = r'0|([1-9][0-9]*)'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_PAREN_OPEN  = r'\('
t_PAREN_CLOSE  = r'\)'
t_SEMICOLON  = r';'
t_EQ  = r'='
t_ignore = ' \n\t'
def t_error(t):
    raise ("Illegal character '%s'" % t.value[0])
import ply.lex as lex
lexer = lex.lex()

variables = { }

def p_program(t):
    'program : assignment program'
def p_program_stop(t):
    'program : assignment'

def p_assignment(t):
    'assignment : IDENTIFIER EQ expression SEMICOLON'
    variables[t[1]] = t[3]

def p_expression_plus(t):
    'expression : expression PLUS term'
    t[0] = t[1] + t[3]
def p_expression_minus(t):
    'expression : expression MINUS term'
    t[0] = t[1] - t[3]
def p_expression(t):
    'expression : term'
    t[0] = t[1]

def p_term_binop(t):
    'term : term TIMES fact'
    t[0] = t[1] * t[3]
def p_term(t):
    'term : fact'
    t[0] = t[1]

def p_fact_group(t):
    'fact : PAREN_OPEN expression PAREN_CLOSE'
    t[0] = t[2]
def p_fact_uplus(t):
    'fact : PLUS expression'
    t[0] = t[2]
def p_fact_uminus(t):
    'fact : MINUS expression'
    t[0] = -t[2]
def p_fact_literal(t):
    'fact : LITERAL'
    t[0] = int(t[1])
def p_fact_identifier(t):
    'fact : IDENTIFIER'
    try:
        t[0] = variables[t[1]]
    except LookupError:
        raise LookupError("Undeclared variable '%s'" % t[1])
        t[0] = 0

def p_error(t):
    raise SyntaxError("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

try:
    parser.parse("""
    x = 1;
    y = 2;
    z = ---(x+y)*(x+-y);

    
    
    """)
    for key, value in variables.items():
      print(key + " = " + str(value))
except (LookupError, SyntaxError) as e:
    print(e)
