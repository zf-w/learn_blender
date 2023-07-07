import numpy as np 

def BuildAdjList(n, edge_list):
    adj_list = [[] for i in range(n)]
    for edge_idx in range(len(edge_list)):
        edge = edge_list[edge_idx]
        # print(edge)
        u = edge[1]
        v = edge[2]
        adj_list[u].append((v, edge_idx))
        adj_list[v].append((u, edge_idx))
    return tuple(adj_list)


def BFS(n, edge_list):
    edge_idxs = []

    adj_list = BuildAdjList(n, edge_list)
    
    visited = np.zeros((n), dtype=bool)

    

    for i in range(n):
        if (visited[i] == True):
            continue
        queue = [i]
        visited[i] = True
        while (len(queue) > 0):
            curr = queue.pop(0)
            for next_info in adj_list[curr]:
                # print(next_info)
                next_idx = next_info[0]
                edge_idx = next_info[1]
                if (visited[next_idx] != True):
                    visited[next_idx] = True
                    edge_idxs.append(edge_idx)
                    queue.append(next_idx)
    print(len(edge_idxs))

    return edge_idxs

def DFS(n, edge_list):
    edge_idxs = []

    adj_list = BuildAdjList(n, edge_list)
    
    visited = np.zeros((n), dtype=bool)

    for i in range(n):
        if (visited[i] == True):
            continue
        stack = [(i, -1)]
        # visited[i] = True
        while (len(stack) > 0):
            curr, edge_idx = stack.pop(len(stack) - 1)
            if (visited[curr]):
                continue
            else:
                if (edge_idx >= 0):
                    edge_idxs.append(edge_idx)
                visited[curr] = True

            for next_info in adj_list[curr]:
                # print(next_info)
                stack.append(next_info)

    print(len(edge_idxs))

    return edge_idxs