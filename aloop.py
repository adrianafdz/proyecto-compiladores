import ply.lex as lex
import ply.yacc as yacc
from collections import deque
from dirFunc import dirFunc
from cuadruplos import Cuadruplos
from cuboSemantico import cuboSemantico
from tablaVars import tablaVars

found_error = False
empty_file = True

dirGlobal = 0 # 0 - 3999
dirLocal = 4000 # 4000 - 6999
dirTemp = 7000 # 7000 - 9999
dirConst = 10000 # 10000 - 13999

cuadruplos = Cuadruplos()
cubo = cuboSemantico()
pilaOperandos = deque()
pilaOperadores = deque()
pilaTipos = deque()
pilaSaltos = deque()

tipos = [0, 1, 2] # number, string, nothing
curr_tipo = 0
dimension = None
dim1 = None
dim2 = None

curr_dir = deque()
curr_func = deque()

dirFuncG = None # directorio de funciones global
dirFuncObj = None # directorio de funciones de un objeto
check_obj = None
constantes = tablaVars()

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
t_NUM = r'[0-9]+(\.[0-9]+)?'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
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
    '''start : PROGRAM f_start ID f_prog ';' clases vars funciones MAIN '(' ')' '{' estatutos '}' END f_end ';' '''

def p_f_start(p):
    "f_start :"
    global dirFuncG
    dirFuncG = dirFunc()
    curr_dir.append(dirFuncG)

def p_f_prog(p):
    "f_prog :"
    curr_dir[-1].add_func(p[-1], cuadruplos.get_cont(), curr_tipo)
    curr_func.append(p[-1])

def p_f_end(p):
    "f_end : "
    global dirLocal
    print(curr_dir[-1])
    curr_dir[-1].delete_dir()
    curr_func.pop()
    dirLocal = 7000 # reinicia

def p_clases(p):
    '''clases : clases clase
              | empty'''

def p_clase(p):
    '''clase : TYPE ID f_startclass ':' ID f_clasepadre '{' cvars f_cvars funciones '}' f_endclass 
             | TYPE ID f_startclass '{' cvars f_cvars funciones '}' f_endclass '''

def p_f_startclass(p):
    "f_startclass :"
    global dirFuncObj
    curr_dir[-1].add_func(p[-1], cuadruplos.get_cont(), 3)
    curr_func.append(p[-1])
    dirFuncObj = curr_dir[-1].create_dir_for_obj(curr_func[-1])

def p_f_clasepadre(p):
    "f_clasepadre :"
    global dirFuncObj
    curr_dir[-1].copy_class_to(p[-1], curr_func[-1])
    dirFuncObj = curr_dir[-1].get_dir_from_obj(curr_func[-1])

def p_f_cvars(p):
    "f_cvars :"
    curr_dir.append(dirFuncObj)

def p_f_endclass(p):
    "f_endclass :"
    curr_dir.pop()
    curr_func.pop()

def p_funciones(p):
    '''funciones : funciones funcion
                  | empty'''

def p_funcion(p):
    '''funcion : FUNC ID f_startfunc '(' params ')' ':' tipo f_tipofunc '{' vars estatutos '}' f_endfunc
               | FUNC ID f_startfunc '(' params ')' ':' NOTHING f_nothing f_tipofunc '{' vars estatutos '}' f_endfunc '''

def p_f_startfunc(p):
    "f_startfunc :"
    curr_dir[-1].add_func(p[-1], cuadruplos.get_cont())
    curr_func.append(p[-1])

def p_f_nothing(p):
    "f_nothing :"
    global curr_tipo
    curr_tipo = 2

def p_f_tipofunc(p):
    "f_tipofunc :"
    curr_dir[-1].update_func_type(curr_func[-1], curr_tipo)

def p_f_endfunc(p):
    "f_endfunc :"
    curr_dir[-1].delete_var_table(curr_func[-1])
    curr_func.pop()
    cuadruplos.add("GOBACK", None, None, None) # cuadruplo para regresar al programa principal

def p_vars(p):
    '''vars : vars DEF tipo dimension ':' lista_id ';'
            | vars DEF ID f_varsobj ':' lista_id ';'
            | empty'''

def p_f_varsobj(p):
    "f_varsobj :"
    global curr_tipo, dimension, found_error
    tipo, mem = curr_dir[0].get_func(p[-1])
    if tipo == 3:
        curr_tipo = p[-1]
    else:
        print("UNDECLARED OBJECT, line ", lexer.lineno)
        found_error = True
    dimension = None

def p_cvars(p):
    '''cvars : cvars DEF tipo dimension ':' lista_id ';'
             | empty'''

def p_lista_id(p): 
    '''lista_id : ID f_vars
                | lista_id ',' ID f_vars'''
                
def p_f_vars(p):
    "f_vars :"
    global dimension, dirGlobal, dirLocal, found_error
    if len(curr_dir) == 0: # esta en variables globales
        if dirGlobal == 4000:
            print("MEMORIA GLOBAL LLENA")
            found_error = True

        curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirGlobal)
        dirGlobal += 1
    else:
        if dirLocal == 7000:
            print("MEMORIA LOCAL LLENA")
            found_error = True

        curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirLocal)
        dirLocal += 1

    dimension = None

def p_dimension(p): 
    '''dimension : '[' expresion f_dim1 ']' f_onedim
                 | '[' expresion f_dim1 ']' '[' expresion f_dim2 ']' f_twodim
                 | empty'''

def p_f_dim1(p):
    "f_dim1 :"
    global dim1
    dim1 = pilaOperandos.pop()

def p_f_dim2(p):
    "f_dim2 :"
    global dim2
    dim2 = pilaOperandos.pop()

def p_f_onedim(p):
    "f_onedim :"
    global dimension, dim1, dim2
    dimension = (dim1)
    dim1 = None
    dim2 = None

def p_f_twodim(p):
    "f_twodim :"
    global dimension, dim1, dim2
    dimension = (dim1, dim2)
    dim1 = None
    dim2 = None

def p_tipo(p): 
    '''tipo : NUMBER 
            | STRING'''
    global curr_tipo
    if p[1] == 'number':
        curr_tipo = 0
    elif p[1] == 'string':
        curr_tipo = 1

def p_params(p): 
    '''params : pparams 
              | empty'''

def p_pparams(p):
    '''pparams : tipo ID f_param
               | pparams ',' tipo ID f_param'''

def p_f_param(p):
    "f_param :"
    curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, 0)
    curr_dir[-1].add_param(curr_func[-1], curr_tipo)

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
    '''func : ID  f_verify_func '(' args ')'
            | ID  f_varobj ':' ID f_verify_func_composite '(' args ')' '''

def p_f_verify_func(p):
    "f_verify_func :"
    global found_error
    f_type, f_start = curr_dir[0].get_func(p[-1])
    if f_type == -1:
        print("UNDECLARED FUNCTION, line", lexer.lineno)
        found_error = True
    else:
        cuadruplos.add("GOTOSUB", None, None, f_start)

def p_f_verify_func_composite(p):
    "f_verify_func_composite :"
    global found_error
    obj_type, obj_mem = curr_dir[0].get_var(curr_func[0], check_obj) # busca de qué tipo de objeto es la variable (busca en las variables globales)
    obj_funcs = curr_dir[0].get_dir_from_obj(obj_type) # trae el directorio de funciones de ese objeto
    f_type, f_start = obj_funcs.get_func(p[-1])

    if f_type == -1:
        print("UNDECLARED FUNCTION, line", lexer.lineno)
        found_error = True
    else:
        cuadruplos.add("GOTOSUB", None, None, f_start)

def p_args(p):
    '''args : args_list
            | empty'''

def p_args_list(p):
    '''args_list : expresion 
                 | args_list ',' expresion'''

def p_asignacion(p):
    '''asignacion : var '=' f_oper expresion ';' '''
    cuadruplos.add(pilaOperadores.pop(), pilaOperandos.pop(), None, pilaOperandos.pop())

def p_var(p):
    '''var : ID f_varobj ':' ID f_verify_type_composite dimension
           | ID f_verify_type dimension'''

def p_f_varobj(p):
    "f_varobj :"
    global check_obj
    check_obj = p[-1]

def p_f_verify_type(p):
    "f_verify_type :"
    global found_error
    var_type, var_mem = curr_dir[-1].get_var(curr_func[-1], p[-1])
    
    if var_type == -1:
        print("UNDECLARED VARIABLE", p[-1], ", line:", lexer.lineno)
        found_error = True
    else:
        pilaOperandos.append(var_mem)
        pilaTipos.append(var_type)

def p_f_verify_type_composite(p):
    "f_verify_type_composite :"
    global found_error
    obj_type, obj_mem = curr_dir[0].get_var(curr_func[0], check_obj) # busca de qué tipo de objeto es la variable (busca en las variables globales)
    obj_vars = curr_dir[0].get_vars_from_obj(obj_type) # trae la tabla de variables de ese objeto
    var_type, var_mem = obj_vars.get_var(p[-1]) # trae el tipo y la memoria del atributo

    if var_type == -1:
        print("UNDECLARED VARIABLE", p[-1], ", line:", lexer.lineno)
        found_error = True
    else:
        pilaOperandos.append(var_mem)
        pilaTipos.append(var_type)

def p_expresion(p):
    '''expresion : exp
                 | expresion COMP f_oper exp f_expres'''

def p_f_expres(p):
    "f_expres :"
    global dirTemp, found_error
    if len(pilaOperadores) > 0 and pilaOperadores[-1] in ['<>', '<', '>', '==']:
        oper = pilaOperadores.pop()
        ro = pilaOperandos.pop()
        lo = pilaOperandos.pop()
        rt = pilaTipos.pop()
        lt = pilaTipos.pop()
        tres = cubo.check(oper, lt, rt)

    if tres == -1:
        print("ERROR: Type Mismatch")
        found_error = True
    else:
        if dirTemp == 10000:
            print("MEMORIA TEMPORAL LLENA")
        res = dirTemp
        dirTemp += 1
        cuadruplos.add(oper, lo, ro, res)

        pilaOperandos.append(res)
        pilaTipos.append(tres)  

def p_exp(p):
    '''exp : term
           | exp OPTERM f_oper term f_exp'''

# Funcion semantica - resolver operaciones + -
def p_f_exp(p):
    "f_exp :"
    global dirTemp, found_error
    if len(pilaOperadores) > 0 and len(pilaOperandos) > 1 and pilaOperadores[-1] in '-+':
        ro = pilaOperandos.pop()
        rt = pilaTipos.pop()
        lo = pilaOperandos.pop()
        lt = pilaTipos.pop()
        oper = pilaOperadores.pop()
        tres = cubo.check(oper, rt, lt)

        if tres == -1:
            print("ERROR: Type Mismatch")
            found_error = True
        else:
            if dirTemp == 10000:
                print("MEMORIA TEMPORAL LLENA")
            res = dirTemp
            dirTemp += 1
            cuadruplos.add(oper, lo, ro, res)

            pilaOperandos.append(res)
            pilaTipos.append(tres)  

def p_term(p):
    '''term : fact
            | term OPFACT f_oper fact f_term'''

# Funcion semantica - resolver operaciones + /
def p_f_term(p):
    "f_term :"
    global dirTemp, found_error
    if len(pilaOperadores) > 0 and len(pilaOperandos) > 1 and pilaOperadores[-1] in '*/':
        ro = pilaOperandos.pop()
        rt = pilaTipos.pop()
        lo = pilaOperandos.pop()
        lt = pilaTipos.pop()
        oper = pilaOperadores.pop()
        tres = cubo.check(oper, rt, lt)

        if tres == -1:
            print("ERROR: Type Mismatch")
            found_error = True
        else:
            if dirTemp == 10000:
                print("MEMORIA TEMPORAL LLENA")
            res = dirTemp
            dirTemp += 1
            cuadruplos.add(oper, lo, ro, res)

            pilaOperandos.append(res)
            pilaTipos.append(tres)      

# Funcion semantica para meter operador a la pilaOperadores
def p_f_oper(p):
    "f_oper :"
    pilaOperadores.append(p[-1])

def p_fact(p):
    '''fact : '(' lparen expresion ')' rparen
            | var
            | NUM f_fact
            | OPTERM NUM
            | CALL call_func'''
    global dirConst
    if p[1] == '-':
        pilaTipos.append(0)
        if not constantes.check_var("-" + p[2]):
            constantes.add_var("-" + p[2], 0, None, dirConst)
            pilaOperandos.append(dirConst)
            dirConst += 1
        else:
            var_tipo, var_mem = constantes.get_var("-" + p[2])
            pilaOperandos.append(var_mem)
    elif p[1] == '+':
        pilaTipos.append(0)
        if not constantes.check_var(p[2]):
            constantes.add_var(p[2], 0, None, dirConst)
            pilaOperandos.append(dirConst)
            dirConst += 1
        else:
            var_tipo, var_mem = constantes.get_var(p[2])
            pilaOperandos.append(var_mem)

def p_lparen(p):
    "lparen :"
    pilaOperadores.append(p[-1])

def p_rparen(p):
    "rparen :"
    pilaOperadores.pop()

def p_f_fact(p):
    "f_fact :"
    global dirConst
    pilaTipos.append(0)

    if not constantes.check_var(p[-1]):
        constantes.add_var(p[-1], 0, None, dirConst)
        pilaOperandos.append(dirConst)
        dirConst += 1
    else:
        var_tipo, var_mem = constantes.get_var(p[-1])
        pilaOperandos.append(var_mem)

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
    global dirTemp, found_error
    if pilaTipos[-1] == 1:
        cuadruplos.add("CNUM", pilaOperandos.pop(), None, dirTemp)
        pilaTipos.pop()
        pilaOperandos.append(dirTemp)
        pilaTipos.append(0)
        dirTemp += 1
    else:
        print("ERROR: Type Mismatch")
        found_error = True

def p_to_str(p):
    '''to_str : TO_STRING '(' expresion ')' '''
    global dirTemp, found_error
    if pilaTipos[-1] == 0:
        cuadruplos.add("CSTR", pilaOperandos.pop(), None, dirTemp)
        pilaTipos.pop()
        pilaOperandos.append(dirTemp)
        pilaTipos.append(1)
        dirTemp += 1
    else:
        print("ERROR: Type Mismatch")
        found_error = True

def p_input(p):
    '''input : INPUT '(' var ')' '''
    cuadruplos.add("READ", None, None, pilaOperandos.pop())

def p_write(p):
    '''write : PRINT '(' write_list ')' '''

def p_write_list(p):
    '''write_list : write_list '&' write_listp
                  | write_listp'''

def p_write_listp(p):
    '''write_listp : STR 
                   | var 
                   | CALL to_str'''
    if len(p) == 1:
        pilaOperandos.append(p[1])
    
    cuadruplos.add("PRINT", None, None, pilaOperandos.pop())

def p_return(p):
    '''return : RET '(' expresion ')' '''
    cuadruplos.add("RET", None, None, pilaOperandos.pop())

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

print("\nCuadruplos:")
print(cuadruplos)