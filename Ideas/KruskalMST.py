from Ideas.DisjointSet import DisjointSet

def KruskalMST(n, edge_list):
    dj = DisjointSet(n)
    edge_list = sorted(edge_list, reverse=True)
    
    ans = []

    for edge in edge_list:
        weight, u, v, face_i = edge
        if (not dj.same(u, v)):
            dj.union(u, v)
            ans.append(face_i)

    return ans