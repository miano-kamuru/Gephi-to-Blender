import json
import bpy
import math
import mathutils

file=open("C:/Users/MIANO/Desktop/json_svg/networkRender/network.json","r")
networkData = json.load(file)
file.close()

node_dict = {}
for i in networkData["nodes"]:
    x=i['attributes']['x']/100
    y=i['attributes']['y']/100
    size=i['attributes']['size']/100
    node_dict[i['key']]={'key':i['key'],'x':x,'y':y}
    bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(x,y,0),scale=(1, 1, 1))
    bpy.ops.transform.resize(value=(size, size, size), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
    bpy.context.active_object.name=i['key'] #name plane object
    material = bpy.data.materials['circleMaterial']  #get material
    bpy.context.object.data.materials.append(material)  #assign material

count=0
for i in networkData['edges']:
    source_node=bpy.data.objects.get(node_dict[i['source']]['key']) #get source node 
    target_node=bpy.data.objects.get(node_dict[i['target']]['key']) #get target node
    position1 = source_node.matrix_world.translation #source node vector
    position2 = target_node.matrix_world.translation #target node vector
    edge_length=math.dist(position1,position2)/2 #calculate edge length
    edge_thickness=0.05
    midpoint = (position1  + position2) 
    direction = position2 - position1

    bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(0,0,0),scale=(1, 1, 1)) #create plane
    bpy.ops.transform.resize(value=(edge_length, edge_thickness, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
    bpy.context.active_object.location=midpoint/2
    bpy.context.active_object.rotation_euler = direction.to_track_quat('X', 'Y').to_euler()
    angle = direction.to_2d().angle_signed(mathutils.Vector((1, 0)))  # Angle relative to the X-axis
    bpy.context.active_object.rotation_euler = (0, 0, angle)  # Only rotate around Z-axis
    bpy.context.active_object.name="edge_{}".format(count)
    material = bpy.data.materials['circleMaterial']  #get material
    bpy.context.object.data.materials.append(material)  #assign material
    count+=1
    
