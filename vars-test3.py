from tablaVars import tablaVars
from dirFunc import dirFunc
from collections import deque

tipos = ["nothing", "number", "string"]

curr_dir = deque()
curr_func = deque()
curr_tipo = tipos[0]
dimension = None

####################################################
# <PROGRAMA>
# Crear dirFuncG, curr_dur.push(dirFuncG)
dirFuncG = dirFunc()
curr_dir.append(dirFuncG)

# Agregar a dirFuncG el id, curr_func.push(id)
id = "programa"
dirFuncG.add_func(id, curr_tipo)
curr_func.append(id)

# <VARS> - globales
id = "x"
curr_tipo = tipos[1]
dimension = None
curr_dir[-1].add_var(curr_func[-1], id, curr_tipo, dimension, 0)

id = "Y"
curr_tipo = tipos[2]
dimension = (2,3)
curr_dir[-1].add_var(curr_func[-1], id, curr_tipo, dimension, 0)

print(dirFuncG)

# ACABA EL PROGRAMA
curr_dir[-1].delete_dir()