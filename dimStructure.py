###------------------
#   DimStructure
#   Clase para las dimensiones de arreglos y matrices
#
#   Hace los cálculos necesarios para obtener su tamaño 
#   y para hacer las operaciones correspondientes al momento de indexar
###------------------

class DimStructure:
    def __init__(self):
        self.DIM = 0 # cantidad de dimensiones (1 o 2)
        self.R = 1
        self.up_lim = list() # límites superiores de cada dimension
        # los límites inferiores son siempre 0, entonces no hay offset
        self.m = list()
        self.size = 0 # tamaño de toda la estructura

    # Agrega un nuevo nodo con su límite superior
    # y va haciendo las operaciones para calcular el tamaño
    def add_upper_lim(self, value):
        self.up_lim.append(int(value)) # asegurar que sea número entero
        self.R = self.R * (int(value))
        self.DIM += 1

    # Resuelve las m cuando ya se registraron todas las dimensiones
    def solve(self):
        self.size = self.R

        for i in range(len(self.up_lim)):
            self.m.append(self.R / self.up_lim[i])
            self.R = self.m[i]

    # Imprimir la estructura (solo para probar)
    def print(self):
        print("R", self.R)
        print("dims", self.up_lim)
        print("num indexes", self.DIM)
        print("m", self.m)
        print("size", self.size)

    # Obtiene el tamaño de todo el arreglo o matriz
    def get_size(self):
        return self.size

    # Obtiene la cantidad de dimensiones (1 o 2)
    def get_num_dims(self):
        return self.DIM

    # Obtiene los valores del nodo n (límite superior_n y m_n)
    def get_node(self, n):
        return self.up_lim[n - 1], self.m[n - 1]

    # Revisa si es el último nodo
    def is_last_node(self, n):
        return n == len(self.up_lim)

# # TEST
# d = DimStructure()
# d.add_upper_lim(5)
# d.add_upper_lim(7)
# d.solve()
# d.print()

# print(d.index(0, [2, 4]))