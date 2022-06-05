from dimStructure import DimStructure
import ply.lex as lex
import ply.yacc as yacc
from collections import deque
from dirFunc import dirFunc
from cuadruplos import Cuadruplos
from cuboSemantico import cuboSemantico
from tablaVars import tablaVars
from dirVirtuales import *

found_error = False
empty_file = True

# DIRECCIONES VIRTUALES
dirGlobalNum = BASE_DIRGLOBALNUM_LI
dirGlobalStr = BASE_DIRGLOBALSTR_LI

dirLocalNum = BASE_DIRLOCALNUM_LI
dirLocalStr = BASE_DIRLOCALSTR_LI

dirTempNum = BASE_DIRTEMPNUM_LI
dirTempStr = BASE_DIRTEMPSTR_LI
dirTempBool = BASE_DIRTEMPBOOL_LI
dirTempPointNum = BASE_DIRTEMPPOINTNUM_LI
dirTempPointStr = BASE_DIRTEMPPOINTSTR_LI

dirConstNum = BASE_DIRCONSTNUM_LI
dirConstStr = BASE_DIRCONSTSTR_LI

dirObjNum = BASE_DIROBJNUM_LI
dirObjStr = BASE_DIROBJSTR_LI

cuadruplos = Cuadruplos()
cubo = cuboSemantico()
pilaOperandos = deque()
pilaOperadores = deque()
pilaTipos = deque()
pilaSaltos = deque()
pilaDim = deque()

function_call = deque()
check_obj = deque()
param_list = deque()
param_count = deque()

tipos = [0, 1, 2, 3, 4, 5, 6 ] # number, string, bool, pointernum, pointerstr, objeto, nothing
curr_tipo = 6
dimension = None
dim1 = None
dim2 = None
var_ctrl = deque() # para el for loop
has_dim = False
dim = 1
base_dir = 0
is_class = False

curr_dir = deque()
curr_func = deque()
constantes = tablaVars()

dirFuncG = None # directorio de funciones global
dirFuncObj = None # directorio de funciones de un objeto

# Función que regresa la dirección de la constante value de tipo tipo type
def get_constante(value, type):
    if not constantes.check_var(value): # revisa si ya está registrada
        # si no, la registra con su nombre y tipo
        if type == 0:
            constantes.add_var(value, 0, None, dirConstNum)
            const_mem = dirConstNum
            add_memory("constantes", 0, 1) # actualiza el contador de constantes
        elif type == 1:
            constantes.add_var(value, 1, None, dirConstStr)
            const_mem = dirConstStr
            add_memory("constantes", 1, 1)
    else:
        # ya está registrada, así que solo la busca
        const_tipo, const_mem = constantes.get_var(value)

    return const_mem

# Función que devuelve un booleano que indica si ya se acabaron los registros según el tipo y el scope
def mem_available(scope, tipo):
    if scope == 'global':
        if tipo == 0: # number
            return dirGlobalNum <= BASE_DIRGLOBALNUM_LS
        elif tipo == 1: # string
            return dirGlobalStr <= BASE_DIRGLOBALSTR_LS
    elif scope == 'local':
        if tipo == 0: # number
            return dirLocalNum <= BASE_DIRLOCALNUM_LS
        elif tipo == 1: # string
            return dirLocalStr <= BASE_DIRLOCALSTR_LS
    elif scope == 'temp':
        if tipo == 0: # number
            return dirTempNum <= BASE_DIRTEMPNUM_LS
        elif tipo == 1: # string
            return dirTempStr <= BASE_DIRTEMPSTR_LS
        elif tipo == 2: # bool
            return dirTempBool <= BASE_DIRTEMPBOOL_LS
        elif tipo == 3: # point num
            return dirTempPointNum <= BASE_DIRTEMPPOINTNUM_LS
        elif tipo == 4: # point str
            return dirTempPointNum <= BASE_DIRTEMPPOINTSTR_LS
    elif scope == 'constantes':
        if tipo == 0:
            return dirConstNum <= BASE_DIRCONSTNUM_LS
        elif tipo == 1:
            return dirConstStr <= BASE_DIRCONSTSTR_LS
    elif scope == 'objeto':
        if tipo == 0:
            return dirObjNum <= BASE_DIROBJNUM_LS
        elif tipo == 1:
            return dirObjStr <= BASE_DIROBJSTR_LS
    return False

# Función para ir aumentando los contadores de las direcciones de memoria según el tipo y scope
def add_memory(scope, tipo, cant):
    global dirGlobalNum, dirGlobalStr, dirLocalNum, dirLocalStr, dirTempNum, dirTempStr, dirTempBool, dirTempPointNum, dirTempPointStr, dirConstNum, dirConstStr, dirObjNum, dirObjStr
    if scope == 'global':
        if tipo == 0: # number
            dirGlobalNum += cant
        elif tipo == 1: # string
            dirGlobalStr += cant
    elif scope == 'local':
        if tipo == 0: # number
            dirLocalNum += cant
        elif tipo == 1: # string
            dirLocalStr += cant
    elif scope == 'temp':
        if tipo == 0: # number
            dirTempNum += cant
        elif tipo == 1: # string
            dirTempStr += cant
        elif tipo == 2: # bool
            dirTempBool += cant
        elif tipo == 3: # point
            dirTempPointNum += cant
        elif tipo == 4: # point
            dirTempPointStr += cant
    elif scope == 'constantes':
        if tipo == 0:
            dirConstNum += cant
        elif tipo == 1:
            dirConstStr += cant
    elif scope == 'objeto':
        if tipo == 0:
            dirObjNum += cant
        elif tipo == 1:
            dirObjStr += cant

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

# palabras reservadas
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
t_ignore_COMMENT = r'\#.*'
t_COMP = r'(<>|<|>|==)'
t_OPTERM = r'\+|\-'
t_OPFACT = r'\*|\/'
t_STR = r'".*?"'

def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
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
    if not found_error and not empty_file: print("Compilation successful\n") 

####################################################
# YACC (parser)

# Inicio del lenguaje, estructura general
def p_start(p):
    '''start : PROGRAM f_start ID f_prog ';' clases vars funciones MAIN f_main '(' ')' '{' estatutos '}' END f_end ';' '''

def p_f_start(p):
    "f_start :"
    global dirFuncG
    dirFuncG = dirFunc() # crea el directorio de funciones
    curr_dir.append(dirFuncG) # lo agrega al stack de directorios
    pilaSaltos.append(cuadruplos.get_cont()) # guarda el cuadruplo para rellenarlo después
    cuadruplos.add("GOTO", -1, -1, -1) # genera el primer cuadruplo GOTO main

def p_f_prog(p):
    "f_prog :"
    curr_dir[-1].add_func(p[-1], cuadruplos.get_cont(), curr_tipo) # agrega el nombre del programa al directorio de funciones
    curr_func.append(p[-1]) # agrega el nombre del programa a la pila de funciones, la cual lleva registro de qué función se está compilando

def p_f_main(p):
    "f_main :"
    cuadruplos.fill(pilaSaltos.pop(), cuadruplos.get_cont()) # rellena el primer GOTO con el cuádruplo donde empieza el programa principal
    cuadruplos.add("ERA", curr_func[-1], -1, -1) # generar memoria global

def p_f_end(p):
    "f_end : "
    cuadruplos.add("END", -1, -1, -1)

    # Calcula recursos del main, acumulando globales y temporales
    recNum = dirGlobalNum + (dirTempNum - BASE_DIRTEMPNUM_LI)
    recStr = dirGlobalStr - BASE_DIRGLOBALSTR_LI + (dirTempStr - BASE_DIRTEMPSTR_LI)
    recBool = dirTempBool - BASE_DIRTEMPBOOL_LI
    recPointNum = dirTempPointNum - BASE_DIRTEMPPOINTNUM_LI
    recPointStr = dirTempPointStr - BASE_DIRTEMPPOINTSTR_LI

    curr_dir[-1].add_resources(curr_func[-1], [recNum, recStr, recBool, recPointNum, recPointStr])
    # print(curr_dir[-1])
    constantes.generate_file()
    curr_dir[0].generate_file()
    # print(constantes)
    curr_dir[-1].delete_dir() # elimina el directorio de funciones
    curr_func.pop() # quita el programa principal de la pila

def p_clases(p):
    '''clases : clases clase
              | empty'''

def p_clase(p):
    '''clase : TYPE ID f_startclass ':' ID f_clasepadre '{' cvars f_cvars funciones '}' f_endclass 
             | TYPE ID f_startclass '{' cvars f_cvars funciones '}' f_endclass '''

def p_f_startclass(p):
    "f_startclass :"
    global dirFuncObj, is_class
    curr_dir[-1].add_func(p[-1], cuadruplos.get_cont(), 5) # agrega el registro del objeto al directorio de funciones
    curr_func.append(p[-1])
    dirFuncObj = curr_dir[-1].create_dir_for_obj(curr_func[-1]) # crea un directorio de funciones para el objeto
    is_class = True

def p_f_clasepadre(p):
    "f_clasepadre :"
    global dirFuncObj
    tipo, mem = curr_dir[0].get_func(p[-1]) # revisa que exista ese id y que sí sea un objeto
    
    if tipo == 5: # objeto
        curr_dir[-1].copy_class_to(p[-1], curr_func[-1]) # copia todo el contenido del objeto padre
        rec = curr_dir[-1].get_resources(curr_func[-1]) # obtiene sus recursos para así seguir registrando a partir de los que ya se crearon
        dirFuncObj = curr_dir[-1].get_dir_from_obj(curr_func[-1])
        add_memory("objeto", 0, rec[0]) # actualiza los contadores según los recursos
        add_memory("objeto", 1, rec[1])
    else:
        print("ERROR: Undeclared object", p[-1], ", line:", lexer.lineno)
        found_error = True

# Declaración de variables dentro una clase o función (no permite declarar objetos)
def p_cvars(p):
    '''cvars : cvars DEF tipo dimension ':' lista_id ';' f_delete_dim
             | empty'''

def p_f_cvars(p):
    "f_cvars :"
    global is_class
    curr_dir.append(dirFuncObj)
    is_class = False

def p_f_endclass(p):
    "f_endclass :"
    global dirObjNum, dirObjStr
    # Calcula los recursos de la clase
    recNum = dirObjNum
    recStr = dirObjStr - BASE_DIROBJSTR_LI

    curr_dir.pop()
    curr_dir[-1].add_resources(curr_func[-1], [recNum, recStr, 0, 0, 0])
    curr_func.pop()

    # reestablece los contadores
    dirObjNum = BASE_DIROBJNUM_LI
    dirObjStr = BASE_DIROBJSTR_LI

def p_funciones(p):
    '''funciones : funciones funcion
                  | empty'''

def p_funcion(p):
    '''funcion : FUNC ID f_startfunc '(' params ')' ':' tipo f_tipofunc '{' cvars estatutos '}' f_endfunc
               | FUNC ID f_startfunc '(' params ')' ':' NOTHING f_nothing f_tipofunc '{' cvars estatutos '}' f_endfunc '''

def p_f_startfunc(p):
    "f_startfunc :"
    curr_dir[-1].add_func(p[-1], cuadruplos.get_cont()) # registra la función y en qué cuádruplo comienza
    curr_func.append(p[-1])

def p_f_nothing(p):
    "f_nothing :"
    global curr_tipo
    curr_tipo = 6

def p_f_tipofunc(p):
    "f_tipofunc :"
    curr_dir[-1].update_func_type(curr_func[-1], curr_tipo)

    if curr_tipo != 6:
        if len(curr_func) > 2: # se trata de metodo en un objeto
            if curr_tipo == 0:
                curr_dir[0].add_return_value(curr_func[-2], curr_func[-1], curr_tipo, dirObjNum)
            else:
                curr_dir[0].add_return_value(curr_func[-2], curr_func[-1], curr_tipo, dirObjStr)

            add_memory("objeto", curr_tipo, 1)
        else: # funcion global
            if curr_tipo == 0:
                curr_dir[0].add_return_value(curr_func[-2], curr_func[-1], curr_tipo, dirGlobalNum)
            else:
                curr_dir[0].add_return_value(curr_func[-2], curr_func[-1], curr_tipo, dirGlobalStr)

            add_memory("global", curr_tipo, 1)

def p_f_endfunc(p):
    "f_endfunc :"
    global dirLocalNum, dirLocalStr, dirTempNum, dirTempStr, dirTempBool, dirTempPointNum, dirTempPointStr
    curr_dir[-1].delete_var_table(curr_func[-1])
    # Calcula los recursos de la función según los registros locales y temporales
    recNum = dirLocalNum - BASE_DIRLOCALNUM_LI + (dirTempNum - BASE_DIRTEMPNUM_LI)
    recStr = dirLocalStr - BASE_DIRLOCALSTR_LI + (dirTempStr - BASE_DIRTEMPSTR_LI)
    recBool = dirTempBool - BASE_DIRTEMPBOOL_LI
    recPointNum = dirTempPointNum - BASE_DIRTEMPPOINTNUM_LI
    recPointStr = dirTempPointStr - BASE_DIRTEMPPOINTSTR_LI

    curr_dir[-1].add_resources(curr_func[-1], [recNum, recStr, recBool, recPointNum, recPointStr])
    curr_func.pop()

    cuadruplos.add("ENDFUNC", -1, -1, -1) # cuadruplo para regresar al programa principal

    # reestablece los contadores
    dirLocalNum = BASE_DIRLOCALNUM_LI
    dirLocalStr = BASE_DIRLOCALSTR_LI
    dirTempNum = BASE_DIRTEMPNUM_LI
    dirTempStr = BASE_DIRTEMPSTR_LI
    dirTempBool = BASE_DIRTEMPBOOL_LI
    dirTempPointNum = BASE_DIRTEMPPOINTNUM_LI 
    dirTempPointStr = BASE_DIRTEMPPOINTSTR_LI

# Declaración de variables globales (permite objetos)
def p_vars(p):
    '''vars : vars DEF tipo dimension ':' lista_id ';' f_delete_dim
            | vars DEF ID f_varsobj ':' lista_id_obj ';'
            | empty'''

def p_f_varsobj(p):
    "f_varsobj :"
    global curr_tipo, dimension, found_error
    tipo, mem = curr_dir[0].get_func(p[-1]) # revisa que exista ese id y que sí sea un objeto
    
    if tipo == 5: # objeto
        curr_tipo = p[-1]
    else:
        print("ERROR: Undeclared object", p[-1], ", line:", lexer.lineno)
        found_error = True

def p_lista_id(p): 
    '''lista_id : ID f_vars
                | lista_id ',' ID f_vars'''
                
def p_f_delete_dim(p):
    "f_delete_dim :"
    global dimension
    dimension = None

def p_f_vars(p):
    "f_vars :"
    global dimension, found_error
    # Registro de variables
    if is_class: # se están declarando atributos de un objeto
        if not mem_available("objeto", curr_tipo):
            print("ERROR: Stack overflow")
            found_error = True

        if curr_tipo == 0:
            curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirObjNum)
        elif curr_tipo == 1:
            curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirObjStr)

        if dimension is None:
            add_memory("objeto", curr_tipo, 1)
        else: # se declara un arreglo
            add_memory("objeto", curr_tipo, dimension.get_size())

    elif len(curr_func) == 1: # se están declarando variables globales
        if not mem_available("global", curr_tipo):
            print("ERROR: Stack overflow")
            found_error = True

        if curr_tipo == 0:
            curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirGlobalNum)
        elif curr_tipo == 1:
            curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirGlobalStr)
        
        if dimension is None:
            add_memory("global", curr_tipo, 1)
        else:
            add_memory("global", curr_tipo, dimension.get_size())
    else: # se están declarando variables dentro de una función
        if not mem_available("local", curr_tipo):
            print("ERROR: Stack overflow")
            found_error = True

        if curr_tipo == 0:
            curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirLocalNum)
        elif curr_tipo == 1:
            curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirLocalStr)

        if dimension is None:
            add_memory("local", curr_tipo, 1)
        else:
            add_memory("local", curr_tipo, dimension.get_size())

def p_lista_id_obj(p): 
    '''lista_id_obj : ID f_vars_obj
                    | lista_id_obj ',' ID f_vars_obj'''

def p_f_vars_obj(p):
    "f_vars_obj :"
    global found_error
    obj_size = curr_dir[0].get_resources(curr_tipo) # obtiene los recursos del objeto

    if not mem_available("global", 0) or not mem_available("global", 1):
        print("ERROR: Stack overflow")
        found_error = True

    curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, None, [dirGlobalNum, dirGlobalStr])

    # toma todas los registros que ocupa segun los recursos
    add_memory("global", 0, obj_size[0])
    add_memory("global", 1, obj_size[1])

# Dimensiones al momento de declarar un arreglo o matriz
def p_dimension(p): 
    '''dimension : '[' NUM f_dim1 ']' f_enddim
                 | '[' NUM f_dim1 ']' '[' NUM f_dim2 ']' f_enddim
                 | empty'''

def p_f_dim1(p):
    "f_dim1 :"
    global dim1, dimension
    dim1 = p[-1]

    dimension = DimStructure()
    dimension.add_upper_lim(dim1)

def p_f_dim2(p):
    "f_dim2 :"
    global dim2, dimension
    dim2 = p[-1]

    dimension.add_upper_lim(dim2)

def p_f_enddim(p):
    "f_enddim :"
    global dimension, dim1, dim2
    dim1 = None
    dim2 = None
    dimension.solve()

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
    if not mem_available("local", curr_tipo):
        print("ERROR: Stack overflow")
        found_error = True
    
    # agrega los parámetros como variables locales
    if curr_tipo == 0:
        curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirLocalNum)
    elif curr_tipo == 1:
        curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirLocalStr)
    
    add_memory("local", curr_tipo, 1)
    # registra el tipo para poder validar los parametros después
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
    '''call_func : func f_gosub f_end_call f_end_check
                 | input 
                 | write
                 | return '''

def p_f_end_call(p):
    "f_end_call :"
    function_call.pop()

def p_f_gosub(p):
    "f_gosub :"
    if check_obj[-1] is None:
        f_type, f_start = curr_dir[-1].get_func(function_call[-1])

        if len(curr_func) > 2: # se está llamando a un metodo desde otro método de un objeto
            cuadruplos.add("GOSUB", function_call[-1], curr_func[-2], f_start)
        else:
            cuadruplos.add("GOSUB", function_call[-1], -1, f_start)

    else: # se llama a una función miembro de un objeto
        obj_type, obj_mem = curr_dir[0].get_var(curr_func[0], check_obj[-1]) # busca de qué tipo de objeto es la variable (busca en las variables globales)
        obj_funcs = curr_dir[0].get_dir_from_obj(obj_type) # trae el directorio de funciones de ese objeto
        f_type, f_start = obj_funcs.get_func(function_call[-1])
        cuadruplos.add("GOSUB", function_call[-1], obj_type, f_start)

def p_func(p):
    '''func : ID  f_verify_func '(' args ')'
            | ID  f_varobj ':' ID f_verify_func_composite '(' args ')' '''

def p_f_verify_func(p):
    "f_verify_func :"
    global found_error
    f_type, f_start = curr_dir[-1].get_func(p[-1]) # verifica que exista la funcion
    if f_type == -1:
        print("ERROR: Undeclared function", p[-1], ", line:", lexer.lineno)
        found_error = True
    else:
        function_call.append(p[-1])
        check_obj.append(None)
        param_list.append(curr_dir[-1].get_params(p[-1]))
        param_count.append(0)

        if len(curr_func) > 2: # está llamando a un método desde otro método de un objeto
            cuadruplos.add("MEMBER", -1, -1, -1)
            cuadruplos.add("ERA", p[-1], curr_func[-2], -1)
        else:
            cuadruplos.add("ERA", p[-1], -1, -1)

def p_f_varobj(p):
    "f_varobj :"
    check_obj.append(p[-1]) # lleva registro de a qué objeto se está accediendo

def p_f_verify_func_composite(p):
    "f_verify_func_composite :"
    global found_error
    
    obj_type, obj_mem = curr_dir[0].get_var(curr_func[0], check_obj[-1]) # busca de qué tipo de objeto es la variable (busca en las variables globales)

    if obj_type == -1: # no está declarado ese objeto
        print("ERROR: Undeclared object,", check_obj[-1], ", line:", lexer.lineno)
        found_error = True
    else:
        obj_funcs = curr_dir[0].get_dir_from_obj(obj_type) # trae el directorio de funciones de ese objeto

        f_type, f_start = obj_funcs.get_func(p[-1])
        function_call.append(p[-1])

        if f_type == -1:
            print("ERROR: Undefined function, line:", lexer.lineno)
            found_error = True
        else:
            param_list.append(obj_funcs.get_params(p[-1]))
            cuadruplos.add("OBJREF", obj_mem[0], obj_mem[1], -1) # manda una referencia de la dirección del objeto por si se modifica
            cuadruplos.add("ERA", p[-1], obj_type, -1)
            param_count.append(0)

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

    param_count[-1] += 1

    if param_count[-1] > len(param_list[-1]):
        print("ERROR: Too many arguments, line:", lexer.lineno)
        found_error = True
    else:
        if arg_type == param_list[-1][param_count[-1] - 1]: # checa que sean del mismo tipo
            cuadruplos.add("PARAMETER", arg, param_count[-1], -1)
        else:
            print("ERROR: Wrong argument type, line:", lexer.lineno, ". Argument number", param_count[-1])
            found_error = True

def p_f_end_args(p):
    "f_end_args :"
    global found_error
    if param_count[-1] < len(param_list[-1]):
        print("ERROR: Missing arguments, line:", lexer.lineno)
        found_error = True
    else:
        param_list.pop()
        param_count.pop()

def p_asignacion(p):
    '''asignacion : var '=' f_oper expresion ';' '''
    if cubo.check("=", pilaTipos.pop(), pilaTipos.pop()) != -1:
        cuadruplos.add(pilaOperadores.pop(), pilaOperandos.pop(), -1, pilaOperandos.pop())
    else:
        print("ERROR: Type mismatch, line:", lexer.lineno)

def p_var(p):
    '''var : ID f_varobj ':' ID f_verify_type_composite f_index_obj indexacion f_end_check
           | ID f_verify_type indexacion f_end_check'''

def p_f_verify_type(p):
    "f_verify_type :"
    global found_error, has_dim, base_dir, curr_tipo

    check_obj.append(None)

    var_type, var_mem = curr_dir[-1].get_var(curr_func[-1], p[-1])
    has_dim = curr_dir[-1].get_dim(curr_func[-1], p[-1]) # revisa si es un arreglo
    base_dir = var_mem
    
    if var_type == -1:
        if len(curr_func) > 1: # la estaba buscando localmente en una función, ahora buscar en otro scope (global o en el objeto)
            var_type, var_mem = curr_dir[0].get_var(curr_func[-2], p[-1])
            base_dir = var_mem
            obj_vars = curr_dir[0].get_vars_from_obj(curr_func[-2])
            has_dim = obj_vars.get_dim(p[-1]) # revisa si es un arreglo

        if var_type == -1:
            print("ERROR: Undeclared variable", p[-1], ", line:", lexer.lineno) # local
            found_error = True
        else:
            pilaOperandos.append(var_mem)
            pilaTipos.append(var_type)
            curr_tipo = var_type
    else:
        pilaOperandos.append(var_mem)
        pilaTipos.append(var_type)
        curr_tipo = var_type

def p_f_verify_type_composite(p):
    "f_verify_type_composite :"
    global found_error, curr_tipo, has_dim, base_dir
    
    obj_type, obj_mem = curr_dir[0].get_var(curr_func[0], check_obj[-1]) # busca de qué tipo de objeto es la variable (busca en las variables globales)

    obj_vars = curr_dir[0].get_vars_from_obj(obj_type) # trae la tabla de variables de ese objeto

    var_type, var_mem = obj_vars.get_var(p[-1]) # trae el tipo y la memoria del atributo

    has_dim = obj_vars.get_dim(p[-1]) # revisa si es un arreglo
    base_dir = var_mem

    # la direccion real del atributo depende de la memoria base del objeto
    # en el objeto se guarda una especie de offset para cada atributo
    if var_type == 0:
        real_mem = obj_mem[0] + (var_mem)
    elif var_type == 1:
        real_mem = obj_mem[1] + (var_mem - 3000)

    if var_type == -1:
        print("ERROR: Undeclared variable", p[-1], ", line:", lexer.lineno)
        found_error = True
    else:
        pilaOperandos.append(real_mem)
        pilaTipos.append(var_type)
        curr_tipo = var_type

def p_f_end_check(p):
    "f_end_check :"
    check_obj.pop() # Termina de usar un método o variable que es miembro de un objeto

def p_f_index_obj(p):
    "f_index_obj :"
    obj_type, obj_mem = curr_dir[0].get_var(curr_func[0], check_obj[-1])
    cuadruplos.add("OBJIND", obj_mem[0], obj_mem[1], -1)

# Dimensiones al indexar un arreglo o matriz
def p_indexacion(p):
    '''indexacion : '[' f_start_array expresion f_index ']' f_end_array
                 | '[' f_start_array expresion f_index ']' '[' f_next_index expresion f_index ']' f_end_array
                 | f_no_index empty'''

def p_f_no_index(p):
    "f_no_index :"
    global found_error
    if has_dim: # habia dimensiones pero no se indexó nada
        print("ERROR: Indexable variable, line:", lexer.lineno)
        found_error = True

def p_f_start_array(p):
    "f_start_array :"
    global dim, found_error
    if not has_dim: # se intentó indexar
        print("ERROR: Variable not indexable, line:", lexer.lineno)
        found_error = True
    else:
        arr = pilaOperandos.pop()
        arr_type = pilaTipos.pop()
        dim = 1
        pilaOperadores.append('(') # fake bottom
        pilaDim.append((has_dim, dim, base_dir, curr_tipo))

    cuadruplos.add("STARR", -1, -1,- 1)

def p_f_index(p):
    "f_index :"
    lim_sup, m = pilaDim[-1][0].get_node(dim)

    const_mem = get_constante(0, 0)
    lim_mem = get_constante(lim_sup, 0)

    cuadruplos.add("VERIFY", pilaOperandos[-1], const_mem, lim_mem)

    if not pilaDim[-1][0].is_last_node(pilaDim[-1][1]):
        aux = pilaOperandos.pop()
        pilaTipos.pop()

        m_mem = get_constante(m, 0)

        cuadruplos.add("*", aux, m_mem, dirTempNum)
        pilaOperandos.append(dirTempNum)
        pilaTipos.append(0)
        add_memory("temp", 0, 1)

    if pilaDim[-1][1] > 1:
        aux2 = pilaOperandos.pop()
        pilaTipos.pop()
        aux1 = pilaOperandos.pop()
        pilaTipos.pop()
        cuadruplos.add("+", aux1, aux2, dirTempNum)
        pilaOperandos.append(dirTempNum)
        pilaTipos.append(0)
        add_memory("temp", 0, 1)

def p_f_next_index(p):
    "f_next_index :"
    global dim
    dim += 1
    top_arr, top_dim, base, tipo = pilaDim.pop()
    pilaDim.append((top_arr, top_dim + 1, base, tipo))

def p_f_end_array(p):
    "f_end_array :"
    global found_error
    num_dims = pilaDim[-1][0].get_num_dims()

    if pilaDim[-1][1] < num_dims:
        print("ERROR: Missing indexes, line:", lexer.lineno)
        found_error = True

    aux1 = pilaOperandos.pop()
    pilaTipos.pop()
    const_mem = get_constante(0, 0)
    cuadruplos.add("+", aux1, const_mem, dirTempNum) # + K

    base_mem = get_constante(pilaDim[-1][2], 0)

    cuadruplos.add("+", dirTempNum, base_mem, dirTempNum+1) # + base

    if pilaDim[-1][3] == 0:
        cuadruplos.add("=>", dirTempNum + 1, -1, dirTempPointNum) # asigna la direccion al apuntador
        pilaOperandos.append(dirTempPointNum)
        pilaTipos.append(3)
        add_memory("temp", 0, 2)
        add_memory("temp", 3, 1)

    elif pilaDim[-1][3] == 1:
        cuadruplos.add("=>", dirTempNum + 1, -1, dirTempPointStr) # asigna la direccion al apuntador
        pilaOperandos.append(dirTempPointStr)
        pilaTipos.append(4)
        add_memory("temp", 0, 2)
        add_memory("temp", 4, 1)

    pilaOperadores.pop() # quitar fake bottom
    pilaDim.pop()

def p_expresion(p):
    '''expresion : exp
                 | expresion COMP f_oper exp f_expres '''

def p_f_expres(p):
    "f_expres :"
    global found_error
    if len(pilaOperadores) > 0 and pilaOperadores[-1] in ['<>', '<', '>', '==']:
        oper = pilaOperadores.pop()
        ro = pilaOperandos.pop()
        lo = pilaOperandos.pop()
        rt = pilaTipos.pop()
        lt = pilaTipos.pop()
        tres = cubo.check(oper, lt, rt)

    if tres == -1:
        print("ERROR: Type mismatch, line:", lexer.lineno)
        found_error = True
    else:
        if not mem_available("temp", tres):
            print("ERROR: Stack overflow")
        res = dirTempBool
        add_memory("temp", tres, 1)
        cuadruplos.add(oper, lo, ro, res)

        pilaOperandos.append(res)
        pilaTipos.append(tres)  

def p_exp(p):
    '''exp : term
           | exp OPTERM f_oper term f_exp'''

# Funcion semantica - resolver operaciones + -
def p_f_exp(p):
    "f_exp :"
    global found_error
    if len(pilaOperadores) > 0 and len(pilaOperandos) > 1 and pilaOperadores[-1] in '-+':
        ro = pilaOperandos.pop()
        rt = pilaTipos.pop()
        lo = pilaOperandos.pop()
        lt = pilaTipos.pop()
        oper = pilaOperadores.pop()
        tres = cubo.check(oper, rt, lt)

        if tres == -1:
            print("ERROR: Type mismatch, line:", lexer.lineno)
            found_error = True
        else:
            if not mem_available("temp", tres):
                print("ERROR: Stack overflow")
            res = dirTempNum
            add_memory("temp", tres, 1)
            cuadruplos.add(oper, lo, ro, res)

            pilaOperandos.append(res)
            pilaTipos.append(tres)  

def p_term(p):
    '''term : fact
            | term OPFACT f_oper fact f_term'''

# Funcion semantica - resolver operaciones + /
def p_f_term(p):
    "f_term :"
    global found_error
    if len(pilaOperadores) > 0 and len(pilaOperandos) > 1 and pilaOperadores[-1] in '*/':
        ro = pilaOperandos.pop()
        rt = pilaTipos.pop()
        lo = pilaOperandos.pop()
        lt = pilaTipos.pop()
        oper = pilaOperadores.pop()
        tres = cubo.check(oper, rt, lt)

        if tres == -1:
            print("ERROR: Type mismatch, line:", lexer.lineno)
            found_error = True
        else:
            if not mem_available("temp", tres):
                print("ERROR: Stack overflow")
            res = dirTempNum
            add_memory("temp", 0, 1)
            cuadruplos.add(oper, lo, ro, res)

            pilaOperandos.append(res)
            pilaTipos.append(tres)      

# Funcion semantica para meter operador a la pilaOperadores
def p_f_oper(p):
    "f_oper :"
    pilaOperadores.append(p[-1])

def p_fact(p):
    '''fact : '(' f_lparen expresion ')' f_rparen
            | var
            | NUM f_fact
            | OPTERM NUM
            | CALL func f_gosub f_return_val f_end_call f_end_check
            | CALL to_num
            | CALL to_str
            | STR f_string 
            | fact '&' f_oper var f_concat
            | fact '&' f_oper STR f_string f_concat '''

    if p[1] == '-':
        pilaTipos.append(0)
        var_mem = get_constante(-1 * p[2], 0)
        pilaOperandos.append(var_mem)

    elif p[1] == '+':
        pilaTipos.append(0)
        var_mem = get_constante(p[2], 0)
        pilaOperandos.append(var_mem)

def p_f_concat(p):
    "f_concat :"
    global found_error
    if len(pilaOperadores) > 0 and len(pilaOperandos) > 1 and pilaOperadores[-1] == '&':
        ro = pilaOperandos.pop()
        rt = pilaTipos.pop()
        lo = pilaOperandos.pop()
        lt = pilaTipos.pop()
        oper = pilaOperadores.pop()
        tres = cubo.check(oper, rt, lt)

        if tres == -1:
            print("ERROR: Type mismatch, line:", lexer.lineno)
            found_error = True
        else:
            if not mem_available("temp", tres):
                print("ERROR: Stack overflow")
            res = dirTempStr
            add_memory("temp", 1, 1)
            cuadruplos.add(oper, lo, ro, res)

            pilaOperandos.append(res)
            pilaTipos.append(tres) 

def p_f_lparen(p):
    "f_lparen :"
    pilaOperadores.append(p[-1])

def p_f_rparen(p):
    "f_rparen :"
    pilaOperadores.pop()

def p_f_fact(p):
    "f_fact :"
    pilaTipos.append(0)
    var_mem = get_constante(p[-1], 0)
    pilaOperandos.append(var_mem)

def p_f_return_val(p):
    "f_return_val :"
    
    func_name = function_call[-1]
    
    if check_obj[-1] is not None: # metodo de un objeto
        obj_name = check_obj[-1]
        obj_type, obj_mem = curr_dir[0].get_var(curr_func[0], obj_name) # busca de qué tipo de objeto es la variable (busca en las variables globales)
        ret_type, ret_mem = curr_dir[0].get_return_value(obj_type, func_name)

        if ret_type == 0 or ret_type == 3: # regresa un apuntador cuando el metodo regresa un atributo de si mismo
            ret_mem = obj_mem[0] + (ret_mem)
        elif ret_type == 1 or ret_type == 4:
            ret_mem = obj_mem[1] + (ret_mem - 3000)
    else: # funcion global
        if len(curr_func) > 2: # accesando metodo dentro de otro metodo
            ret_type, ret_mem = curr_dir[0].get_return_value(curr_func[-2], func_name)
        else: # funcion global
            ret_type, ret_mem = curr_dir[-1].get_return_value(curr_func[0], func_name)

    if ret_type == -1:
        print("ERROR: No return value, line", lexer.lineno)
    else:
        if ret_type == 0:
            cuadruplos.add("=", ret_mem, -1, dirTempNum)
            pilaOperandos.append(dirTempNum)
        elif ret_type == 1:
            cuadruplos.add("=", ret_mem, -1, dirTempStr)
            pilaOperandos.append(dirTempStr)

        pilaTipos.append(ret_type)
        add_memory("temp", ret_type, 1)

def p_condicion(p):
    '''condicion : IF '(' expresion ')' f_if THEN '{' estatutos '}' condicionp f_endif'''

def p_condicionp(p):
    '''condicionp : ELSE f_else '{' estatutos '}'
                  | empty '''

def p_f_if(p):
    "f_if :"
    exp_type = pilaTipos.pop()
    if exp_type == 2: # debe ser booleana
        res = pilaOperandos.pop()
        cuadruplos.add("GOTOF", res, -1, -1)
        pilaSaltos.append(cuadruplos.get_cont() - 1)
    else:
        print("ERROR: Type mismatch, line:", lexer.lineno)

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
    if exp_type == 2:
        res = pilaOperandos.pop()
        cuadruplos.add("GOTOF", res, -1, -1)
        pilaSaltos.append(cuadruplos.get_cont() - 1)
    else:
        print("ERROR: Type mismatch, line:", lexer.lineno)

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
    global found_error

    if pilaTipos.pop() == 0: # la expresion resulta en numerico
        cuadruplos.add("=", pilaOperandos.pop(), -1, dirTempNum)
        var_ctrl.append(dirTempNum)
        add_memory("temp", 0, 1)
    else:
        found_error = True
        print("ERROR: Type mismatch, line:", lexer.lineno)

def p_f_for_to(p):
    "f_for_to :"
    global found_error

    exp_type = pilaTipos.pop()
    exp = pilaOperandos.pop()
    if exp_type == 0:
        pilaSaltos.append(cuadruplos.get_cont()) # para el retorno
        cuadruplos.add(">", var_ctrl[-1], exp, dirTempBool) # el for será inclusive
        cuadruplos.add("GOTOV", dirTempBool, -1, -1)
        pilaSaltos.append(cuadruplos.get_cont() - 1) # GotoV
        add_memory("temp", 2, 1)
    else:
        found_error = True
        print("ERROR: Type mismatch, line:", lexer.lineno)

def p_f_for_end(p):
    "f_for_end :" 
    const_mem = get_constante(1, 0)
    cuadruplos.add("+", var_ctrl[-1], const_mem, dirTempNum) # sumar 1 a la var de control
    cuadruplos.add("=", dirTempNum, -1, var_ctrl[-1]) # asignar el resultado a la var de control
    add_memory("temp", 0, 1)

    var_ctrl.pop()
    fin = pilaSaltos.pop()
    retorno = pilaSaltos.pop()
    cuadruplos.add("GOTO", -1, -1, retorno)
    cuadruplos.fill(fin, cuadruplos.get_cont())

def p_to_num(p):
    '''to_num : TO_NUMBER '(' STR f_string ')' 
              | TO_NUMBER '(' var ')' '''
    global found_error
    if pilaTipos.pop() == 1:
        cuadruplos.add("CNUM", pilaOperandos.pop(), -1, dirTempNum)
        pilaOperandos.append(dirTempNum)
        pilaTipos.append(0)
        add_memory("temp", 0, 1)
    else:
        print("ERROR: Type mismatch, line:", lexer.lineno)
        found_error = True

def p_to_str(p):
    '''to_str : TO_STRING '(' expresion ')' '''
    global found_error
    tipo = pilaTipos.pop()
    if tipo == 0 or tipo == 3:
        cuadruplos.add("CSTR", pilaOperandos.pop(), -1, dirTempStr)
        pilaOperandos.append(dirTempStr)
        pilaTipos.append(1)
        add_memory("temp", 1, 1)
    else:
        print("ERROR: Type mismatch, line:", lexer.lineno)
        found_error = True

def p_input(p):
    '''input : INPUT '(' var ')' '''
    tipo = pilaTipos.pop()
    if tipo == 1 or tipo == 4:
        cuadruplos.add("READ", -1, -1, pilaOperandos.pop())
    else:
        print("ERROR: Type mismatch, line:", lexer.lineno)

def p_write(p):
    '''write : PRINT '(' write_list ')' f_call_empty_print
             | PRINT '(' ')' f_call_empty_print '''

def p_f_call_empty_print(p):
    '''f_call_empty_print :'''
    cuadruplos.add("PRINT", -1, -1, -1)

def p_write_list(p):
    '''write_list : write_list '&' write_listp
                  | write_listp'''

def p_write_listp(p):
    '''write_listp : STR f_string
                   | var 
                   | CALL to_str'''    
    if pilaTipos.pop() == 1:
        cuadruplos.add("PRINT", -1, -1, pilaOperandos.pop())
    else:
        print("ERROR: Type mismatch, line:", lexer.lineno)

def p_f_string(p):
    "f_string :"
    clean = p[-1][1:-1] # quitar comillas
    const_mem = get_constante(clean, 1)
    pilaOperandos.append(const_mem)
    pilaTipos.append(1)

def p_return(p):
    '''return : RET '(' expresion ')' '''
    global found_error
    res = pilaOperandos.pop()
    res_type = pilaTipos.pop()

    f_type, f_start = curr_dir[-1].get_func(curr_func[-1])

    if res_type == f_type or cubo.check('=', res_type, f_type) != -1:
        if len(curr_func) > 2: # es una funcion en un objeto
            # Obtener la direccion de la variable de retorno
            ret_type, ret_mem = curr_dir[0].get_return_value(curr_func[-2], curr_func[-1])

            if ( res_type == 0 or res_type == 3 ) and mem_available("objeto", 0):
                cuadruplos.add("RET", res, -1, ret_mem)

            elif ( res_type == 1 or res_type == 3 ) and mem_available("objeto", 1):
                cuadruplos.add("RET", res, -1, ret_mem)
                
            else:
                print("ERROR: Stack overflow")
                found_error = True
        else:
            # Obtener la direccion de la variable de retorno
            ret_type, ret_mem = curr_dir[0].get_return_value(curr_func[-2], curr_func[-1])

            if res_type == 0 and mem_available("global", res_type):
                cuadruplos.add("RET", res, -1, ret_mem) # valor local de retorno es res y se le asigna a la variable global dirGlobalNum
            elif res_type == 1 and mem_available("global", res_type):
                cuadruplos.add("RET", res, -1, ret_mem) # valor local de retorno es res y se le asigna a la variable global dirGlobalNum
            else:
                print("ERROR: Stack overflow")
                found_error = True
                
    else:
        print("ERROR: Type mismatch, line:", lexer.lineno)
        print("Check the type of the function and return value")
        found_error = True

def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    global found_error
    found_error = True
    if p:
         print("Syntax error at token", p.type, ", line:", p.lineno)
         parser.errok()
    else:
         print("Syntax error at EOF")


###########################################
# MAIN

lexer = lex.lex()
parser = yacc.yacc(start='start')

nombre = input('Nombre del archivo: ')
print("")
f = open("./test/revision/" + nombre, "r")
# f = open(nombre, "r")

s = f.read()

if (len(s) > 0):
    empty_file = False

parser.parse(s)

# print("\nCuadruplos:")
# print(cuadruplos)
cuadruplos.generate_file()