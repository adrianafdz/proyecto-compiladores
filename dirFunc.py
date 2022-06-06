###------------------
#   Directorio de funciones
#
#   Los atributos semánticos que contiene son:
#   - nombre de la funcion
#   - tipo
#   - inicio (en qué cuádruplo empieza)
#   - recursos (tamaño de memoria que ocupa): [Num, Str, Bool, PtNum, PtStr]
#   - tabla de variables
#   - lista de tipos de los parámetros
#   - directorio de funciones (para las clases)
#
###------------------

tipos = [0, 1, 2] # number, string, nothing

import json
from tablaVars import tablaVars

class dirFunc:
    def __init__(self, funcs = {}):
        self.dir_func = funcs.copy()

    # Registrar en el directorio una función de tipo 'tipo' que comienza en el cuadruplo cuadStart
    # si no se indica un tipo, se guarda como tipo nothing
    def add_func(self, nombre, cuadStart, tipo = 7):
        if nombre not in self.dir_func:
            self.dir_func[nombre] = {
                'tipo': tipo,
                'vars' : tablaVars(),
                'inicio': cuadStart,
                'params': list()
            }
        else:
            return False
        return True

    def get_func(self, nombre):
        if nombre in self.dir_func:
            return (self.dir_func[nombre]['tipo'], self.dir_func[nombre]['inicio'])
        else:
            return (-1, -1)

    # Actualiza el tipo de una función (porque las funciones primero se dan de alta y luego se encuentra el tipo)
    def update_func_type(self, nombre, tipo):
        if nombre in self.dir_func:
            self.dir_func[nombre]['tipo'] = tipo
        else:
            return False
        return True

    # Al terminar de compilar una función se registran cuántos recursos utilizó
    def add_resources(self, nombre, cantidades):
        if nombre in self.dir_func:
            self.dir_func[nombre]['recursos'] = cantidades # [Num, Str, Bool, PtNum, PtStr]
        else:
            return False
        return True

    # Agregar una variable a la tabla de variables de la función func
    # nombre: nombre de la variable
    # tipo: tipo de la variable
    # dimension: None o dimStructure ya solucionada
    # memoria: dirección
    def add_var(self, func, nombre, tipo, dimension, memoria):
        if nombre not in self.dir_func:
            return self.dir_func[func]['vars'].add_var(nombre, tipo, dimension, memoria)
        else:
            return False

    # Obtiene una variable de la función func
    # regresa el tipo y la direccion de memoria
    def get_var(self, func, nombre):
        return self.dir_func[func]['vars'].get_var(nombre) 

    # Agrega una nueva variable para manejar los retornos de las funciones
    # (no se utiliza la función add_var porque esa checa que no exista una función con el mismo nombre)
    def add_return_value(self, func, nombre, tipo, memoria):
        return self.dir_func[func]['vars'].add_return_value(nombre, tipo, memoria)

    # Regresa el tipo y la dirección del registro donde almacena la variable de retorno de la función func
    def get_return_value(self, func, nombre):
        return self.dir_func[func]['vars'].get_return_value(nombre)

    # Registra un parámetro de tipo 'tipo' para la función 'func'
    def add_param(self, func, tipo):
        if 'params_count' not in self.dir_func[func]:
            self.dir_func[func]['params'] = [tipo]
            self.dir_func[func]['params_count'] = 1
        else:
            self.dir_func[func]['params'].append(tipo)
            self.dir_func[func]['params_count'] += 1

    # (las clases se registran en el directorio de funciones principal)
    # Crear un directorio de funciones para la clase 'nombre'
    def create_dir_for_obj(self, nombre):
        if nombre in self.dir_func and self.dir_func[nombre]['tipo'] == 5:
            self.dir_func[nombre]['funcs'] = dirFunc()
            return self.dir_func[nombre]['funcs']
        else:
            return None

    # Obtiene la tabla de variables de la clase 'nombre'
    def get_vars_from_obj(self, nombre):
        if nombre in self.dir_func:
            return self.dir_func[nombre]['vars']
        else:
            return None

    # Obtiene el directorio de funciones de la clase 'nombre'
    def get_dir_from_obj(self, nombre):
        if nombre in self.dir_func:
            return self.dir_func[nombre]['funcs']
        else:
            return None

    # Obtiene la cantidad de recursos de la función o clase 'nombre'
    def get_resources(self, nombre):
        if nombre in self.dir_func:
            return self.dir_func[nombre]['recursos']
        else:
            return None

    # Obtiene la lista de parámetros de una función
    def get_params(self, nombre):
        if nombre in self.dir_func:
            return self.dir_func[nombre]['params']
        else:
            return None

    # Copia el directorio de funciones de la clase padre a la clase hijo
    def copy_class_to(self, padre, hijo):
        p = self.dir_func[padre]
        if padre in self.dir_func:
            if 'funcs' in self.dir_func[padre]:
                funcs = dirFunc(p['funcs'].dir_func)
            else:
                funcs = dirFunc()

            self.dir_func[hijo] = {
                'tipo': p['tipo'],
                'vars': tablaVars(p['vars'].tabla_vars),
                'funcs': funcs,
                'inicio': p['inicio'],
                'params': p['params'].copy(),
                'recursos': p['recursos'].copy()
            }

            return True
        else:
            return False
            
    # Obtiene la dimensión de una variable, ya se None o una instancia de dimStructure
    def get_dim(self, func, nombre):
        return self.dir_func[func]['vars'].get_dim(nombre)

    # Elimina el registro de la función 'nombre'
    def delete_func(self, nombre):
        del self.dir_func[nombre]

    # Elimina la tabla de variables de la función 'nombre'
    def delete_var_table(self, nombre):
        del self.dir_func[nombre]['vars']

    # Elimina el directorio de funciones
    def delete_dir(self):
        self.dir_func = {}

    # Imprimir directorio de funciones
    def __str__(self):
        output = ""
        for key1, value1 in self.dir_func.items():
            output += key1 + ' : { \n'
            for key2, value2 in value1.items():
                output += '\t' + key2 + ' : ' + str(value2) + '\n'
            output += '} \n'
        return output

    # Genera un archivo json en donde se almacenan los recursos que utiliza cada función
    # Este archivo lo utiliza la máquina virtual para la administración de memoria
    def generate_file(self):
        data = self.transform()

        with open("recursos.json", "w") as outfile:
            json.dump(data, outfile)

    def transform(self):
        resources_data = {}
        for key1, value1 in self.dir_func.items():
            if 'funcs' in value1: # es una clase
                resources_class = value1['funcs'].transform() # recursos de cada metodo
                resources_data[key1] = resources_class
            else: # es una función
                resources_data[key1] = value1['recursos']

        return resources_data
