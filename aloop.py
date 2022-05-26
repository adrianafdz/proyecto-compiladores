from dimStructure import DimStructure
import ply.lex as lex
import ply.yacc as yacc
from collections import deque
from dirFunc import dirFunc
from cuadruplos import Cuadruplos
from cuboSemantico import cuboSemantico
from tablaVars import tablaVars

found_error = False
empty_file = True

dirGlobalNum = 0 # 0 - 2999
dirGlobalStr = 3000 # 3000 - 3999
# dirGlobalBool = 4000 # 4000 - 4999

dirLocalNum = 5000 # 5000 - 7999
dirLocalStr = 8000 # 8000 - 8999
dirLocalBool = 9000 # 9000 - 9999

dirTempNum = 10000 # 10000 - 12999
dirTempStr = 13000 # 13000 - 13999
dirTempBool = 14000 # 14000 - 14999
dirTempPoint = 15000 # 15000 - 15999

dirConstNum = 16000 # 16000 - 20999
dirConstStr = 21000 # 21000 - 25999

dirObjNum = 0 # 0 - 2999
dirObjStr = 3000 # 3000 - 4999

cuadruplos = Cuadruplos()
cubo = cuboSemantico()
pilaOperandos = deque()
pilaOperadores = deque()
pilaTipos = deque()
pilaSaltos = deque()
pilaDim = deque()

tipos = [0, 1, 2, 3, 4, 5, 6] # number, string, bool, pointer, objeto, nothing
curr_tipo = 6
dimension = None
dim1 = None
dim2 = None
var_ctrl = None # para el for loop
var_ctrl_type = None
has_dim = False
dim = 1
base_dir = 0
is_class = False

curr_dir = deque()
curr_func = deque()
constantes = tablaVars()

dirFuncG = None # directorio de funciones global
dirFuncObj = None # directorio de funciones de un objeto
check_obj = None
param_list = []
param_count = 0

def mem_available(scope, tipo):
    if scope == 'global':
        if tipo == 0: # number
            return dirGlobalNum <= 2999
        elif tipo == 1: # string
            return dirGlobalStr <= 3999
    elif scope == 'local':
        if tipo == 0: # number
            return dirLocalNum <= 7999
        elif tipo == 1: # string
            return dirLocalStr <= 8999
        elif tipo == 3: # bool
            return dirLocalBool <= 9999
    elif scope == 'temp':
        if tipo == 0: # number
            return dirTempNum <= 12999
        elif tipo == 1: # string
            return dirTempStr <= 13999
        elif tipo == 3: # bool
            return dirTempBool <= 14999
        elif tipo == 4: # point
            return dirTempBool <= 15999
    elif scope == 'constantes':
        if tipo == 0:
            return dirConstNum <= 20999
        elif tipo == 1:
            return dirConstStr <= 25999
    elif scope == 'objeto':
        if tipo == 0:
            return dirObjNum <= 2999
        elif tipo == 1:
            return dirObjStr <= 4999
    return False

def add_memory(scope, tipo, cant):
    global dirGlobalNum, dirGlobalStr, dirLocalNum, dirLocalStr, dirLocalBool, dirTempNum, dirTempStr, dirTempBool, dirTempPoint, dirConstNum, dirConstStr, dirObjNum, dirObjStr
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
        elif tipo == 2: # bool
            dirLocalBool += cant
    elif scope == 'temp':
        if tipo == 0: # number
            dirTempNum += cant
        elif tipo == 1: # string
            dirTempStr += cant
        elif tipo == 2: # bool
            dirTempBool += cant
        elif tipo == 3: # point
            dirTempPoint += cant
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
    # CALCULAR RECURSOS
    recNum = dirGlobalNum + (dirTempNum - 10000)
    recStr = dirGlobalStr - 3000 + (dirTempStr - 13000)
    recBool = dirTempBool - 14000
    recPoint = dirTempPoint - 15000

    curr_dir[-1].add_resources(curr_func[-1], [recNum, recStr, recBool, recPoint])
    print(curr_dir[-1])
    # print(constantes)
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
    global dirFuncObj, is_class
    curr_dir[-1].add_func(p[-1], cuadruplos.get_cont(), 5)
    curr_func.append(p[-1])
    dirFuncObj = curr_dir[-1].create_dir_for_obj(curr_func[-1])
    is_class = True

def p_f_clasepadre(p):
    "f_clasepadre :"
    global dirFuncObj
    curr_dir[-1].copy_class_to(p[-1], curr_func[-1])
    rec = curr_dir[-1].get_resources(curr_func[-1])
    dirFuncObj = curr_dir[-1].get_dir_from_obj(curr_func[-1])
    add_memory("objeto", 0, rec[0])
    add_memory("objeto", 1, rec[1])

def p_f_cvars(p):
    "f_cvars :"
    global is_class
    curr_dir.append(dirFuncObj)
    is_class = False

def p_f_endclass(p):
    "f_endclass :"
    global dirObjNum, dirObjStr
    recNum = dirObjNum
    recStr = dirObjStr - 3000

    curr_dir.pop()
    curr_dir[-1].add_resources(curr_func[-1], [recNum, recStr, 0, 0])
    curr_func.pop()

    dirObjNum = 0
    dirObjStr = 3000

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
    curr_tipo = 6

def p_f_tipofunc(p):
    "f_tipofunc :"
    curr_dir[-1].update_func_type(curr_func[-1], curr_tipo)

def p_f_endfunc(p):
    "f_endfunc :"
    global dirLocalNum, dirLocalStr, dirLocalBool, dirTempNum, dirTempStr, dirTempBool, dirTempPoint
    curr_dir[-1].delete_var_table(curr_func[-1])
    # CALCULAR RECURSOS
    recNum = dirLocalNum - 5000 + (dirTempNum - 10000)
    recStr = dirLocalStr - 8000 + (dirTempStr - 13000)
    recBool = dirLocalBool - 9000 + (dirTempBool - 14000)
    recPoint = dirTempPoint - 15000

    curr_dir[-1].add_resources(curr_func[-1], [recNum, recStr, recBool, recPoint])
    curr_func.pop()

    cuadruplos.add("ENDFUNC", -1, -1, -1) # cuadruplo para regresar al programa principal

    dirLocalNum = 5000
    dirLocalStr = 8000
    dirLocalBool = 9000

    dirTempNum = 10000
    dirTempStr = 13000
    dirTempBool = 14000
    dirTempPoint = 15000

def p_vars(p):
    '''vars : vars DEF tipo dimension ':' lista_id ';'
            | vars DEF ID f_varsobj ':' lista_id_obj ';'
            | empty'''

def p_f_varsobj(p):
    "f_varsobj :"
    global curr_tipo, dimension, found_error
    tipo, mem = curr_dir[0].get_func(p[-1])
    
    if tipo == 5: # objeto
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
    global dimension, found_error
    if is_class:
        if not mem_available("objeto", curr_tipo):
            print("MEMORIA GLOBAL LLENA")
            found_error = True

        if curr_tipo == 0:
            curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirObjNum)
        elif curr_tipo == 1:
            curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirObjStr)

        if dimension is None:
            add_memory("objeto", curr_tipo, 1)
        else:
            add_memory("objeto", curr_tipo, dimension.get_size())

    elif len(curr_func) == 1: # esta en variables globales
        if not mem_available("global", curr_tipo):
            print("MEMORIA GLOBAL LLENA")
            found_error = True

        if curr_tipo == 0:
            curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirGlobalNum)
        elif curr_tipo == 1:
            curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirGlobalStr)
        
        if dimension is None:
            add_memory("global", curr_tipo, 1)
        else:
            add_memory("global", curr_tipo, dimension.get_size())
    else:
        if not mem_available("local", curr_tipo):
            print("MEMORIA LOCAL LLENA")
            found_error = True

        if curr_tipo == 0:
            curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirLocalNum)
        elif curr_tipo == 1:
            curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirLocalStr)

        if dimension is None:
            add_memory("local", curr_tipo, 1)
        else:
            add_memory("local", curr_tipo, dimension.get_size())

    dimension = None

def p_lista_id_obj(p): 
    '''lista_id_obj : ID f_vars_obj
                    | lista_id_obj ',' ID f_vars_obj'''

def p_f_vars_obj(p):
    "f_vars_obj :"
    global found_error, dimension
    obj_size = curr_dir[0].get_resources(curr_tipo)

    if len(curr_func) == 1: # esta en variables globales
        if not mem_available("global", 0) or not mem_available("global", 1):
            print("MEMORIA GLOBAL LLENA")
            found_error = True

        curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, [dirGlobalNum, dirGlobalStr])

        add_memory("global", 0, obj_size[0])
        add_memory("global", 1, obj_size[1])
    else:
        if not mem_available("local", 0) or not mem_available("local", 1):
            print("MEMORIA LOCAL LLENA")
            found_error = True

        curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, [dirLocalNum, dirLocalStr])
        
        add_memory("local", 0, obj_size[0])
        add_memory("local", 1, obj_size[1])

    dimension = None

def p_dimension(p): 
    '''dimension : '[' NUM f_dim1 ']' f_onedim
                 | '[' NUM f_dim1 ']' '[' NUM f_dim2 ']' f_twodim
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

def p_f_onedim(p):
    "f_onedim :"
    global dimension, dim1, dim2
    dim1 = None
    dim2 = None
    dimension.solve()

def p_f_twodim(p):
    "f_twodim :"
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
        print("MEMORIA LOCAL LLENA")
        found_error = True
    
    if curr_tipo == 0:
        curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirLocalNum)
    elif curr_tipo == 1:
        curr_dir[-1].add_var(curr_func[-1], p[-1], curr_tipo, dimension, dirLocalStr)
    
    add_memory("local", curr_tipo, 1)
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
        curr_func.append(p[-1])

def p_f_verify_func_composite(p):
    "f_verify_func_composite :"
    global found_error, param_list, param_count
    
    if len(curr_func) > 1: # esta en una función, busca objeto localmente
        obj_type, obj_mem = curr_dir[0].get_vars_from_obj(curr_func[-1]).get_var(check_obj)
    else:
        obj_type, obj_mem = curr_dir[0].get_var(curr_func[0], check_obj) # busca de qué tipo de objeto es la variable (busca en las variables globales)
    
    curr_func.append(check_obj)
    obj_funcs = curr_dir[0].get_dir_from_obj(obj_type) # trae el directorio de funciones de ese objeto

    f_type, f_start = obj_funcs.get_func(p[-1])
    curr_func.append(p[-1])

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
        found_error = True
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
    if cubo.check("=", pilaTipos.pop(), pilaTipos.pop()) != -1:
        cuadruplos.add(pilaOperadores.pop(), pilaOperandos.pop(), -1, pilaOperandos.pop())
    else:
        print("ERROR: type mismatch, line", lexer.lineno)

def p_var(p):
    '''var : ID f_varobj ':' ID f_verify_type_composite indexacion
           | ID f_verify_type indexacion'''

def p_indexacion(p):
    '''indexacion : f_start_array '[' expresion f_index ']' f_end_array
                 | f_start_array '[' expresion f_index ']' '[' f_next_index expresion f_index ']' f_end_array
                 | f_no_index empty'''

def p_f_varobj(p):
    "f_varobj :"
    global check_obj
    check_obj = p[-1]

def p_f_verify_type(p):
    "f_verify_type :"
    global found_error, has_dim, base_dir
    var_type, var_mem = curr_dir[-1].get_var(curr_func[-1], p[-1])
    has_dim = curr_dir[-1].get_dim(curr_func[-1], p[-1])
    base_dir = var_mem
    
    if var_type == -1:
        if len(curr_func) > 1: # la estaba buscando localmente en una función, ahora buscar en otro scope
            var_type, var_mem = curr_dir[0].get_var(curr_func[-2], p[-1])
             
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
    obj_type, obj_mem = curr_dir[0].get_var(curr_func[0], check_obj) # busca de qué tipo de objeto es la variable (busca en las variables globales)

    obj_vars = curr_dir[0].get_vars_from_obj(obj_type) # trae la tabla de variables de ese objeto

    var_type, var_mem = obj_vars.get_var(p[-1]) # trae el tipo y la memoria del atributo

    # la direccion real del atributo depende de la memoria base del objeto
    # en el objeto se guarda una especia de offset para cada atributo
    if var_type == 0:
        real_mem = obj_mem[0] + (var_mem)
    elif var_type == 1:
        real_mem = obj_mem[1] + (var_mem - 3000)

    if var_type == -1:
        print("UNDECLARED VARIABLE", p[-1], ", line:", lexer.lineno)
        found_error = True
    else:
        pilaOperandos.append(real_mem)
        pilaTipos.append(var_type)

def p_f_no_index(p):
    "f_no_index :"
    global found_error
    if has_dim:
        print("ERROR: indexable variable, line", lexer.lineno)
        found_error = True

def p_f_start_array(p):
    "f_start_array :"
    global dim, found_error
    if not has_dim:
        print("Error: variable not indexable, line", lexer.lineno)
        found_error = True
    else:
        arr = pilaOperandos.pop()
        arr_type = pilaTipos.pop()
        dim = 1
        pilaOperadores.append('(') # fake bottom
        pilaDim.append((has_dim, dim, base_dir))

def p_f_index(p):
    "f_index :"
    lim_sup, m = pilaDim[-1][0].get_node(dim)

    if not constantes.check_var(0):
        constantes.add_var(0, 0, None, dirConstNum)
        const_mem = dirConstNum
        add_memory("constantes", 0, 1)
    else:
        const_tipo, const_mem = constantes.get_var(0)

    if not constantes.check_var(lim_sup):
        constantes.add_var(lim_sup, 0, None, dirConstNum)
        lim_mem = dirConstNum
        add_memory("constantes", 0, 1)
    else:
        const_tipo, lim_mem = constantes.get_var(lim_sup)

    cuadruplos.add("VERIFY", pilaOperandos[-1], const_mem, lim_mem)

    if not pilaDim[-1][0].is_last_node(pilaDim[-1][1]):
        aux = pilaOperandos.pop()
        pilaTipos.pop()

        if not constantes.check_var(m):
            constantes.add_var(m, 0, None, dirConstNum)
            m_mem = dirConstNum
            add_memory("constantes", 0, 1)
        else:
            const_tipo, m_mem = constantes.get_var(m)

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
    top_arr, top_dim, base = pilaDim.pop()
    pilaDim.append((top_arr, top_dim + 1, base))

def p_f_end_array(p):
    "f_end_array :"
    global found_error
    num_dims = pilaDim[-1][0].get_num_dims()

    if pilaDim[-1][1] < num_dims:
        print("ERROR: missing indexes, line", lexer.lineno)
        found_error = True

    aux1 = pilaOperandos.pop()
    pilaTipos.pop()
    const_tipo, const_mem = constantes.get_var(0) # K = 0
    cuadruplos.add("+", aux1, const_mem, dirTempNum)

    if not constantes.check_var(pilaDim[-1][2]):
        constantes.add_var(pilaDim[-1][2], 0, None, dirConstNum) # base
        base_mem = dirConstNum
        add_memory("constantes", 0, 1)
    else:
        const_tipo, base_mem = constantes.get_var(pilaDim[-1][2])

    cuadruplos.add("+", dirTempNum, base_mem, dirTempNum+1)
    add_memory("temp", 0, 2)

    pilaOperandos.append(dirTempNum-1) # APUNTADOR
    pilaTipos.append(3)
    pilaOperadores.pop() # quitar fake bottom
    pilaDim.pop()

def p_expresion(p):
    '''expresion : exp
                 | expresion COMP f_oper exp f_expres
                 | STR f_string_expr '''

def p_f_string_expr(p):
    "f_string_expr :"
    pilaOperandos.append(p[-1])
    pilaTipos.append(1)

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
        print("ERROR: Type Mismatch")
        found_error = True
    else:
        if not mem_available("temp", tres):
            print("MEMORIA TEMPORAL LLENA")
        res = dirTempNum
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
            print("ERROR: Type Mismatch")
            found_error = True
        else:
            if not mem_available("temp", tres):
                print("MEMORIA TEMPORAL LLENA")
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
            print("ERROR: Type Mismatch")
            found_error = True
        else:
            if not mem_available("temp", tres):
                print("MEMORIA TEMPORAL LLENA")
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
    '''fact : '(' lparen expresion ')' rparen
            | var
            | NUM f_fact
            | OPTERM NUM
            | CALL call_func f_return_val '''

    if p[1] == '-':
        pilaTipos.append(0)
        if not constantes.check_var(-1 * p[2]):
            constantes.add_var(-1 * p[2], 0, None, dirConstNum)
            pilaOperandos.append(dirConstNum)
            add_memory("constantes", 0, 1)
        else:
            var_tipo, var_mem = constantes.get_var(-1 * p[2])
            pilaOperandos.append(var_mem)
    elif p[1] == '+':
        pilaTipos.append(0)
        if not constantes.check_var(p[2]):
            constantes.add_var(p[2], 0, None, dirConstNum)
            pilaOperandos.append(dirConstNum)
            add_memory("constantes", 0, 1)
        else:
            var_tipo, var_mem = constantes.get_var(p[2])
            pilaOperandos.append(var_mem)

def p_f_return_val(p):
    "f_return_val :"
    func_name = curr_func.pop()

    if len(curr_func) > 1: # funcion de un objeto
        obj_name = curr_func.pop()

        if len(curr_func) > 1: # esta en una función, busca objeto localmente
            obj_type, obj_mem = curr_dir[0].get_vars_from_obj(curr_func[-1]).get_var(obj_name)
        else:
            obj_type, obj_mem = curr_dir[0].get_var(curr_func[0], obj_name) # busca de qué tipo de objeto es la variable (busca en las variables globales)
        
        obj_vars = curr_dir[0].get_vars_from_obj(obj_type) # trae la tabla de variables de ese objeto

        ret_type, ret_mem = obj_vars.get_return_value(func_name)

        if ret_type == 0:
            ret_mem = obj_mem[0] + (ret_mem)
        elif ret_type == 1:
            ret_mem = obj_mem[1] + (ret_mem - 3000)
    else: 
        ret_type, ret_mem = curr_dir[-1].get_return_value(curr_func[-1], func_name)

    if ret_type == -1:
        print("ERROOR, No return value, line", lexer.lineno)
    else:
        pilaOperandos.append(ret_mem)
        pilaTipos.append(ret_type)

def p_lparen(p):
    "lparen :"
    pilaOperadores.append(p[-1])

def p_rparen(p):
    "rparen :"
    pilaOperadores.pop()

def p_f_fact(p):
    "f_fact :"
    pilaTipos.append(0)

    if not constantes.check_var(p[-1]):
        constantes.add_var(p[-1], 0, None, dirConstNum)
        pilaOperandos.append(dirConstNum)
        add_memory("constantes", 0, 1)
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
    global found_error

    exp_type = pilaTipos.pop()
    exp = pilaOperandos.pop()
    if exp_type == 0:
        pilaSaltos.append(cuadruplos.get_cont()) # para el retorno
        cuadruplos.add(">", var_ctrl, exp, dirTempBool) # el for será inclusive
        cuadruplos.add("GOTOV", dirTempBool, -1, -1)
        pilaSaltos.append(cuadruplos.get_cont() - 1) # GotoV
        add_memory("temp", 3, 1)
    else:
        found_error = True
        print("ERROR: Type mismatch, line", lexer.lineno)

def p_f_for_end(p):
    "f_for_end :" 
    cuadruplos.add("+", var_ctrl, "1", dirTempNum) # sumar 1 a la var de control
    cuadruplos.add("=", dirTempNum, -1, var_ctrl) # asignar el resultado a la var de control
    add_memory("temp", 0, 1)

    fin = pilaSaltos.pop()
    retorno = pilaSaltos.pop()
    cuadruplos.add("GOTO", -1, -1, retorno)
    cuadruplos.fill(fin, cuadruplos.get_cont())

def p_to_num(p):
    '''to_num : TO_NUMBER '(' STR ')' 
              | TO_NUMBER '(' var ')' '''
    global found_error
    if pilaTipos[-1] == 1:
        cuadruplos.add("CNUM", pilaOperandos.pop(), -1, dirTempNum)
        pilaTipos.pop()
        pilaOperandos.append(dirTempNum)
        pilaTipos.append(0)
        add_memory("temp", 0, 1)
    else:
        print("ERROR: Type Mismatch")
        found_error = True

def p_to_str(p):
    '''to_str : TO_STRING '(' expresion ')' '''
    global found_error
    if pilaTipos[-1] == 0:
        cuadruplos.add("CSTR", pilaOperandos.pop(), -1, dirTempStr)
        pilaTipos.pop()
        pilaOperandos.append(dirTempStr)
        pilaTipos.append(1)
        add_memory("temp", 1, 1)
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
    '''write_listp : STR f_string
                   | var 
                   | CALL to_str'''    
    if pilaTipos.pop() == 1:
        cuadruplos.add("PRINT", -1, -1, pilaOperandos.pop())
    else:
        print("type mismatch")

def p_f_string(p):
    "f_string :"
    pilaOperandos.append(p[-1])
    pilaTipos.append(1)

def p_return(p):
    '''return : RET '(' expresion ')' '''
    global found_error
    res = pilaOperandos.pop()
    res_type = pilaTipos.pop()

    f_type, f_start = curr_dir[-1].get_func(curr_func[-1])

    if res_type == f_type:
        if len(curr_func) > 2: # es una funcion en un objeto
            if res_type == 0 and mem_available("objeto", res_type):
                curr_dir[0].add_return_value(curr_func[-2], curr_func[-1], res_type, dirObjNum)
                cuadruplos.add("RET", res, -1, dirObjNum) # asigna el valor de retorno a la variable creada
                
                add_memory("objeto", 0, 1)
            elif res_type == 1 and mem_available("objeto", res_type):
                curr_dir[0].add_return_value(curr_func[-2], curr_func[-1], res_type, dirObjStr)
                cuadruplos.add("RET", res, -1, dirObjStr) # asigna el valor de retorno a la variable creada
                
                add_memory("objeto", 1, 1)
            else:
                print("ERROR: memoria llena")
                found_error = True
        else:
            if res_type == 0 and mem_available("global", res_type):
                curr_dir[0].add_return_value(curr_func[-2], curr_func[-1], res_type, dirGlobalNum)
                cuadruplos.add("RET", res, -1, dirGlobalNum)
                
                add_memory("global", 0, 1)
            elif res_type == 1 and mem_available("global", res_type):
                curr_dir[0].add_return_value(curr_func[-2], curr_func[-1], res_type, dirGlobalStr)
                cuadruplos.add("RET", res, -1, dirGlobalStr)
                
                add_memory("global", 1, 1)
            else:
                print("ERROR: memoria global llena")
                found_error = True
                
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