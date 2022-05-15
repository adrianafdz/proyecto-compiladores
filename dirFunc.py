###------------------
#   Directorio de funciones
#
#   Los atributos semánticos que contiene son:
#   - nombre de la funcion
#   - tipo
#   - starts (en qué cuádruplo empieza)
#   - recursos (tamaño de memoria que ocupa)
#   - tabla de variables
#   - lista de tipos de los parámetros
#
###------------------

tipos = [0, 1, 2] # number, string, nothing

from tablaVars import tablaVars

class dirFunc:
    def __init__(self, funcs = {}):
        self.dir_func = funcs.copy()

    def add_func(self, nombre, cuadStart, tipo = 2):
        if nombre not in self.dir_func:
            self.dir_func[nombre] = {
                'tipo': tipo,
                'vars' : tablaVars(),
                'inicio': cuadStart
            }
        else:
            print("Error: la funcion", str(nombre), "ya existe")
            return False
        return True

    def get_func(self, nombre): # regresa tipo y en qué cuadruplo empieza
        if nombre in self.dir_func:
            return (self.dir_func[nombre]['tipo'], self.dir_func[nombre]['inicio'])
        else:
            print("Error: la funcion", str(nombre), "no existe")
            return (-1, -1)

    def update_func_type(self, nombre, tipo):
        if nombre in self.dir_func:
            self.dir_func[nombre]['tipo'] = tipo
        else:
            print("Error: la funcion", str(nombre), "no existe")
            return False
        return True

    def add_resources(self, nombre, cantidad):
        if nombre in self.dir_func:
            self.dir_func[nombre]['recursos'] = cantidad
        else:
            print("Error: la funcion", str(nombre), "no existe")
            return False
        return True

    def add_var(self, func, nombre, tipo, dimension, memoria):
        if nombre not in self.dir_func:
            self.dir_func[func]['vars'].add_var(nombre, tipo, dimension, memoria)
        else:
            print("Error: la variable", str(nombre), "ya existe")
            return False
        return True

    def get_var(self, func, nombre):
        # regresa el tipo y la direccion de memoria
        return self.dir_func[func]['vars'].get_var(nombre) 

    def add_param(self, func, tipo):
        if 'params' not in self.dir_func[func]:
            self.dir_func[func]['params'] = [tipo]
        else:
            self.dir_func[func]['params'].append(tipo)

    def create_dir_for_obj(self, nombre):
        if nombre in self.dir_func:
            self.dir_func[nombre]['funcs'] = dirFunc()
            return self.dir_func[nombre]['funcs']
        else:
            print("Error: el objeto", str(nombre), "no existe")
            return None

    def get_vars_from_obj(self, nombre):
        if nombre in self.dir_func:
            return self.dir_func[nombre]['vars']
        else:
            print("Error: el objeto", str(nombre), "no existe")
            return None

    def get_dir_from_obj(self, nombre):
        if nombre in self.dir_func:
            return self.dir_func[nombre]['funcs']
        else:
            print("Error: el objeto", str(nombre), "no existe")
            return None

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
                'funcs': funcs
            }

            return True
        else:
            print("Error: no existe la clase", str(nombre))
            return False
            

    def delete_func(self, nombre):
        del self.dir_func[nombre]

    def delete_var_table(self, nombre):
        del self.dir_func[nombre]['vars']

    def delete_dir(self):
        self.dir_func = {}

    def __str__(self):
        output = ""
        for key1, value1 in self.dir_func.items():
            output += key1 + ' : { \n'
            for key2, value2 in value1.items():
                output += '\t' + key2 + ' : ' + str(value2) + '\n'
            output += '} \n'
        return output