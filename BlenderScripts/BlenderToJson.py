import bpy
import numpy as np
import bmesh
import json

# Get the selected object
scene = bpy.context
selected_object = scene.active_object

output_file_path = r"D:\3.Projects\1.py-create-3D\Data\Test"



if selected_object.type == 'MESH':
     # Get the mesh data
    mesh_data = selected_object.data
    # Ensure mesh data is in the correct form
    mesh_data.calc_loop_triangles()

    json_dict = {}
    position_array = []
    indices = []
    json_dict["position"] = position_array
    json_dict["indices"] = indices

    vert_num = len(mesh_data.vertices)

    for i in range(vert_num):
        curr_vert = mesh_data.vertices[i]
        position_array.append(curr_vert.co[0])
        position_array.append(curr_vert.co[1])
        position_array.append(curr_vert.co[2])

    for face in mesh_data.loop_triangles:
        idxs = face.vertices
        indices.append(idxs[0])
        indices.append(idxs[1])
        indices.append(idxs[2])

    json.dump(json_dict, open(f"{output_file_path}.json", 'w'))

    

