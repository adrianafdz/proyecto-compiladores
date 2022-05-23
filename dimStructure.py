tipos = [0, 1, 2] # number, string, nothing

class DimStructure:
    def __init__(self):
        self.DIM = 0
        self.R = 1
        self.up_lim = list()
        self.m = list()
        self.size = 0

    def add_upper_lim(self, value):
        self.up_lim.append(value)
        self.R = self.R * (value)
        self.DIM += 1

    def solve(self):
        self.size = self.R

        for i in range(len(self.up_lim)):
            self.m.append(self.R / self.up_lim[i])
            self.R = self.m[i]

    def print(self):
        print("R", self.R)
        print("dims", self.up_lim)
        print("num ibdexes", self.DIM)
        print("m", self.m)
        print("size", self.size)

    def index(self, base, values):
        if len(values) != len(self.up_lim):
            print("ERROR")
            return -1

        suma = 0
        for i in range(len(values)):
            suma += values[i] * self.m[i]
        return base + suma

    def get_size(self):
        return self.size

    def get_num_dims(self):
        return self.DIM

    def get_node(self, num):
        return self.up_lim[num - 1], self.m[num - 1]

    def is_last_node(self, num):
        return num == len(self.up_lim)

    def __str__(self):
        return str(self.up_lim)

    def __repr__(self):
        return str(self.up_lim)

# # TEST
# d = DimStructure()
# d.add_upper_lim(5)
# d.add_upper_lim(7)
# d.solve()
# d.print()

# print(d.index(0, [2, 4]))