from collections import deque
import json
from aloop import *
from dirVirtuales import *
from memoria import Memoria

CUADRUPLOS = []
RESOURCES = {}
CONSTANTS = {}

pilaMemoria = deque()
pilaCurrCuadruplo = deque()
object_ref = None

'''
Función que obtiene los cuádruplos generados durante la compilación
'''
def get_cuadruplos():
    codObj = open("codint.txt", 'r', encoding='utf-8')
    cuadLista = codObj.readlines()

    for linea in cuadLista:
        linea = linea.replace('\n', '')
        cuadruplo = tuple(linea.split(','))
        cuadruplo = (cuadruplo[0], cuadruplo[1], cuadruplo[2], cuadruplo[3])
        CUADRUPLOS.append(cuadruplo)

'''
Función que obtiene los datos generados durante la compilación
'''
def get_compilation_info():
    global RESOURCES, CONSTANTS
    try:
        with open("recursos.json", "r") as jsonFile:
            RESOURCES = json.load(jsonFile)
        with open("constantes.json", "r") as jsonFile:
            CONSTANTS = json.load(jsonFile)
    except:
        print("Error while retrieving data from compilation")

'''
Función que obtiene los recursos de memoria que requiere una función
'''
def get_resources(func_name, obj_name):
    if obj_name == "-1":
        if func_name in RESOURCES.keys():
            return RESOURCES[func_name]
        else:
            print("Error while retrieving function data")
    else:
        if obj_name in RESOURCES.keys():
            if func_name in RESOURCES[obj_name].keys():
                return RESOURCES[obj_name][func_name]
            else:
                print("Error while retrieving function data")
        else:
            print("Error while retrieving object data")

    return None

'''
Función que obtiene el valor de una constante
'''
def get_constant(const_dir):
    if str(const_dir) in CONSTANTS.keys():
        if CONSTANTS[str(const_dir)]['tipo'] == 0:
            return float(CONSTANTS[str(const_dir)]['nombre']), 0
        else:
            return str(CONSTANTS[str(const_dir)]['nombre']), 1
    else:
        print("Error while retriving data from constants")
        return None

'''
Función que obtiene el valor contenido en una dirección de la memoria
'''
def get_value(address, param_scope = 0):
    address = int(address)

    if address >= BASE_DIRCONSTNUM_LI and address <= BASE_DIRCONSTSTR_LS:
        return get_constant(address)

    if address >= BASE_DIRTEMPPOINTNUM_LI and address <= BASE_DIRTEMPPOINTSTR_LS: # apuntador
        val, tipo = pilaMemoria[-1].get_data(address) # obtiene la direccion a la que apunta
        return pilaMemoria[-1].get_data(val) # le asigna el valor a esa direccion

    if address >= BASE_DIRGLOBALNUM_LI and address <= BASE_DIRGLOBALSTR_LS:
        if object_ref is not None:
            if address >= BASE_DIROBJNUM_LI and address <= BASE_DIROBJNUM_LS:
                address = object_ref[0] + address - BASE_DIROBJNUM_LI
            else:
                address = object_ref[1] + address - BASE_DIROBJSTR_LI

        return pilaMemoria[0].get_data(address)

    else:
        return pilaMemoria[-1 - param_scope].get_data(address)

'''
Función que le asigna un valor a una dirección de memoria
'''
def set_value(address, value):
    address = int(address)

    if address >= BASE_DIRTEMPPOINTNUM_LI and address <= BASE_DIRTEMPPOINTSTR_LS: # apuntador
        points_at, tipo = pilaMemoria[-1].get_data(address) # regresa una direccion

        if points_at is None: 
            # no tiene asignada una dirección aún
            return pilaMemoria[-1].set_data(address, int(value))
        else: 
            # ya tiene algo asignado, así que se le asigna el valor a la direccion a la que apunta
            return pilaMemoria[-1].set_data(points_at, value)

    if address >= BASE_DIRGLOBALNUM_LI and address <= BASE_DIRGLOBALSTR_LS:
        if object_ref is not None:
            if address >= BASE_DIROBJNUM_LI and address <= BASE_DIROBJNUM_LS:
                address = object_ref[0] + address - BASE_DIROBJNUM_LI
            else:
                address = object_ref[1] + address - BASE_DIROBJSTR_LI

        return pilaMemoria[0].set_data(address, value)

    else:
        return pilaMemoria[-1].set_data(address, value)

def resOpeBool(res):
    if res == True:
        return 1
    elif res == False:
        return 0

def operadores(signo, val1, val2):
    if signo == '+':
        res = val1 + val2
    elif signo == '-':
        res = val1 - val2
    elif signo == '*':
        res = val1 * val2
    elif signo == '/':
        res = val1 / val2
    elif signo == '>':
        res = resOpeBool(val1 > val2)
    elif signo == '<':
        res = resOpeBool(val1 < val2)
    elif signo == '<>':
        res = resOpeBool(val1 != val2)
    elif signo == '==':
        res = resOpeBool(val1 == val2)
    elif  signo == '<>':
        res = resOpeBool(val1 != val2)
    elif signo == '==':
        res = resOpeBool(val1 == val2)
    elif signo == '&':
        res = val1 + val2

    return res

##########################################################
# MAIN
get_cuadruplos()
get_compilation_info()
pilaCurrCuadruplo.append(0)
cant_funciones_anidadas = -1

while True:
    cuadruplo = CUADRUPLOS[pilaCurrCuadruplo[-1]]

    if cuadruplo[0] == 'END':
        # print("Termina ejecución")
        # pilaMemoria[0].print()
        break

    elif cuadruplo[0] == 'GOTO':
        pilaCurrCuadruplo[-1] = int(cuadruplo[3]) - 1
        continue

    elif cuadruplo[0] == "GOTOF":
        value, _ = get_value(cuadruplo[1])
        if value == 0:
            pilaCurrCuadruplo[-1] = int(cuadruplo[3]) - 1
            continue

    elif cuadruplo[0] == "GOTOV":
        value, _ = get_value(cuadruplo[1])
        if value == 1:
            pilaCurrCuadruplo[-1] = int(cuadruplo[3]) - 1
            continue

    elif cuadruplo[0] == 'ERA':
        func_name = cuadruplo[1]
        obj_name = cuadruplo[2]
        recursos = get_resources(func_name, obj_name)
        nueva_memoria = Memoria(recursos)
        pilaMemoria.append(nueva_memoria)
        cant_funciones_anidadas += 1

    elif cuadruplo[0] == "PARAMETER":
        value, tipo = get_value(cuadruplo[1], cant_funciones_anidadas)
        pilaMemoria[-1].set_parameter(value, tipo)

    elif cuadruplo[0] == "GOSUB":
        pilaCurrCuadruplo.append(int(cuadruplo[3]) - 1)
        continue

    elif cuadruplo[0] == "ENDFUNC":
        pilaMemoria.pop()
        pilaCurrCuadruplo.pop()
        object_ref = None
        cant_funciones_anidadas -= 1

    elif cuadruplo[0] == "RET":
        return_value, _ = get_value(cuadruplo[1])
        return_address = cuadruplo[3]
        set_value(return_address, return_value)

    elif cuadruplo[0] == "OBJREF":
        object_ref = (int(cuadruplo[1]), (cuadruplo[2])) # referencia de las direcciones number y string

    elif cuadruplo[0] == '=':
        value, _ = get_value(cuadruplo[1])
        set_value(cuadruplo[3], value)

    elif cuadruplo[0] in ['+', '-', '*', '/', '>', '<', '<>', '==', '&']:
        value1, _ = get_value(cuadruplo[1])
        value2, _ = get_value(cuadruplo[2])
        res_address = cuadruplo[3]
        res_value = operadores(cuadruplo[0], value1, value2)
        set_value(res_address, res_value)

    elif cuadruplo[0] == "VERIFY":
        value, _ = get_value(cuadruplo[1])
        lim_inf, _ = get_value(cuadruplo[2])
        lim_sup, _ = get_value(cuadruplo[3])

        if value >= lim_inf and value < lim_sup:
            pass
        else:
            print("ERROR: Index out of bounds")

    elif cuadruplo[0] == "CNUM":
        new_val, _ = get_value(cuadruplo[1])
        set_value(cuadruplo[3], float(new_val))

    elif cuadruplo[0] == "CSTR":
        new_val, _ = get_value(cuadruplo[1])
        set_value(cuadruplo[3], str(new_val))

    elif cuadruplo[0] == "READ":
        new_val = input(">> ")
        set_value(cuadruplo[3], new_val)

    elif cuadruplo[0] == 'PRINT':
        texto, _ = get_value(cuadruplo[3])
        print("<<",str(texto))

    pilaCurrCuadruplo[-1] += 1
