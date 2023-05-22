import bpy
import numpy as np
import bmesh

# Copy zugztri class definition here

tri = ZugzTri(2)

# Get the selected object
scene = bpy.context
selected_object = scene.active_object

new_name = "Custom_Object"


try:
    scene.object[new_name].free()
except:
    print("Remove failed")
    
new_mesh = bpy.data.meshes.new("Custom_Mesh")
obj = bpy.data.objects.new(new_name, new_mesh)
bm = bmesh.new()

# Ensure the selected object is a mesh
if selected_object.type == 'MESH':
    
    obj.location = selected_object.location
    
    if selected_object.rotation_mode == 'QUATERNION':
        obj.rotation = selected_object.rotation_quaternion
    else:
        obj.rotation_euler = selected_object.rotation_euler
    
    
    # Get the mesh data
    mesh_data = selected_object.data

    # Copy materials
    for material in mesh_data.materials:
        new_mesh.materials.append(material.copy())
    
    # Ensure mesh data is in the correct form
    mesh_data.calc_loop_triangles()
    
    vert_num = 0
    # Iterate through the faces (triangles) of the mesh
    for face in mesh_data.loop_triangles:
        
        # Get the vertices of the face
        idxs = face.vertices
        
        temp = tri.Transform(mesh_data.vertices[idxs[0]].co, mesh_data.vertices[idxs[1]].co, mesh_data.vertices[idxs[2]].co)
        for i3 in range(0,len(temp), 3):
            
            v0 = bm.verts.new(temp[i3 + 0])
            v1 = bm.verts.new(temp[i3 + 1])
            v2 = bm.verts.new(temp[i3 + 2])
            bm.faces.new((v0, v1, v2))
            vert_num += 3

    bm.to_mesh(new_mesh)
    bm.free()

    for layer in mesh_data.uv_layers:
        new_mesh.uv_layers.new(name = layer.name)
    
    for layer in mesh_data.uv_layers:
        new_layer = new_mesh.uv_layers.get(layer.name)
        vert_num = 0

        # Iterate through the faces (triangles) of the mesh
        for face in mesh_data.loop_triangles:
            idxs = face.vertices

            # Get the uvs of the face
            temp = tri.Transform(layer.data[idxs[0]].uv, layer.data[idxs[1]].uv, layer.data[idxs[2]].uv)
            for i3 in range(0,len(temp), 3):

                new_layer.data[vert_num + 0].uv = temp[i3 + 0]
                new_layer.data[vert_num + 1].uv = temp[i3 + 1]
                new_layer.data[vert_num + 2].uv = temp[i3 + 2]
                
                vert_num += 3


    
    new_mesh.update()
    scene.collection.objects.link(obj)

else:
    print("The selected object is not a mesh.")