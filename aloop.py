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
    'nothing' : 'NOTHING',
    'to_number' : 'TO_NUMBER',
    'to_string' : 'TO_STRING',
    'input' : 'INPUT',
    'print' : 'PRINT'
}

literals = ['=', ';', ':', ',', '{', '}', '(', ')', '[', ']', '&']

tokens = tokens + list(reserved.values())

t_ignore  = ' \t'
t_COMP = r'(<>|<|>|==)'
t_OPTERM = r'\+|\-'
t_OPFACT = r'\*|\/'
t_STR = r'".*"'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_NUM(t):
    r'[0-9]+(\.[0-9]+)?'
    t.value = float(t.value)
    return t

# Track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

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

def p_start(p):
    '''start : PROGRAM ID ';' clases vars funciones MAIN '(' ')' '{' estatutos '}' END ';' '''

def p_clases(p):
    '''clases : clases clase
              | empty'''

def p_clase(p):
    '''clase : TYPE ID ':' ID '{' cvars funciones '}' 
             | TYPE ID '{' cvars funciones '}' '''

def p_funciones(p):
    '''funciones : funciones funcion
                  | empty'''

def p_funcion(p):
    '''funcion : FUNC ID '(' params ')' ':' tipo '{' vars estatutos '}'
               | FUNC ID '(' params ')' ':' NOTHING '{' vars estatutos '}' '''

def p_vars(p):
    '''vars : vars DEF tipo dimension ':' lista_id ';'
            | vars DEF ID ':' lista_id ';'
            | empty'''

def p_cvars(p):
    '''cvars : cvars DEF tipo dimension ':' lista_id ';'
             | empty'''

def p_lista_id(p): 
    '''lista_id : ID 
                | lista_id ',' ID'''

def p_dimension(p): 
    '''dimension : '[' expresion ']' 
                 | '[' expresion ']' '[' expresion ']' 
                 | empty'''

def p_tipo(p): 
    '''tipo : NUMBER 
            | STRING'''

def p_params(p): 
    '''params : pparams 
              | empty'''

def p_pparams(p):
    '''pparams : tipo ID
               | pparams ',' tipo ID'''

def p_estatutos(p):
    '''estatutos : estatutos estatuto 
                 | empty'''

def p_estatuto(p):
    '''estatuto : asignacion 
                | while 
                | for 
                | condicion 
                | CALL call_func ';' '''

def p_call_func(p):
    '''call_func : func
                 | input 
                 | write 
                 | to_num 
                 | to_str
                 | return '''

def p_func(p):
    '''func : ID  '(' args ')'
            | ID  ':' ID '(' args ')' '''

def p_args(p):
    '''args : args_list
            | empty'''

def p_args_list(p):
    '''args_list : expresion 
                 | args_list ',' expresion'''

def p_asignacion(p):
    '''asignacion : var '=' expresion ';' '''

def p_var(p):
    '''var : ID ':' ID dimension
           | ID dimension'''

def p_expresion(p):
    '''expresion : exp
                 | expresion COMP exp'''

def p_exp(p):
    '''exp : term
           | exp OPTERM term'''

def p_term(p):
    '''term : fact
            | term OPFACT fact'''

def p_fact(p):
    '''fact : '(' expresion ')'
            | var
            | NUM
            | OPTERM NUM
            | CALL call_func'''

def p_condicion(p):
    '''condicion : IF '(' expresion ')' THEN '{' estatutos '}' condicionp'''

def p_condicionp(p):
    '''condicionp : ELSE '{' estatutos '}'
                  | empty '''

def p_while(p):
    '''while : WHILE '(' expresion ')' DO '{' estatutos '}' '''

def p_for(p):
    '''for : FOR expresion TO expresion '{' estatutos '}' '''

def p_to_num(p):
    '''to_num : TO_NUMBER '(' STR ')' 
              | TO_NUMBER '(' var ')' '''

def p_to_str(p):
    '''to_str : TO_STRING '(' expresion ')' '''

def p_input(p):
    '''input : INPUT '(' var ')' '''

def p_write(p):
    '''write : PRINT '(' write_list ')' '''

def p_write_list(p):
    '''write_list : write_list '&' write_listp
                  | write_listp'''

def p_write_listp(p):
    '''write_listp : STR 
                   | var 
                   | CALL to_str'''

def p_return(p):
    '''return : RET '(' expresion ')' '''

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
f = open("./test/" + nombre, "r")
# f = open(nombre, "r")

s = f.read()

if (len(s) > 0):
    empty_file = False

parser.parse(s)