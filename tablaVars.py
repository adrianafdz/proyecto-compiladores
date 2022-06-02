###------------------
#   La tabla de variables es representado por un diccionario.
#
#   Los atributos semánticos que contiene son:
#   - nombre de la variable
#   - tipo de la variable 
#   - dimension de la variable (de tipo dimStructure)
#   - dirección de memoria
#   - valor: valor de la constante (esto solo se utiliza para las constantes)
#
#   Esta clase se utiliza para el directorio de funciones y para almacenar constantes
###------------------

import json


class tablaVars:

    # Constructor para la tabla de variables
    # Se inializa vacía, pero opcionalmente se le puede pasar una tabla de variables ya exitente (se utiliza para la herencia de clases)
    def __init__(self, vars = {}):
        self.tabla_vars = vars.copy()

    # Verifica si existe la variable 'nombre'
    def check_var(self, nombre):
        return nombre in self.tabla_vars.keys()

    # Agregar una variable a la tabla de variables
    def add_var(self, nombre, tipo, dimension, memoria, cte = False):
        if self.check_var(nombre):
            print("Error: la variable", str(nombre), "ya existe")
            return False
        else:
            self.tabla_vars[nombre] = {
                'nombre': nombre,
                'tipo': tipo,
                'dimension': dimension,
                'memoria': memoria
            }
            return True

    # Agrega un registro para el valor de retorno de una función
    def add_return_value(self, nombre, tipo, memoria):
        self.tabla_vars[nombre] = {
            'nombre' : nombre,
            'tipo' : tipo,
            'dimension' : None,
            'memoria' : memoria
        }

    # Regresa el registro del valor de retorno de una función
    def get_return_value(self, nombre):
        if nombre not in self.tabla_vars:
            return (-1, -1)
        return self.tabla_vars[nombre]['tipo'], self.tabla_vars[nombre]['memoria']

    # Obtener el registro de una variable
    # Regresa su tipo y dirección
    def get_var(self, nombre):
        if self.check_var(nombre):
            return (self.tabla_vars[nombre]['tipo'], self.tabla_vars[nombre]['memoria'])
        else:
            return (-1, -1)

    # Regresa la dimensión de una variable (None o una instancia de dimStructure)
    def get_dim(self, nombre):
        if nombre in self.tabla_vars and 'dimension' in self.tabla_vars[nombre]:
            return self.tabla_vars[nombre]['dimension']
        return False

    # Imprimir la tabla
    def __repr__(self):
        output = ""
        for key1, value1 in self.tabla_vars.items():
            output += str(key1) + ' : { \n'
            for key2, value2 in value1.items():
                output += str(key2) + ' : ' + str(value2) + '\n'
            output += '} \n'
        return output

    # Imprimir la tabla
    def __str__(self):
        output = ""
        for key1, value1 in self.tabla_vars.items():
            output += '\t' + str(key1) + ' : { \n'
            for key2, value2 in value1.items():
                output += '\t\t' + str(key2) + ' : ' + str(value2) + '\n'
            output += '\t } \n'
        return output

    # Transforma la tabla de variables, cambiando la llave a la dirección de memoria,
    # y lo almacena en un archivo json.
    # Esto para poder acceder a los valores desde la máquina virtual y poder buscarlos por su dirección
    def generate_file(self):
        new_table = {}
        for key1, value1 in self.tabla_vars.items():
            new_table[value1['memoria']] = value1

        # self.tabla_vars = new_table
        with open("constantes.json", "w") as outfile:
            json.dump(self.tabla_vars, outfile)