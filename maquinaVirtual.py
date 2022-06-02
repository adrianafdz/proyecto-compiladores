import sys
#from aloop import *
from dirVirtuales import *

# Declaracion de constantes
CONST_TEMPORAL = 'temporal'
CONST_EJECUCION = 'ejecucion'
CONST_RETORNO_VALOR = 'retorno'
CONST_FUNCION_RETORNO = 'funcion'

# Declaracion de pilas
pilaTemporal = []
pilaEjecucion = []
pilaRetorno = []
pilaFuncion = []

pilaCorriendo = ''

cuadLista = []
cuadIndice = 0
cuadruplo = ()

'''
Funciones de control de las pilas
'''
def push(pilaNom, mem):
    if pilaNom == CONST_TEMPORAL:
        global pilaTemporal
        pilaTemporal.append(mem)
    elif pilaNom == CONST_EJECUCION:
        global pilaEjecucion
        pilaEjecucion.append(mem)
    elif pilaNom == CONST_RETORNO_VALOR:
        global pilaRetorno
        pilaRetorno.append(mem)
    elif pilaNom == CONST_FUNCION_RETORNO:
        global pilaFuncion
        pilaFuncion.append(mem)

def pop(pilaNom):
    if pilaNom == CONST_TEMPORAL:
        global pilaTemporal
        return pilaTemporal.pop()
    elif pilaNom == CONST_EJECUCION:
        global pilaEjecucion
        return pilaEjecucion.pop()
    elif pilaNom == CONST_RETORNO_VALOR:
        global pilaRetorno
        return pilaRetorno.pop()
    elif pilaNom == CONST_FUNCION_RETORNO:
        global pilaFuncion
        return pilaFuncion.pop()

def top(pilaNom):
    if pilaNom == CONST_EJECUCION:
        global pilaEjecucion
        aux = len(pilaEjecucion) - 1
        if (aux < 0):
            return 'vacia'
        return pilaEjecucion[aux]
    elif pilaNom == CONST_TEMPORAL:
        global pilaTemporal
        aux = len(pilaTemporal) - 1
        if (aux < 0):
            return 'vacia'
        return pilaTemporal[aux]

'''
Funcion para obtener el valor de la direccion
'''
def getValor(memVirtual, memDireccion, memTipo):
    print("Valor = ", memDireccion)
    #Obtiene el v
    #if (direccion >= 0 and direccion <  )

'''
Funcion para obtener el tipo de la direccion
'''
def getTipo(direccion):
    print ("Tipo = ", direccion)
    direccion = int(direccion)
    if ((direccion >= BASE_DIRGLOBALNUM_LI and direccion <= BASE_DIRGLOBALNUM_LS) or (direccion >= BASE_DIRLOCALNUM_LI and direccion <= BASE_DIRLOCALNUM_LS) or (direccion >= BASE_DIRTEMPNUM_LI and direccion <= BASE_DIRTEMPNUM_LS) or (direccion >= BASE_DIRCONSTNUM_LI and direccion <= BASE_DIRCONSTNUM_LS) ):
        return 'number'
    if ((direccion >= BASE_DIRGLOBALSTR_LI and direccion <= BASE_DIRGLOBALSTR_LS) or (direccion >= BASE_DIRLOCALSTR_LI and direccion <= BASE_DIRLOCALSTR_LS) or (direccion >= BASE_DIRTEMPSTR_LI and direccion <= BASE_DIRTEMPSTR_LS) or (direccion >= BASE_DIRCONSTSTR_LI and direccion <= BASE_DIRCONSTSTR_LS) ):
        return 'string'
    if (direccion >= BASE_DIRTEMPBOOL_LI and direccion <= BASE_DIRTEMPBOOL_LS):
        return 'bool'
    if (direccion >= BASE_DIRTEMPPOINTNUM_LI and direccion <= BASE_DIRTEMPPOINTNUM_LS):
        return 'pointer number'
    if (direccion >= BASE_DIRTEMPPOINTSTR_LI and direccion <= BASE_DIRTEMPPOINTSTR_LS):
        return 'pointer string'
    else:
        print("Error Maquina Virtual: {} no se encuentra dentro del rango de ningun tipo de variable".format(direccion))
        sys.exit()

'''
Funcion para meter los valores en la memoria
'''
def llenarValor(memoriaVirtual, memDireccion, memTipo, valor):
    global memGlobal
    print (memDireccion)
    #obtiene el valor de la direccion
    #guarda el valor en la memoria principal

'''
Funcion para realizar operaciones aritmeticas
'''
def resOpeBool(res):
    if res == True:
        return 1
    elif res == False:
        return 0

def operadores(signo):
    global cuadruplos
    global pilaEjecucion

    tipo1 = getTipo(cuadruplos[1])
    tipo2 = getTipo(cuadruplos[2])
    val1 = getValor(pilaCorriendo, cuadruplos[1], tipo1)
    val2 = getValor(pilaCorriendo, cuadruplos[2], tipo2)

    if tipo1 == 'number' and tipo2 == 'number':
        val1 = int(val1)
        val2 = int(val2)

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

    elif tipo1 == 'string' and tipo2 == 'string':
        if  signo == '<>':
            res = resOpeBool(val1 != val2)
        elif signo == '==':
            res = resOpeBool(val1 == val2)
        elif signo == '&':
            res = val1 + val2
    
    llenarValor(pilaCorriendo, cuadruplos[3], getTipo(cuadruplos[3]), res)

'''
DECLARACION DE VARIABLES GLOBALES
'''
cuadIndice = 0

def main():
    Termina = False
    #print (cuadruplo[0])
    while not Termina:
        sigCuadIndice = -1
        pilaCorriendo = top(CONST_EJECUCION)
        print ("Ejecutando cuadruplo = ", cuadruplos[cuadIndice])
        cuadruplo = cuadruplos[cuadIndice]
        print ("Operacion = ", cuadruplo[0])

        # Asignacion
        if cuadruplo[0] == '=':
            try:  
                valor = getValor(pilaCorriendo, cuadruplo[1], getTipo(cuadruplo[1]))
            except:
                valor = pop(CONST_RETORNO_VALOR)
            
            llenarValor(pilaCorriendo, cuadruplo[3], getTipo(cuadruplo[3]), valor)

        # Lectura
        elif cuadruplo[0] == 'READ':
            auxTipo = getTipo(cuadruplo[1])
            #saber que tipo de valor esta leyendo para guardarlo en el espacio de memoria correspondiente

        # Escritura
        elif cuadruplo[0] == 'PRINT':
            texto = getValor(pilaCorriendo, cuadruplo[1], getTipo(cuadruplo[1]))
            print("<< ",str(texto))
        
        # GOTO
        elif cuadruplo[0] == 'GOTO':
            sigCuadIndice = int(cuadruplo[3])
            print (sigCuadIndice)
        # GOTOF
        # GOTOV
        # GOSUB
        # ERA
        # PARAMETER
        # ENDFUNC
        #elif cuadruplo[0] == 'ENDFUNC':
        
        # OBJREF
        # SUMREF
        # VERIFY
        # CNUM
        # CSTR
        # RET

        #Control de índices para el cuadIndice o sigCuadIndice
        # if sigCuadIndice != -1:
        #     cuadIndice = sigCuadIndice
        # else: 
        #     cuadIndice = cuadIndice + 1
        
        Termina = True

'''
EJECUTAR EL ARCHIVO CON EL CODIGO INTERMEDIO Y
PASA LOS CUADRUPLOS COMO TUPLA A UNA LISTA PARA PODER SER ACCESADOS
'''
cuadLista = []
cuadruplos = []

codObj = open("codint.txt", 'r', encoding='utf-8')
cuadLista = codObj.readlines()

for linea in cuadLista:
    linea = linea.replace('\n', '')
    cuadruplo = tuple(linea.split(','))
    cuadruplo = (cuadruplo[0], cuadruplo[1], cuadruplo[2], cuadruplo[3])
    cuadruplos.append(cuadruplo)

main()