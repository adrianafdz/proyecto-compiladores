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
dimension = ('1')
dim1 = None
dim2 = None
var_ctrl = None # para el for loop
var_ctrl_type = None

curr_dir = deque()
curr_func = deque()
constantes = tablaVars()

dirFuncG = None # directorio de funciones global
dirFuncObj = None # directorio de funciones de un objeto
check_obj = None
param_list = []
param_count = 0

def calc_size(dim): # calcular el tamaño de una variable
    if dim == None:
        return 1
    if len(dim) == 1:
        return int(dim[0])
    elif len(dim) == 2:
        return int(dim[1]) * int(dim[0])

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
    '''start : PROGRAM f_start ID f_prog ';' clases vars funciones MAIN f_main '(' ')' '{' estatutos '}' END f_end ';' '''

def p_f_start(p):
    "f_start :"
    global dirFuncG
    dirFuncG = dirFunc()
    curr_dir.append(dirFuncG)
    pilaSaltos.append(cuadruplos.get_cont())
    cuadruplos.add("GOTO", -1, -1, -1)

def p_f_prog(p):
    "f_prog :"
    curr_dir[-1].add_func(p[-1], cuadruplos.get_cont(), curr_tipo)
    curr_func.append(p[-1])

def p_f_main(p):
    "f_main :"
    cuadruplos.fill(pilaSaltos.pop(), cuadruplos.get_cont())

def p_f_end(p):
    "f_end : "
    global dirLocal, dirTemp
    # CALCULAR RECURSOS
    recursos = dirGlobal + (dirTemp - 7000)
    curr_dir[-1].add_resources(curr_func[-1], recursos)
    # print(curr_dir[-1])
    curr_dir[-1].delete_dir()
    curr_func.pop()

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
    global dirLocal
    curr_dir[-1].add_resources(curr_func[-1], dirLocal - 4000)
    curr_dir.append(dirFuncObj)
    dirLocal = 4000

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
    global dirLocal, dirTemp
    curr_dir[-1].delete_var_table(curr_func[-1])
    # CALCULAR RECURSOS
    recursos = (dirLocal - 4000) + (dirTemp - 7000)
    curr_dir[-1].add_resources(curr_func[-1], recursos)
    curr_func.pop()

    cuadruplos.add("ENDFUNC", -1, -1, -1) # cuadruplo para regresar al programa principal

    dirLocal = 4000 # reinicia direcciones locales y temporales
    dirTemp = 7000

def p_vars(p):
    '''vars : vars DEF tipo dimension ':' lista_id ';'
            | vars DEF ID f_varsobj ':' lista_id_obj ';'
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
    dimension = ('1')

def p_cvars(p):
    '''cvars : cvars DEF tipo dimension ':' lista_id ';'
             | empty'''

def p_lista_id(p): 
    '''lista_id : ID f_vars
                | lista_id ',' ID f_vars'''
                
def p_f_vars(p):
    "f_vars :"
    global dimension, dirGlobal, dirLocal, found_error
    if len(curr_func) == 1: # esta en variables globales
        if dirGlobal == 4000:
            print("MEMORIA GLOBAL LLENA")
            found_error = True

        curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirGlobal)
        dirGlobal += calc_size(dimension)
    else:
        if dirLocal == 7000:
            print("MEMORIA LOCAL LLENA")
            found_error = True

        curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirLocal)
        dirLocal += calc_size(dimension)

    dimension = ('1')

def p_lista_id_obj(p): 
    '''lista_id_obj : ID f_vars_obj
                    | lista_id_obj ',' ID f_vars_obj'''

def p_f_vars_obj(p):
    "f_vars_obj :"
    global dirGlobal, dirLocal, found_error, dimension
    obj_size = curr_dir[0].get_resources(curr_tipo)

    if len(curr_func) == 1: # esta en variables globales
        if dirGlobal == 4000:
            print("MEMORIA GLOBAL LLENA")
            found_error = True

        curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirGlobal)
        dirGlobal += obj_size
    else:
        if dirLocal == 7000:
            print("MEMORIA LOCAL LLENA")
            found_error = True

        curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirLocal)
        dirLocal += obj_size

    dimension = ('1')

def p_dimension(p): 
    '''dimension : '[' NUM f_dim1 ']' f_onedim
                 | '[' NUM f_dim1 ']' '[' NUM f_dim2 ']' f_twodim
                 | empty'''

def p_f_dim1(p):
    "f_dim1 :"
    global dim1
    dim1 = p[-1]

def p_f_dim2(p):
    "f_dim2 :"
    global dim2
    dim2 = p[-1]

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
    global dirLocal
    curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirLocal)
    dirLocal += 1
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
    global found_error, param_list, param_count
    f_type, f_start = curr_dir[-1].get_func(p[-1])
    if f_type == -1:
        print("UNDECLARED FUNCTION, line", lexer.lineno)
        found_error = True
    else:
        cuadruplos.add("GOSUB", -1, -1, f_start)
        recursos = curr_dir[-1].get_resources(p[-1])
        param_list = curr_dir[-1].get_params(p[-1])
        cuadruplos.add("ERA", recursos, -1, -1)
        param_count = 0

def p_f_verify_func_composite(p):
    "f_verify_func_composite :"
    global found_error, param_list, param_count
    obj_type, obj_mem = curr_dir[0].get_var(curr_func[0], check_obj) # busca de qué tipo de objeto es la variable (busca en las variables globales)
    obj_funcs = curr_dir[0].get_dir_from_obj(obj_type) # trae el directorio de funciones de ese objeto
    f_type, f_start = obj_funcs.get_func(p[-1])

    if f_type == -1:
        print("UNDECLARED FUNCTION, line", lexer.lineno)
        found_error = True
    else:
        cuadruplos.add("GOSUB", -1, -1, f_start)
        recursos = obj_funcs.get_resources(p[-1])
        param_list = obj_funcs.get_params(p[-1])
        cuadruplos.add("ERA", recursos, -1, -1)
        param_count = 0

def p_args(p):
    '''args : args_list f_end_args
            | f_end_args'''

def p_args_list(p):
    '''args_list : expresion f_arg
                 | args_list ',' expresion f_arg'''

def p_f_arg(p):
    "f_arg :"
    global found_error, param_count
    
    arg = pilaOperandos.pop()
    arg_type = pilaTipos.pop()

    param_count += 1

    if param_count > len(param_list):
        print("ERROR: Too many arguments, line", lexer.lineno)
    else:
        if arg_type == param_list[param_count-1]:
            cuadruplos.add("PARAMETER", arg, param_count, -1)
        else:
            print("ERROR: Wrong argument type, line", lexer.lineno, ". Argument", param_count)
            found_error = True

def p_f_end_args(p):
    "f_end_args :"
    global found_error
    if param_count < len(param_list):
        print("ERROR: Missing arguments, line", lexer.lineno)
        found_error = True

def p_asignacion(p):
    '''asignacion : var '=' f_oper expresion ';' '''
    cuadruplos.add(pilaOperadores.pop(), pilaOperandos.pop(), -1, pilaOperandos.pop())

def p_var(p):
    '''var : ID f_varobj ':' ID f_verify_type_composite indexacion
           | ID f_verify_type indexacion'''

def p_indexacion(p):
    '''indexacion : '[' expresion ']'
                 | '[' expresion ']' '[' expresion ']'
                 | empty'''

def p_f_varobj(p):
    "f_varobj :"
    global check_obj
    check_obj = p[-1]

def p_f_verify_type(p):
    "f_verify_type :"
    global found_error
    var_type, var_mem = curr_dir[-1].get_var(curr_func[-1], p[-1])
    
    if var_type == -1:
        if len(curr_func) > 1: # la estaba buscando localmente, ahora buscar global
            var_type, var_mem = curr_dir[0].get_var(curr_func[0], p[-1])
             
        if var_type == -1:
            print("UNDECLARED VARIABLE", p[-1], ", line:", lexer.lineno) # local
            found_error = True
        else:
            pilaOperandos.append(var_mem)
            pilaTipos.append(var_type)
    else:
        pilaOperandos.append(var_mem)
        pilaTipos.append(var_type)

def p_f_verify_type_composite(p):
    "f_verify_type_composite :"
    global found_error
    obj_type, obj_mem = curr_dir[0].get_var(curr_func[-1], check_obj) # busca de qué tipo de objeto es la variable (busca en las variables globales)
    
    obj_vars = curr_dir[0].get_vars_from_obj(obj_type) # trae la tabla de variables de ese objeto
    var_type, var_mem = obj_vars.get_var(p[-1]) # trae el tipo y la memoria del atributo

    # la direccion real de la memoria depende de la memoria base del objeto, como si los atributos estuvieran en un arreglo
    real_mem = obj_mem + (var_mem - 4000)

    if var_type == -1:
        print("UNDECLARED VARIABLE", p[-1], ", line:", lexer.lineno)
        found_error = True
    else:
        pilaOperandos.append(real_mem)
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
    '''condicion : IF '(' expresion ')' f_if THEN '{' estatutos '}' condicionp f_endif'''

def p_condicionp(p):
    '''condicionp : ELSE f_else '{' estatutos '}'
                  | empty '''

def p_f_if(p):
    "f_if :"
    exp_type = pilaTipos.pop()
    if exp_type == 0:
        res = pilaOperandos.pop()
        cuadruplos.add("GOTOF", res, -1, -1)
        pilaSaltos.append(cuadruplos.get_cont() - 1)
    else:
        print("ERROR: Type mismatch, line", lexer.lineno)

def p_f_endif(p):
    "f_endif :"
    fin = pilaSaltos.pop()
    cuadruplos.fill(fin, cuadruplos.get_cont())

def p_f_else(p):
    "f_else :"
    cuadruplos.add("GOTO", -1, -1, -1)
    falso = pilaSaltos.pop()
    pilaSaltos.append(cuadruplos.get_cont() - 1)
    cuadruplos.fill(falso, cuadruplos.get_cont())

def p_while(p):
    '''while : WHILE f_while '(' expresion f_exprwhile ')' DO '{' estatutos '}' f_endwhile '''

def p_f_while(p):
    "f_while :"
    pilaSaltos.append(cuadruplos.get_cont())

def p_f_exprwhile(p):
    "f_exprwhile :"
    exp_type = pilaTipos.pop()
    if exp_type == 0:
        res = pilaOperandos.pop()
        cuadruplos.add("GOTOF", res, -1, -1)
        pilaSaltos.append(cuadruplos.get_cont() - 1)
    else:
        print("ERROR: Type mismatch, line", lexer.lineno)

def p_f_endwhile(p):
    "f_endwhile :"
    fin = pilaSaltos.pop()
    ret = pilaSaltos.pop()
    cuadruplos.add("GOTO", -1, -1, ret)
    cuadruplos.fill(fin, cuadruplos.get_cont())

def p_for(p):
    '''for : FOR expresion f_for_start TO expresion f_for_to '{' estatutos '}' f_for_end '''

def p_f_for_start(p):
    "f_for_start :"
    global found_error, var_ctrl, var_ctrl_type

    if pilaTipos.pop() == 0: # la expresion resulta en numerico
        var_ctrl = pilaOperandos.pop()
    else:
        found_error = True
        print("ERROR: Type mismatch, line", lexer.lineno)

def p_f_for_to(p):
    "f_for_to :"
    global found_error, dirTemp

    exp_type = pilaTipos.pop()
    exp = pilaOperandos.pop()
    if exp_type == 0:
        pilaSaltos.append(cuadruplos.get_cont()) # para el retorno
        cuadruplos.add(">", var_ctrl, exp, dirTemp) # el for será inclusive
        cuadruplos.add("GOTOV", dirTemp, -1, -1)
        pilaSaltos.append(cuadruplos.get_cont() - 1) # GotoV
        dirTemp += 1
    else:
        found_error = True
        print("ERROR: Type mismatch, line", lexer.lineno)

def p_f_for_end(p):
    "f_for_end :" 
    global dirTemp
    cuadruplos.add("+", var_ctrl, "1", dirTemp) # sumar 1 a la var de control
    cuadruplos.add("=", dirTemp, -1, var_ctrl) # asignar el resultado a la var de control
    dirTemp += 1

    fin = pilaSaltos.pop()
    retorno = pilaSaltos.pop()
    cuadruplos.add("GOTO", -1, -1, retorno)
    cuadruplos.fill(fin, cuadruplos.get_cont())

def p_to_num(p):
    '''to_num : TO_NUMBER '(' STR ')' 
              | TO_NUMBER '(' var ')' '''
    global dirTemp, found_error
    if pilaTipos[-1] == 1:
        cuadruplos.add("CNUM", pilaOperandos.pop(), -1, dirTemp)
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
        cuadruplos.add("CSTR", pilaOperandos.pop(), -1, dirTemp)
        pilaTipos.pop()
        pilaOperandos.append(dirTemp)
        pilaTipos.append(1)
        dirTemp += 1
    else:
        print("ERROR: Type Mismatch")
        found_error = True

def p_input(p):
    '''input : INPUT '(' var ')' '''
    cuadruplos.add("READ", -1, -1, pilaOperandos.pop())

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
    
    cuadruplos.add("PRINT", -1, -1, pilaOperandos.pop())

def p_return(p):
    '''return : RET '(' expresion ')' '''
    global found_error
    res = pilaOperandos.pop()
    res_type = pilaTipos.pop()

    f_type, f_start = curr_dir[-1].get_func(curr_func[-1])

    if res_type == f_type:
        cuadruplos.add("RET", -1, -1, res)
    else:
        print("ERROR: Type Mismatch, line", lexer.lineno)
        found_error = True

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
cuadruplos.generate_file()