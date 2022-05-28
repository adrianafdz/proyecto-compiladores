###------------------
#   El cubo semantico es representado por una matriz.
#
#   La estructura del cubo semantico es:
#   [operando1, operando2, operador] = tipo del resultado
#   
#   Tipo de datos:
#   - 0: number
#   - 1: string
#   - 2: bool
#   - 3: pointer num
#   - 4: pointer str
#   - 7: nothing
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
            '&' : 8,
            '=' : 9
        }

        self.cuboSeman =  [[  # number
                            #     +   -   *   /   >   <  <>  ==   &   =
                                [ 0,  0,  0,  0,  2,  2,  2,  2, -1,  0], # number
                                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # string
                                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # bool
                                [ 0,  0,  0,  0,  2,  2,  2,  2, -1,  0], # pointer num (pq en la maquina virtual se va a traer un numero)
                                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # pointer str
                            ], [ # string
                                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # number
                                [-1, -1, -1, -1, -1, -1,  2,  2,  1,  1], # string
                                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # bool
                                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # pointer num
                                [-1, -1, -1, -1, -1, -1,  2,  2,  1,  1]  # pointer str
                            ], [ # bool
                                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # number
                                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # string
                                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # bool
                                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # pointer num
                                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]  # pointer str
                            ], [ # pointer num
                                [ 0,  0,  0,  0,  2,  2,  2,  2, -1,  0], # number
                                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # string
                                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # bool
                                [ 0,  0,  0,  0,  2,  2,  2,  2, -1,  0], # pointer num
                                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # pointer str
                            ], [ # pointer str
                                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # number
                                [-1, -1, -1, -1, -1, -1,  2,  2,  1,  1], # string
                                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # bool
                                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # pointer num
                                [-1, -1, -1, -1, -1, -1,  2,  2,  1,  1]  # pointer str
                            ], 
                            
                            ]

    def check(self, op, t1, t2):
        if t1 == 7 or t2 == 7: # uno es nothing, no se pueden hacer operaciones
            return -1
            
        return self.cuboSeman[t1][t2][self.operadores[op]]

    # CUANDO OP = '=' y el t2 sea un apuntador, revisar si ya apunta a algo
    # si no, hacer que apunte a la direccion t1
    # si sí, asignarle t1 a la direccion a la que apunta t2

    # si t1 es un apuntador, siempre se toma la direccion a la que apunta, ya debe de traerla asignada
