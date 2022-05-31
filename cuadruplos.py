###------------------
#   CUADRUPLOS
#   Clase para el manejo de cuádruplos
# 
#   Los cuádruplos son represetandos por tuplas
###------------------

from tablaVars import tablaVars

class Cuadruplos():
    def __init__(self):
        self.cuadruplos = list()
        self.cont = 1

    # Generar un cuádruplo
    def add(self, op, izq, der, res):
        self.cuadruplos.append((op, izq, der, int(res)))
        self.cont += 1

    # Obtener dónde va el contador de cuadruplos
    def get_cont(self):
        return self.cont

    # Rellenar un cuádruplo que ya había sido creado (para los GOTO)
    def fill(self, cuadruplo, value):
        self.cuadruplos[cuadruplo-1] = self.cuadruplos[cuadruplo-1][:-1] + tuple([value]) 

    # Método para imprimir los cuadruplos en consola
    def __str__(self):
        output = ""
        i = 1
        for c in self.cuadruplos:
            output += str(i) + ":- " + str(c) + '\n'
            i += 1
        return output

    # Método para escribir los cuadruplos en un archivo
    def generate_file(self):
        f = open("codint.txt", "w")

        for c in self.cuadruplos:
            f.write(",".join([str(x) for x in c]) + "\n")

        f.close()