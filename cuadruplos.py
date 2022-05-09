from tablaVars import tablaVars

class Cuadruplos():
    def __init__(self):
        self.cuadruplos = list()
        self.cont = 1

    def add(self, op, izq, der, res):
        self.cuadruplos.append((op, izq, der, res))
        self.cont += 1

    def get_cont(self):
        return self.cont

    def fill(self, cuadruplo, value):
        self.cuadruplos[cuadruplo-1] = self.cuadruplos[cuadruplo-1][:-1] + tuple([value]) 

    def __str__(self):
        output = ""
        i = 1
        for c in self.cuadruplos:
            output += str(i) + ":- " + str(c) + '\n'
            i += 1
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
