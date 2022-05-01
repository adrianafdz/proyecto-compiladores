###------------------
#   El cubo semantico es representado por una matriz.
#
#   La estructura del cubo semantico es:
#   [operando1, operando2, operador] = tipo del resultado
#   
#   Tipo de datos:
#   - 0: number
#   - 1: string
#   - 2: nothing
#   - -1: error
#
#   Tipo de error:
#    - Error: Type Mismatch
#
###------------------

class cuboSemantico:
    #Constructor
    def __init__(self):
        self.operadores = {
            '+' : 0,
            '-' : 1,
            '*' : 2,
            '/' : 3,
            '>' : 4,
            '<' : 5,
            '<>' : 6,
            '==' : 7,
            '&' : 8
        }

        self.cuboSeman =  [[  # number
                            #     +   -   *   /   >   <  <>  ==   &
                                [ 0,  0,  0,  0,  0,  0,  0,  0, -1], # number
                                [-1, -1, -1, -1, -1, -1, -1, -1, -1]  # string
                            ], [ # string
                                [-1, -1, -1, -1, -1, -1,  0,  0,  1], # number
                                [-1, -1, -1, -1, -1, -1, -1, -1, -1]  # string
                            ]]

    def check(self, op, t1, t2):
        if t1 == 2 or t2 == 2: # uno es nothing
            return -1
        return self.cuboSeman[t1][t2][self.operadores[op]]