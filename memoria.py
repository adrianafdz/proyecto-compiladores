from dirVirtuales import *

class Memoria():
    def __init__(self, recursos):
        self.number_type = [None] * recursos[0]
        self.string_type = [None] * recursos[1]

        self.bool_type = [None] * recursos[2]
        self.point_number_type = [None] * recursos[3]
        self.point_string_type = [None] * recursos[4]

        self.temp_number_type = [None] * recursos[0]
        self.temp_string_type = [None] * recursos[1]

        self.count_number_params = 0
        self.count_string_params = 0

    def get_index(self, address):
        address = int(address)
        if address >= BASE_DIRGLOBALNUM_LI and address <= BASE_DIRGLOBALNUM_LS: # GLOBAL NUMBER
            indice = address - BASE_DIRGLOBALNUM_LI
            tipo = 0
        elif address >= BASE_DIRGLOBALSTR_LI and address <= BASE_DIRGLOBALSTR_LS: # GLOBAL STRING
            indice = address - BASE_DIRGLOBALSTR_LI
            tipo = 1
        elif address >= BASE_DIRLOCALNUM_LI and address <= BASE_DIRLOCALNUM_LS: # LOCAL NUMBER
            indice = address - BASE_DIRLOCALNUM_LI
            tipo = 0
        elif address >= BASE_DIRLOCALSTR_LI and address <= BASE_DIRLOCALSTR_LS: # LOCAL STRING
            indice = address - BASE_DIRLOCALSTR_LI
            tipo = 1
        elif address >= BASE_DIRTEMPBOOL_LI and address <= BASE_DIRTEMPBOOL_LS: # BOOLEAN
            indice = address - BASE_DIRTEMPBOOL_LI
            tipo = 2
        elif address >= BASE_DIRTEMPPOINTNUM_LI and address <= BASE_DIRTEMPPOINTNUM_LS: # POINTER NUMBER
            indice = address - BASE_DIRTEMPPOINTNUM_LI
            tipo = 3
        elif address >= BASE_DIRTEMPPOINTSTR_LI and address <= BASE_DIRTEMPPOINTSTR_LS: # POINTER STRING
            indice = address - BASE_DIRTEMPPOINTSTR_LI
            tipo = 4
        elif address >= BASE_DIRTEMPNUM_LI and address <= BASE_DIRTEMPNUM_LS: # TEMP NUMBER
            indice = address - BASE_DIRTEMPNUM_LI
            tipo = 5
        elif address >= BASE_DIRTEMPSTR_LI and address <= BASE_DIRTEMPSTR_LS: # TEMP STRING
            indice = address - BASE_DIRTEMPSTR_LI
            tipo = 6
        else:
            indice = -1
            tipo = -1
        
        return indice, tipo

    def set_data(self, address, value):
        address = int(address)
        indice, tipo = self.get_index(address)
        # print(address, indice)

        if tipo == 0:
            self.number_type[indice] = float(value)
        elif tipo == 1:
            self.string_type[indice] = str(value)
        elif tipo == 2:
            self.bool_type[indice] = int(value) # 1 o 0
        elif tipo == 3:
            self.point_number_type[indice] = int(value) # una direccion
        elif tipo == 4:
            self.point_string_type[indice] = int(value) # una direccion
        elif tipo == 5:
            self.temp_number_type[indice] = float(value) 
        elif tipo == 6:
            self.temp_string_type[indice] = str(value)
        else:
            return False

        return True

    def get_data(self, address):
        indice, tipo = self.get_index(address)
        value = None

        if tipo == 0:
            value = self.number_type[indice]
        elif tipo == 1:
            value = self.string_type[indice]
        elif tipo == 2:
            value = self.bool_type[indice]
        elif tipo == 3:
            value = self.point_number_type[indice]
        elif tipo == 4:
            value = self.point_string_type[indice]
        elif tipo == 5:
            value = self.temp_number_type[indice]
        elif tipo == 6:
            value = self.temp_string_type[indice]

        return value, tipo

    def set_parameter(self, value, type):
        if type == 0 or type == 5:
            self.number_type[self.count_number_params] = float(value)
            self.count_number_params += 1
        elif type == 1 or type == 6:
            self.string_type[self.count_string_params] = str(value)
            self.count_string_params += 1

    def print(self):
        print("NUM:", self.number_type)
        print("BOOL:", self.bool_type)
        print("TEMP:", self.temp_number_type)
        print("PNUM:", self.point_number_type)