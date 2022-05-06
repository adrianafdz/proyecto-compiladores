from tablaVars import tablaVars

class Cuadruplos():
    def __init__(self):
        self.cuadruplos = list()

    def add(self, op, izq, der, res):
        self.cuadruplos.append((op, izq, der, res))

    def __str__(self):
        output = ""
        for c in self.cuadruplos:
            output += str(c) + '\n'
        return output
    
    #Leer: input()
    def read(self, cuadruplos, nombre):
        if (cuadruplos[0] == 'leer'):
            texto = tablaVars.search_var(nombre)
            if (tablaVars.searchType_var == 'number'):
                print ("Valor tipo number") #Aplicar funcion to_string 
            elif(tablaVars.searchType_var == 'string'):
                print ("Valor tipo string")
        else:
            print("error")

    #Escribir: print(<string>)
    def write(self, cuadruplos, cadena):
        if (cuadruplos[0] == 'escribir'):
            texto = tablaVars.search_var(cadena)
            print(">>", str(texto))
        else:
            print("error")

    #Regresar 
    def ret(self, cuadruplos, valor):
        stackRetorno = []
        if (cuadruplos[0] == 'regresar'):
            texto = tablaVars.search_var(valor)
            stackRetorno.append(texto) #Guarda el valor 
        else:
            print("error")
