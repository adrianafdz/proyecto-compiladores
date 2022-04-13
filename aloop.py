import ply.lex as lex
import ply.yacc as yacc

found_error = False
empty_file = True

####################################################
# LEX (scanner)

tokens = [
   'ID',
   'NUM',
   'STR',
   'COMP',
   'OPTERM',
   'OPFACT'
]

reserved = {
    'program' : 'PROGRAM',
    'main' : 'MAIN',
    'end' : 'END',
    'type' : 'TYPE',
    'def' : 'DEF',
    'func' : 'FUNC',
    'ret' : 'RET',
    'call' : 'CALL',
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'do' : 'DO',
    'for' : 'FOR',
    'to' : 'TO',
    'number' : 'NUMBER',
    'string' : 'STRING',
    'nothing' : 'NOTHING',Z
    'to_number' : 'TO_NUMBER',
    'to_string' : 'TO_STRING',
    'input' : 'INPUT',
    'print' : 'PRINT'
}

literals = ['=', ';', ':', ',', '{', '}', '(', ')', '[', ']']

tokens = tokens + list(reserved.values())

t_ignore  = ' \t'
t_TOSTR = r'\.string'
t_COMP = r'(<>|<|>|==)'
t_OPTERM = r'\+|\-'
t_OPFACT = r'\*|\/'
t_STR = r'".*"'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_NUM(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

# Lexical error handling rule
def t_error(t):
    global found_error
    found_error = True
    print("Illegal character ", t.value[0], "at line", t.lineno)
    t.lexer.skip(1)

# End of file rule
def t_eof(t):
    if empty_file: print("Empty file")
    if not found_error and not empty_file: print("No errors found") 

####################################################
# YACC (parser)

# GRAMATICA
# start -> PROGRAM ID ';' clases vars funciones MAIN '(' ')' '{' estatutos '}' END ';'

# clases -> clases clase
#         | empty

# clase -> TYPE ID ':' ID '{' cvars funciones '}' 
#       | TYPE ID '{' cvars funciones '}'

# funciones -> funciones funcion 
#           | empty

# funcion -> FUNC ID '(' params ')' ':' tipo '{' vars estatutos '}'
#          | FUNC ID '(' params ')' ':' NOTHING '{' vars estatutos '}'

# vars -> vars DEF tipo dimension ':' lista_id ';'
#       | vars DEF tipo ID ':' lista_id ';'
#       | empty

# cvars -> cvars DEF tipo dimension ':' lista_id ';'
#        | empty

# lista_id -> ID | lista_id ',' ID

# dimension -> '[' expresion ']' | '[' expresion ']' '[' expresion ']' | empty

# tipo -> NUMBER | STRING

# params -> pparams | empty

# pparams -> TIPO ID
#          | pparams ',' TIPO ID

# estatutos -> estatutos estatuto | empty

# estatuto -> asignacion | while | for | condicion | call_func

# call_func -> func | print | write | to_num | to_str

# func -> CALL ID  '(' args ')' ';'
#       | CALL ID  ':' ID '(' args ')' ';'

# args -> expresion 
#       | args ',' expresion

# asignacion -> var '=' expresion ';'

# var -> ID ':' ID dimension
# var -> ID dimension

# expresion -> exp
#           | expresion COMP exp

# exp -> term
#       | exp OPTERM term

# term -> fact
#       | term OPTERM fact

# fact -> '(' expresion ')'
#       | var
#       | NUM
#       | call_func

# condicion -> IF '(' expresion ')' THEN '{' estatutos '}' condicionp

# condicionp -> ELSE '{' estatutos '}'

# while -> WHILE '(' expresion ')' DO '{' estatutos '}'

# for -> FOR expresin TO expresion '{' estatutos '}'

# to_num -> TO_NUMBER '(' STR ')' ';'
#         | TO_NUMBER '(' VAR ')' ';'

# to_str -> TO_STRING '(' expresion ')' ';'

# input -> INPUT '(' VAR ')' ';'

# write -> PRINT '(' write_list ')' ';'

# write_list -> write_list '&' write_listp 
#             | write_listp

# write_listp -> str | var | to_str

def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    global found_error
    found_error = True
    if p:
         print("Syntax error at token", p.type, "line", p.lineno)
         parser.errok()
    else:
         print("Syntax error at EOF")


###########################################
# MAIN

lexer = lex.lex()
parser = yacc.yacc(start='start')

nombre = input('Nombre del archivo: ')
print("")
f = open(nombre, "r")
s = f.read()

if (len(s) > 0):
    empty_file = False

parser.parse(s)