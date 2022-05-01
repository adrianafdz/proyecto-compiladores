# TEST HERENCIA
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

####################################################
# <CLASE>
# Agregar id (tipo nothing) a curr_dir.top(), curr_func.push(id)
id = "clasePadre"
curr_dir[-1].add_func(id, curr_tipo)
curr_func.append(id)

# Generar un directorio de funciones DirFuncObj para curr_func.top()
dirFuncObj = curr_dir[-1].create_dir_for_obj(curr_func[-1])

# <VARS> - en una clase
id = "classvar1"
curr_tipo = tipos[1]
dimension = None
curr_dir[-1].add_var(curr_func[-1], id, curr_tipo, dimension, 0)

# curr_dir.push(DirFuncObj)
curr_dir.append(dirFuncObj)

# <FUNCION> - EN UN OBJETO
# Agregar id a curr_dir.top(), curr_func.push(id)
id = "classfunc1"
curr_dir[-1].add_func(id)
curr_func.append(id)

# <PARAMS>
# Agregar id con el curr_tipo a curr_dir.top()[curr_func.top()]
curr_tipo = tipos[1]
id = "p1"
curr_dir[-1].add_var(curr_func[-1], id, curr_tipo, dimension, 0)

# tipo de la funcion
curr_tipo = tipos[1]
# Actualizar el tipo de curr_dir.top()[curr_func.top()] con curr_tipo
curr_dir[-1].update_func_type(curr_func[-1], curr_tipo)

# <VARS> - de la funcion
# Agregar variable id con curr_tipo y dimension a curr_dir.top()[curr_func.top()]
id = "varfunc"
curr_tipo = tipos[1]
dimension = None
curr_dir[-1].add_var(curr_func[-1], id, curr_tipo, dimension, 0)

# acaba funcion
# Eliminar tabla de variables de curr_func.top(), curr_func.pop()
curr_dir[-1].delete_var_table(curr_func[-1])
curr_func.pop()

# ACABA LA CLASE
curr_dir.pop()
curr_func.pop()

####################################################
# <CLASE>
# Agregar id (tipo nothing) a curr_dir.top(), curr_func.push(id)
id = "claseHijo"
curr_dir[-1].add_func(id, curr_tipo)
curr_func.append(id)

# Generar un directorio de funciones DirFuncObj para curr_func.top()
dirFuncObj = curr_dir[-1].create_dir_for_obj(curr_func[-1])

# HERENCIA
id = "clasePadre"
curr_dir[-1].copy_class_to(id, curr_func[-1])
dirFuncObj = curr_dir[-1].get_dir_from_obj(curr_func[-1])

# <VARS> - en una clase
id = "hijovar1"
curr_tipo = tipos[1]
dimension = None
curr_dir[-1].add_var(curr_func[-1], id, curr_tipo, dimension, 0)

# curr_dir.push(DirFuncObj)
curr_dir.append(dirFuncObj)

# <FUNCION> - EN UN OBJETO
# Agregar id a curr_dir.top(), curr_func.push(id)
id = "hijofunc1"
curr_dir[-1].add_func(id)
curr_func.append(id)

# <PARAMS>
# Agregar id con el curr_tipo a curr_dir.top()[curr_func.top()]
curr_tipo = tipos[1]
id = "h1"
curr_dir[-1].add_var(curr_func[-1], id, curr_tipo, dimension, 0)

# tipo de la funcion
curr_tipo = tipos[1]
# Actualizar el tipo de curr_dir.top()[curr_func.top()] con curr_tipo
curr_dir[-1].update_func_type(curr_func[-1], curr_tipo)

# <VARS> - de la funcion
# Agregar variable id con curr_tipo y dimension a curr_dir.top()[curr_func.top()]
id = "varhijofunc"
curr_tipo = tipos[1]
dimension = None
curr_dir[-1].add_var(curr_func[-1], id, curr_tipo, dimension, 0)

# acaba funcion
# Eliminar tabla de variables de curr_func.top(), curr_func.pop()
curr_dir[-1].delete_var_table(curr_func[-1])
curr_func.pop()

# ACABA LA CLASE
curr_dir.pop()
curr_func.pop()

print(dirFuncG)

# ACABA EL PROGRAMA
curr_dir[-1].delete_dir()