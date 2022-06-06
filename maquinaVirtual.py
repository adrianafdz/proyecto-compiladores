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
object_ref = deque()
cant_funciones = deque()
indref = deque()

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
Función que obtiene los datos sobre los recursos y constantes generados durante la compilación
'''
def get_compilation_info():
    global RESOURCES, CONSTANTS
    try:
        with open("recursos.json", "r") as jsonFile:
            RESOURCES = json.load(jsonFile)
        with open("constantes.json", "r") as jsonFile:
            CONSTANTS = json.load(jsonFile)
    except:
        raise Exception("Error while retrieving data from compilation")

'''
Función que obtiene los recursos de memoria que requiere una función
'''
def get_resources(func_name, obj_name):
    if obj_name == "-1":
        if func_name in RESOURCES.keys():
            return RESOURCES[func_name]
        else:
            raise Exception("Error while retrieving function data")
    else:
        if obj_name in RESOURCES.keys():
            if func_name in RESOURCES[obj_name].keys():
                return RESOURCES[obj_name][func_name]
            else:
                raise Exception("Error while retrieving function data")
        else:
            raise Exception("Error while retrieving object data")

    return None

'''
Función que obtiene el valor y tipo de una constante
'''
def get_constant(const_dir):
    if str(const_dir) in CONSTANTS.keys():
        if CONSTANTS[str(const_dir)]['tipo'] == 0:
            return float(CONSTANTS[str(const_dir)]['nombre']), 0
        else:
            return str(CONSTANTS[str(const_dir)]['nombre']), 1
    else:
        raise Exception("Error while retriving data from constants")

'''
Función que obtiene el valor contenido en una dirección de la memoria
'''
def get_value(address, should_pop = True):
    value = None
    address = int(address)

    if address >= BASE_DIRCONSTNUM_LI and address <= BASE_DIRCONSTSTR_LS: # constante
        value = get_constant(address)

    elif address >= BASE_DIRTEMPPOINTNUM_LI and address <= BASE_DIRTEMPPOINTSTR_LS: # apuntador
        val, tipo = pilaMemoria[-1].get_data(address) # obtiene la direccion a la que apunta

        if indref[-1] is not None:
            if val >= BASE_DIROBJNUM_LI and val <= BASE_DIROBJNUM_LS:
                ref = int(indref[-1][0])
                val = ref + val
            else:
                ref = int(indref[-1][1])
                val = ref + val

        if should_pop:
            indref.pop()

        if object_ref[-1 - cant_funciones[-1]] is not None:
            value = pilaMemoria[0].get_data(val)
        else:
            value = pilaMemoria[-1].get_data(val) # toma el valor a esa direccion

    elif address >= BASE_DIRGLOBALNUM_LI and address <= BASE_DIRGLOBALSTR_LS: # global
        if object_ref[-1 - cant_funciones[-1]] is not None: # como se utilizan los mismos rangos, hay que identificar si es un objeto
            if address >= BASE_DIROBJNUM_LI and address <= BASE_DIROBJNUM_LS:
                ref = int(object_ref[-1 - cant_funciones[-1]][0])
                address = ref + address - BASE_DIROBJNUM_LI # obtiene la dirección real
            else:
                ref = int(object_ref[-1 - cant_funciones[-1]][1])
                address = ref + address - BASE_DIROBJSTR_LI

        value = pilaMemoria[0].get_data(address)

    else: # local
        value = pilaMemoria[-1 - cant_funciones[-1]].get_data(address)

    if value[0] is None:
        raise Exception("ERROR: Uninitialized variable")

    return value

'''
Función que le asigna un valor a una dirección de memoria
'''
def set_value(address, value, set_pointer = False):
    address = int(address)

    if address >= BASE_DIRTEMPPOINTNUM_LI and address <= BASE_DIRTEMPPOINTSTR_LS: # apuntador
        if set_pointer: # asignarle una dirección ( address -> value )
            value = int(value)
            if object_ref[-1] is not None:
                if value >= BASE_DIROBJNUM_LI and value <= BASE_DIROBJNUM_LS:
                    ref = int(object_ref[-1 - cant_funciones[-1]][0])
                    value = ref + value - BASE_DIROBJNUM_LI
                else:
                    ref = int(object_ref[-1 - cant_funciones[-1]][1])
                    value = ref + value - BASE_DIROBJSTR_LI

            return pilaMemoria[-1].set_data(address, value)
        else:
            points_at, tipo = pilaMemoria[-1].get_data(address) # obtiene la dirección a la que apunta
            
            if indref[-1] is not None:
                if points_at >= BASE_DIROBJNUM_LI and points_at <= BASE_DIROBJNUM_LS:
                    ref = int(indref[-1][0])
                    points_at = ref + points_at
                else:
                    ref = int(indref[-1][1])
                    points_at = ref + points_at

            indref.pop()
            if object_ref[-1] is not None:
                return pilaMemoria[0].set_data(points_at, value)
            return pilaMemoria[-1].set_data(points_at, value) # le asigna el valor a esa dirección

    if address >= BASE_DIRGLOBALNUM_LI and address <= BASE_DIRGLOBALSTR_LS: # global
        if object_ref[-1 - cant_funciones[-1]] is not None: # identificar si es un objeto
            if address >= BASE_DIROBJNUM_LI and address <= BASE_DIROBJNUM_LS:
                ref = int(object_ref[-1 - cant_funciones[-1]][0])
                address = ref + address - BASE_DIROBJNUM_LI
            else:
                ref = int(object_ref[-1 - cant_funciones[-1]][1])
                address = ref + address - BASE_DIROBJSTR_LI

        return pilaMemoria[0].set_data(address, value)

    else: # local
        pilaMemoria[-1 - cant_funciones[-1]].set_data(address, value)

'''
Función que convierte un valor booleano a 1 o 0
'''
def resOpeBool(res):
    if res == True:
        return 1
    elif res == False:
        return 0

'''
Función para realizar una operación entre dos valores según el signo
'''
def operadores(signo, val1, val2):
    try:
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
        elif signo == '&':
            res = val1 + val2

        return res
    except:
        raise Exception("ERROR: Invalid operation")

##########################################################
# MAIN
get_cuadruplos()
get_compilation_info()
pilaCurrCuadruplo.append(0)
cant_funciones.append(-1)
set_object_ref = False
add_indrex = False

while True:
    # try:
    #     pilaMemoria[-1].print()
    #     print("---------------")
    # except:
    #     pass
    cuadruplo = CUADRUPLOS[pilaCurrCuadruplo[-1]]

    # print(cuadruplo)

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
        cant_funciones[-1] += 1

        if not set_object_ref:
            object_ref.append(None)

        set_object_ref = False

    elif cuadruplo[0] == "PARAMETER":
        value, tipo = get_value(cuadruplo[1])
        pilaMemoria[-1].set_parameter(value, tipo)

    elif cuadruplo[0] == "GOSUB":
        pilaCurrCuadruplo.append(int(cuadruplo[3]) - 1)
        cant_funciones.append(0)
        continue

    elif cuadruplo[0] == "ENDFUNC":
        pilaMemoria.pop()
        pilaCurrCuadruplo.pop()
        object_ref.pop()
        cant_funciones.pop()
        cant_funciones[-1] -= 1

    elif cuadruplo[0] == "RET":
        return_value, _ = get_value(cuadruplo[1])
        return_address = cuadruplo[3]
        set_value(return_address, return_value)

    elif cuadruplo[0] == "OBJREF":
        object_ref.append((int(cuadruplo[1]), (cuadruplo[2]))) # referencia de las direcciones number y string
        set_object_ref = True

    elif cuadruplo[0] == "MEMBER":
        object_ref.append(object_ref[-1]) # referencia de las direcciones number y string
        set_object_ref = True

    elif cuadruplo[0] == "=>": # asignar una dirección a un apuntador
        value, _ = get_value(cuadruplo[1])
        set_value(cuadruplo[3], value, True)

    elif cuadruplo[0] == '=':
        value, _ = get_value(cuadruplo[1])
        set_value(cuadruplo[3], value)

    elif cuadruplo[0] in ['+', '-', '*', '/', '>', '<', '<>', '==', '&']:
        value1, _ = get_value(cuadruplo[1])
        value2, _ = get_value(cuadruplo[2])
        res_address = cuadruplo[3]
        res_value = operadores(cuadruplo[0], value1, value2)
        set_value(res_address, res_value)

    elif cuadruplo[0] == "OBJIND":
        indref.append((int(cuadruplo[1]), int(cuadruplo[2])))
        add_indrex = True

    elif cuadruplo[0] == "STARR":
        if not add_indrex:
            indref.append(None)
        add_indrex = False

    elif cuadruplo[0] == "VERIFY":
        value, _ = get_value(cuadruplo[1], False)
        lim_inf, _ = get_value(cuadruplo[2])
        lim_sup, _ = get_value(cuadruplo[3])

        if value >= lim_inf and value < lim_sup:
            pass
        else:
            raise Exception("ERROR: Index out of bounds")

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
        if cuadruplo[3] == "-1":
            print("")
        else:
            texto, _ = get_value(cuadruplo[3])
            print(str(texto), end=" ")

    pilaCurrCuadruplo[-1] += 1
