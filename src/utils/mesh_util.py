import numpy as np

from src.consts import INDEX_KEY_STRING, POSITION_KEY_STRING

def CaluculateNormal(A, B, C):
    AB = B - A
    AC = C - A

    n = np.cross(AB, AC)
    n /= pow(np.dot(n, n), 0.5)
    return n

def IsCounterClockwise(A, B, C, n):
    AB = B - A
    AC = C - A
    cross = np.cross(AB, AC)

    return np.dot(n, cross) < 0

def fromArray(arr, idx):
    i3 = idx * 3
    return np.array(arr[i3:i3 + 3])

class GeometryBuilder:

    def __init__(self):

        self.__ps = []
        self.__is = []
        self.__mp = {}

    def insertVertex(self, cord, id):
        if (id in self.__mp):
            return self.__mp[id]
        else:
            curr_idx = int(len(self.__ps) / 3)
            self.__ps.append(cord[0])
            self.__ps.append(cord[1])
            self.__ps.append(cord[2])
            self.__mp[id] = curr_idx
            return curr_idx

    def insertFace(self, A1_i, B1_i, C1_i, A, B, C):
        A1 = fromArray(self.__ps, A1_i)
        B1 = fromArray(self.__ps, B1_i)
        C1 = fromArray(self.__ps, C1_i)
        N0 = CaluculateNormal(A, B, C)
        if (not IsCounterClockwise(A1, B1, C1, N0)):
            temp = B1_i
            B1_i = C1_i
            C1_i = temp
        
        self.__is.append(A1_i)
        self.__is.append(B1_i)
        self.__is.append(C1_i)
            

    def toGeoDict(self):
        return {POSITION_KEY_STRING: list(self.__ps), INDEX_KEY_STRING: list(self.__is)}

class GeometryEdgeList:

    class GeometryEdge:
        def __init__(self, u, v, weight):
            self.u = u
            self.v = v
            self.weight = weight

            self.relate = []

            if (u > v):
                self.u = v
                self.v = u

        def __str__(self):
            return f"({self.u}, {self.v}), weight: {self.weight}, relate: {self.relate}\n"

    def __init__(self):
        self.__list = []

    def exists(self, u, v):
        if (u > v):
            temp = u
            u = v
            v = temp

        begin = 0
        end = len(self.__list)
        while (begin < end):
            mid_idx = int((begin + end) / 2)
            mid_edge = self.__list[mid_idx]
            if (u == mid_edge.u and v == mid_edge.v):
                return True, mid_idx
            elif (u < mid_edge.u or (u == mid_edge.u and v < mid_edge.v)):
                end = mid_idx
            else:
                begin = mid_idx + 1

        return False, begin

    def insert(self, u, v, w, weight):
        if (u > v):
            temp = u
            u = v
            v = temp

        found, insert_idx = self.exists(u, v)
        if (found):
            edge = self.__list[insert_idx]
            if (not w in edge.relate):
                edge.relate.append(w)
            return False, insert_idx
        
        self.__list.insert(insert_idx, GeometryEdgeList.GeometryEdge(u, v, weight))
        self.__list[insert_idx].relate.append(w)

        return True, insert_idx

    def getRelate(self, i):
        return tuple(self.__list[i].relate)

    def toList(self):
        ans = []
        for i in range(len(self.__list)):
            edge = self.__list[i]
            ans.append((edge.weight, edge.u, edge.v, i))
        return ans

    def __str__(self):
        ans = ""
        for edge in self.__list:
            ans += str(edge)
        return ans

class GeometryGraph:

    def __init__(self, geometry_dict: dict):
        self.__geometry = dict(geometry_dict)

        self.__edgelist = GeometryEdgeList()
        
        indices = geometry_dict[INDEX_KEY_STRING]
        ps = geometry_dict[POSITION_KEY_STRING]

        def distance2(i, j):
            
            i3 = i * 3
            j3 = j * 3

            return pow(ps[i3] - ps[j3], 2) + pow(ps[i3 + 1] - ps[j3 + 1], 2) + pow(ps[i3 + 2] - ps[j3 + 2], 2)

        for i3 in range(0, len(indices), 3):
            face_i = int(i3 / 3)
            a, b, c = indices[i3], indices[i3 + 1], indices[i3 + 2]

            self.__edgelist.insert(a, b, i3, distance2(a, b))
            self.__edgelist.insert(b, c, i3 + 1, distance2(b, c))
            self.__edgelist.insert(c, a, i3 + 2, distance2(c, a))

        # print(str(self.__edgelist))
    def getVSize(self):
        return int(len(self.__geometry[POSITION_KEY_STRING]) / 3)

    def getEdges(self):
        return self.__edgelist.toList()

    def buildGeometryWithEdges(self, edge_idxs):
        ps0 = self.__geometry[POSITION_KEY_STRING]
        indices0 = self.__geometry[INDEX_KEY_STRING]

        builder = GeometryBuilder()

        v_size = self.getVSize()

        ps = []
        indices = []

        def buildRelate(frag_idx):
            
            face_idx = int(frag_idx / 3)
            edge_pos = frag_idx % 3

            A_id = indices0[face_idx * 3]
            B_id = indices0[face_idx * 3 + 1]
            C_id = indices0[face_idx * 3 + 2]

            A = fromArray(ps0, A_id)
            B = fromArray(ps0, B_id)
            C = fromArray(ps0, C_id)
            D = (A + B + C) / 3

            p = 0.4
            q = 1 - p

            A1 = D * p + A * q
            B1 = D * p + B * q
            C1 = D * p + C * q

            A1_id = v_size + face_idx * 3
            B1_id = v_size + face_idx * 3 + 1
            C1_id = v_size + face_idx * 3 + 2

            D_id = v_size + face_idx

            if (edge_pos == 0):
                A_i = builder.insertVertex(A, A_id)
                B_i = builder.insertVertex(B, B_id)
                A1_i = builder.insertVertex(A1, A1_id)
                B1_i = builder.insertVertex(B1, B1_id)

                builder.insertFace(A_i, B_i, A1_i, A, B, C)
                builder.insertFace(A1_i, B1_i, B_i, A, B, C)

            elif (edge_pos == 1):
                A_i = builder.insertVertex(B, B_id)
                B_i = builder.insertVertex(C, C_id)
                A1_i = builder.insertVertex(B1, B1_id)
                B1_i = builder.insertVertex(C1, C1_id)

                builder.insertFace(A_i, B_i, A1_i, A, B, C)
                builder.insertFace(A1_i, B1_i, B_i, A, B, C)

            elif (edge_pos == 2):
                A_i = builder.insertVertex(C, C_id)
                B_i = builder.insertVertex(A, A_id)
                A1_i = builder.insertVertex(C1, C1_id)
                B1_i = builder.insertVertex(A1, A1_id)

                builder.insertFace(A_i, B_i, A1_i, A, B, C)
                builder.insertFace(A1_i, B1_i, B_i, A, B, C)
            else:
                print("ERROR!")
            

        for edge_idx in edge_idxs:
            relate = self.__edgelist.getRelate(edge_idx)
            for r in relate:
                buildRelate(r)
            
        return builder.toGeoDict()
        
# Test
# position = [0, 1, 2, 3, 4, 5, 6, 7, 8]
# indices = [0, 1, 2]
# geo_dict = {POSITION_KEY_STRING: position, INDEX_KEY_STRING: indices}
# print(GeometryGraph(geo_dict).getEdges())
