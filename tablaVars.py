###------------------
#   La tabla de variables es representado por un diccionario.
#
#   Los atributos semánticos que contiene son:
#   -nombre de la variable
#   -tipo de la variable 
#   -dimension de la variable (tupla de 1 o 2 elementos)
#   -posicion de memoria
#
#   El formato es:
#   tabla_vars = {nombre: nombre, tipo, dimension, memoria}
###------------------

class tablaVars:

    #Constructor para la tabla de variables
    def __init__(self, vars = {}):
        self.tabla_vars = vars.copy()

    #Verificador de vars por si ya existe una
    def check_var(self, nombre):
        return nombre in self.tabla_vars.keys()

    #Agregar vars a la tabla de variables
    def add_var(self, nombre, tipo, dimension, memoria):
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

    def get_var(self, nombre):
        if self.check_var(nombre):
            return (self.tabla_vars[nombre]['tipo'], self.tabla_vars[nombre]['memoria'])
        else:
            return (-1, -1)

    #Regresar los datos de una variable especifica
    def search_var(self, nombre):
        if self.check_var(nombre):
            return self.tabla_vars[nombre]
        else:
            return None

    #Regresar el tipo de una variable especifica
    def searchType_var(self, nombre):
        if self.check_var(nombre):
            return self.tabla_vars[nombre]['tipo']
        else:
            return -1

    #Regresar la dimesion de una variable especifica
    def searchMem_var(self, nombre):
        if self.check_var(nombre):
            return self.tabla_vars[nombre]['dimension']
        else:
            return None

    #Regresar la posición de memoria de una variable especifica
    def searchMem_var(self, nombre):
        if self.check_var(nombre):
            return self.tabla_vars[nombre]['memoria']
        else:
            return None

    def __repr__(self):
        output = ""
        for key1, value1 in self.tabla_vars.items():
            output += key1 + ' : { \n'
            for key2, value2 in value1.items():
                output += key2 + ' : ' + value2 + '\n'
            output += '} \n'
        return output

    def __str__(self):
        output = ""
        for key1, value1 in self.tabla_vars.items():
            output += '\t' + key1 + ' : { \n'
            for key2, value2 in value1.items():
                output += '\t\t' + key2 + ' : ' + str(value2) + '\n'
            output += '\t } \n'
        return output