import json
import numpy as np

from utils.mesh_util import GeometryGraph
from fun.kruskal_minimum_spanning_tree import KruskalMST
from fun.traversals import BFS, DFS

input_file_path = r"Data\Test1.json"
output_file_path = r"Data\Test1.out.json"
geometry = json.load(open(input_file_path, "r"))

geo_graph = GeometryGraph(geometry)
# print(len(geometry["indices"]) / 3, len(geo_graph.getEdges()))
print(geo_graph.getVSize())

# edge_idxs = KruskalMST(geo_graph.getVSize(), geo_graph.getEdges())
edge_idxs = DFS(geo_graph.getVSize(), geo_graph.getEdges())

json.dump(geo_graph.buildGeometryWithEdges(edge_idxs), open(output_file_path, "w"))
