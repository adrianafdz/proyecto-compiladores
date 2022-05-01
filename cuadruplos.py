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