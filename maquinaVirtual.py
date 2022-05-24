from aloop import *

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

#Funciones de control de las pilas
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
