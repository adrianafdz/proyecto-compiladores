import sys
from aloop import *
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
    if ((direccion >= 0 and direccion <= 2999) or (direccion >= 5000 and direccion <= 7999) or (direccion >= 10000 and direccion <= 12999) or (direccion >= 17000 and direccion <= 21999) ):
        return 'number'
    if ((direccion >= 3000 and direccion <= 4999) or (direccion >= 8000 and direccion <= 9999) or (direccion >= 13000 and direccion <= 13999) or (direccion >= 22000 and direccion <= 26999) ):
        return 'string'
    if (direccion >= 14000 and direccion <= 14999):
        return 'bool'
    else:
        print("Error Maquina Virtual: {} no se encuentra dentro del rango de ningun tipo de variable".format(direccion))
        sys.exit()

'''
Funcion para meter los valores en la memoria
'''
def llenarValor(memoriaVirtual, memDireccion, memTipo, valor):
    global memGlobal
    #obtiene el valor de la direccion
    #guarda el valor en la memoria principal

'''
Funcion para realizar operaciones aritmeticas
'''
def resOpeBool(res):
    if res == True:
        print ('1')
    elif res == False:
        print ('0')

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
            res = val1 > val2
            resOpeBool(res)
        elif signo == '<':
            res = val1 < val2
            resOpeBool(res)
        elif signo == '<>':
            res = val1 != val2
            resOpeBool(res)
        elif signo == '==':
            res = val1 == val2
            resOpeBool(res)

    elif tipo1 == 'string' and tipo2 == 'string':
        if  signo == '<>':
            res = val1 != val2
            resOpeBool(res)
        elif signo == '==':
            res = val1 == val2
            resOpeBool(res)
        '''
        Operacion con '&' 
        elif signo == '&':
            res
        ''' 
    
    llenarValor(pilaCorriendo, cuadruplos[3], getTipo(cuadruplos[3]), res)

    def main():
        Finish = False
        while not Finish:
            sigCuadIndice = -1
            pilaCorriendo = top(CONST_EJECUCION)
            cuadruplos = cuadLista[cuadIndice] #Cuadruplo a ejecutar

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
            # GOTOF
            # GOTOV
            # GOSUB
            # ERA
            # PARAMETER
            # ENDFUNC
            # OBJREF
            # SUMREF
            # VERIFY
            # CNUM
            # CSTR
            # RET
