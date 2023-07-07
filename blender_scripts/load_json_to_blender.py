import json
import bpy
import bmesh
# Get the selected object
scene = bpy.context
selected_object = scene.active_object

new_name = "Custom_Object"

input_file_path = r"" # path

try:
    scene.object[new_name].free()
except:
    print("Remove failed")
    
new_mesh = bpy.data.meshes.new("Custom_Mesh")
obj = bpy.data.objects.new(new_name, new_mesh)
bm = bmesh.new()

geo_dict = json.load(open(input_file_path, 'r'))

ps = geo_dict["position"]
indices = geo_dict["indices"]

for i3 in range(0, len(ps), 3):
    u = ps[i3]
    v = ps[i3 + 1]
    w = ps[i3 + 2]
    bm.verts.new((u, v, w))

bm.verts.ensure_lookup_table()

for i3 in range(0, len(indices), 3):
    # print(dir(bm.verts))
    u = bm.verts[indices[i3]]
    v = bm.verts[indices[i3 + 1]]
    w = bm.verts[indices[i3 + 2]]
    bm.faces.new((u, v, w))

bm.to_mesh(new_mesh)
bm.free()

new_mesh.update()
scene.collection.objects.link(obj)
