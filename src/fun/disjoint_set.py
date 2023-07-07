import numpy as np

class DisjointSet:

    def find(self, i):
        if (self.__ps[i] < 0):
            return i

        self.__ps[i] = self.find(self.__ps[i])
        return self.__ps[i]

    def same(self, i, j):
        p_i = self.find(i)
        p_j = self.find(j)
        return p_i == p_j

    def union(self, i, j):
        p_i = self.find(i)
        p_j = self.find(j)
        if (p_i == p_j):
            return False

        if (self.__ps[p_i] <= self.__ps[p_j]):
            self.__ps[p_j] = p_i
        else:
            self.__ps[p_i] = p_j
    
        return True

    def __init__(self, size):
        self.__ps = np.ones((size), dtype=np.int32) * -1

# Test
# u = DisjointSet(10)
# u.union(0, 1)
# u.union(1, 2)
# print(u.find(2))    