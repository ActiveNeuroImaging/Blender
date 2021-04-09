import nibabel as nb
import numpy as np
 
# cifti code based on Christopher J Markiewicz https://nbviewer.jupyter.org/github/neurohackademy/nh2020-curriculum/blob/master/we-nibabel-markiewicz/NiBabel.ipynb

cifti = nb.load('/Users/robleech/Dropbox/HCP_S900_GroupAvg_v1/S900.MyelinMap_BC_MSMAll.32k_fs_LR.dscalar.nii')
cifti_data = cifti.get_fdata(dtype=np.float32)
cifti_hdr = cifti.header
nifti_hdr = cifti.nifti_header

axes = [cifti_hdr.get_axis(i) for i in range(cifti.ndim)]

def surf_data_from_cifti(data, axis, surf_name): 
    assert isinstance(axis, nb.cifti2.BrainModelAxis)
    for name, data_indices, model in axis.iter_structures():  # Iterates over volumetric and surface structures
        if name == surf_name:                                 # Just looking for a surface
            data = data.T[data_indices]                       # Assume brainmodels axis is last, move it to front
            vtx_indices = model.vertex                        # Generally 1-N, except medial wall vertices
            surf_data = np.zeros((vtx_indices.max() + 1,) + data.shape[1:], dtype=data.dtype)
            surf_data[vtx_indices] = data
            return surf_data
    raise ValueError(f"No structure named {surf_name}")

left_brain=surf_data_from_cifti(cifti_data, axes[1], 'CIFTI_STRUCTURE_CORTEX_LEFT')

gifti_img_3KBaseBrain = nb.load('/Users/robleech/Dropbox/HCP_S900_GroupAvg_v1/S900.L.pial_MSMAll.32k_fs_LR.surf.gii')
gifti_img_3KBaseBrain.darrays[0].data.shape
import bpy
import bmesh
vertices = gifti_img_3KBaseBrain.darrays[0].data
faces = gifti_img_3KBaseBrain.darrays[1].data

#new_mesh = bpy.data.meshes.new('new_mesh')
me = bpy.data.meshes.new("name") 
me.from_pydata(vertices,[],faces.tolist())
me.update()

new_object = bpy.data.objects.new('brain', me)


#new_collection = bpy.data.collections.new('new_collection')
#bpy.context.scene.collection.children.link(new_collection)
# add object to scene collection
bpy.data.collections[0].objects.link(new_object)
colorData=left_brain[:]
colorData[colorData!=0]=colorData[colorData!=0]-colorData[colorData!=0].min()
C=colorData/colorData.max()





if not me.vertex_colors:
    me.vertex_colors.new()

color_layer = me.vertex_colors["Col"]

#i = 0



for face in me.polygons:
    for idx in face.loop_indices:
        loop = me.loops[idx]
        #print(idx)
        v=loop.vertex_index
        r, g, b = [C[v], C[v], C[v]]
        color_layer.data[idx].color = (r, g, b, 1.0)
              




