import bpy
import bmesh
import os
from random import uniform
from mathutils import Vector


def ImportModel(path):
    print(path)
    bpy.ops.import_scene.obj(filepath=path+'\GT.obj')
    #bpy.ops.object.mode_set(mode='OBJECT')

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            obj.select_set(True)
    # Join selected objects
            bpy.context.view_layer.objects.active = obj
    bpy.ops.object.join()    
    bpy.context.selected_objects[0].name = "GT"
    #bpy.context.selected_objects[0].hide_render = not bpy.context.selected_objects[0].hide_render

def PointCloudGen(obj,AimPointCloudCount):
    
    Bx = obj.dimensions.x
    By = obj.dimensions.y
    Bz = obj.dimensions.z
    #print(Bx)
    #print(By)
    #print(Bz)
    #print(Bx*By*Bz)
    
    #
    
    distribute_points_node.inputs["Density"].default_value = tempDensity
    #return
    #Ratio
    FirstRatio = AimPointCloudCount/GetModifierPointCount(obj)
    print(GetModifierPointCount(obj))
    ##
    tempDensity = (int)(tempDensity*FirstRatio)
    smallDensity = 0
    bigDensity = (int)(tempDensity*1.5)
    print(tempDensity)
    count = 0
    while abs(GetModifierPointCount(obj)-AimPointCloudCount) > 1000:
        count = count+1
        print("Step: "+str(count))
        print("Density: "+str(tempDensity))
        print("PointCloud Count: "+str(GetModifierPointCount(obj)))
        #too much
        if GetModifierPointCount(obj) > AimPointCloudCount:
            bigDensity = tempDensity
        else:
            smallDensity = tempDensity
        tempDensity = (bigDensity+smallDensity)/2
        if abs(bigDensity-smallDensity)<1:
            break
        distribute_points_node.inputs["Density"].default_value = tempDensity
        #print(tempDensity)
        bpy.context.view_layer.update()
        
    print("Final Density: "+str(tempDensity))
    print("Final PointCloud Count: "+str(GetModifierPointCount(obj)))
    #bpy.ops.object.select_all(action='DESELECT')
    #obj.select_set(True)
    #bpy.ops.object.modilfier_apply(modifier="GeometryNodes")

def ExportModel(obj,Path):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    if not os.path.isdir(Path):
        os.mkdir(Path)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    bm = bmesh.new()
    bm.from_object( obj, depsgraph )
    bm.verts.ensure_lookup_table()
    # Extract vertex coordinates and color values
    verts = [v.co for v in bm.verts]
    # 導出為 PLY 檔案l
    with open(Path+"PolyFit.ply", "w") as f:
    # Write the header
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write("element vertex "+str(len(verts))+"\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("end_header\n") 
        # Write the vertex data
        for v in verts:
            f.write(" ".join(str(x) for x in v) + "\n")
    #Close the file
    f.close()
        
def main():
    ###
    MainPath = r'D:\PaperEvaluation\Other\\'
    LoadModelStart = 1
    LoadModelEnd = 29
    model_names= ['GT']
    ###    
    ##import model
    for NumberName in range(LoadModelStart,LoadModelEnd):
        ImportModel(MainPath+"M"+'{:02d}'.format(NumberName)+"\\GT\\")
        ##point cloud genderater
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH' and obj.name in model_names:
                #
                PointCloudGen(obj,400000)
                #
                ExportModel(obj,MainPath+"M"+'{:02d}'.format(NumberName)+"\\PolyFit\\")
                bpy.ops.object.delete()
                break
    
if __name__ == '__main__':
    main()