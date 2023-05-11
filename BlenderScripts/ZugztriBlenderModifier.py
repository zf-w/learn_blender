import bpy
import numpy as np
import bmesh

def ZugzTriTemplate(N = 3):

    templateList = []

    def AddFace(A, B, C):
        nonlocal templateList
        templateList += [A[0], A[1], B[0], B[1], C[0], C[1]]

    def Vect2DirectRatioPoint(A, B, r = 1 / 3):
        A = np.array(A)
        B = np.array(B)
        AB = B - A

        return AB * r + A

    def Vect2MidPoint(A, B):
        A = np.array(A)
        B = np.array(B)
        
        return (A + B) / 2

    def helper(n, A, B, C):
        
        A = np.array(A)
        B = np.array(B)
        C = np.array(C)


        unitHalfRatio = 0.5 / (pow(2, n) - 1)

        ABcenter = Vect2MidPoint(A, B)
        BCcenter = Vect2MidPoint(B, C)
        CAcenter = Vect2MidPoint(C, A)

        ab = (B - A) * unitHalfRatio
        bc = (C - B) * unitHalfRatio
        ca = (A - C) * unitHalfRatio

        AB0 = ABcenter - ab
        AB1 = ABcenter + ab
        BC0 = BCcenter - bc
        BC1 = BCcenter + bc
        CA0 = CAcenter - ca
        CA1 = CAcenter + ca

        linkRatio = unitHalfRatio

        ab0 = Vect2DirectRatioPoint(AB0, CA1, linkRatio)
        ab1 = Vect2DirectRatioPoint(AB1, BC0, linkRatio)
        bc0 = Vect2DirectRatioPoint(BC0, AB1, linkRatio)
        bc1 = Vect2DirectRatioPoint(BC1, CA0, linkRatio)

        if (n == 1):
            AddFace(A, B, C)
            return
        
        helper(n - 1, A, CA1, AB0)
        AddFace(AB1, ab0, AB0)
        AddFace(ab1, AB1, ab0)
        helper(n - 1, AB1, B, BC0)
        AddFace(bc0, BC0, BC1)
        AddFace(bc1, BC1, bc0)
        helper(n - 1, BC1, CA0, C)
    
    A = np.array([1,0])
    B = np.array([0,0])
    C = np.array([0,1])

    helper(N, A, B, C)

    return templateList


class ZugzTri:

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

    def __init__(self, N):
        self.__template = ZugzTriTemplate(N)

    def Transform(self, A, B, C):
        print(type(A))
        BA = A - B
        BC = C - B

        to_return = []
        
        normal0 = ZugzTri.CaluculateNormal(A, B, C)

        for i6 in range(0, len(self.__template), 6):
            A1 = B + BA * self.__template[i6 + 0] + BC * self.__template[i6 + 1]
            B1 = B + BA * self.__template[i6 + 2] + BC * self.__template[i6 + 3]
            C1 = B + BA * self.__template[i6 + 4] + BC * self.__template[i6 + 5]

            if (ZugzTri.IsCounterClockwise(A1, B1, C1, normal0)):
                temp = B1
                B1 = C1
                C1 = temp

            to_return.append(A1)
            to_return.append(B1)
            to_return.append(C1)
        
        return to_return


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