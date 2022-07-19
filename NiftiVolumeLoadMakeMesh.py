import colorsys
import numpy as np
import bpy
import bmesh
import numpy as np
from mathutils import Matrix, Euler, Vector
import nibabel as nb


nii = nb.load('/usr/local/fsl/data/standard/MNI152_T1_2mm_brain.nii.gz')

data=nii.get_fdata()

nii = nb.load('/Users/robleech/Downloads/PH_RSFC_DIfference.nii')
dataFunc=nii.get_fdata()


vals=[]
FuncVals=[]
vals3=[]


for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        for k in range(data.shape[2]):
            if data[i,j,k]>0:
                vals.append(data[i,j,k])
                FuncVals.append(dataFunc[i,j,k])
                vals3.append([i,j,k])
     

context = bpy.context
scene = context.scene
scale = 0.05


me = bpy.data.meshes.new('pc')



bm = bmesh.new()
bm.from_mesh(me)
for x, y, z in vals3:
    co = scale * Vector((x, y, z))
    v = bm.verts.new(co)
 

bm.to_mesh(me)
ob = bpy.data.objects.new('pc', me)
scene.collection.objects.link(ob)

a_mesh = ob.data

bm = bmesh.new()
bm.from_mesh(a_mesh)
StructuralIntensityAttribute = bm.verts.layers.float.new("StructuralIntensityAttribute")
FunctionalIntensityAttribute = bm.verts.layers.float.new("FunctionalIntensityAttribute")

count=0
for vert in bm.verts:
   
    vert[StructuralIntensityAttribute] =vals[count] 
    vert[FunctionalIntensityAttribute] =FuncVals[count] 
    count=count+1

#bm.to_mesh(a_mesh)


bm.to_mesh(a_mesh)
bm.free() 

#source = np.zeros((len(a_mesh.vertices) * 1,), dtype=np.float32)
#a_mesh.vertices.foreach_get('IntensityAttribute', source )







