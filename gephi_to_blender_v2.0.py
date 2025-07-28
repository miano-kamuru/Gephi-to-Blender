import json
import bpy
import math
import mathutils

file=open("C:/Users/MIANO/Desktop/json_svg/networkRender/network.json","r")
networkData = json.load(file)
file.close()

colors = []
for i in networkData["nodes"]: #get node colors
    if i["attributes"]['color'] not in colors:
        colors.append(i["attributes"]['color'])
        
for i in colors: #create collections based on node colors
    bpy.context.scene.collection.children.link(bpy.data.collections.new("group_{}".format(i)))
        
    
node_dict = {}

for i in networkData["nodes"]:
    x=i['attributes']['x']/100
    y=i['attributes']['y']/100
    size=i['attributes']['size']/100
    node_dict[i['key']]={'key':i['key'],'x':x,'y':y}
    bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(x,y,0),scale=(1, 1, 1))
    bpy.ops.transform.resize(value=(size, size, size), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
    bpy.context.active_object.name="node_{}".format(i['key']) #name plane object
    material = bpy.data.materials['circleMaterial']  #get material
    bpy.context.object.data.materials.append(material)  #assign material

   
count=0
for i in networkData['edges']:
    source_node=bpy.data.objects.get("node_{}".format(node_dict[i['source']]['key'])) #get source node 
    target_node=bpy.data.objects.get("node_{}".format(node_dict[i['target']]['key'])) #get target node
    position1 = source_node.matrix_world.translation #source node vector
    position2 = target_node.matrix_world.translation #target node vector
    edge_length=math.dist(position1,position2)/2 #calculate edge length
    edge_thickness=0.05
    midpoint = (position1  + position2) / 2
    direction = position2 - position1
    z_component=-0.005
    bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(0,0,0),scale=(1, 1, 1)) #create plane
    bpy.ops.transform.resize(value=(edge_length, edge_thickness, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
    bpy.context.active_object.location=(midpoint.x,midpoint.y,z_component) #position edges
    bpy.context.active_object.rotation_euler = direction.to_track_quat('X', 'Y').to_euler()
    angle = direction.to_2d().angle_signed(mathutils.Vector((1, 0)))  # Angle relative to the X-axis
    bpy.context.active_object.rotation_euler = (0, 0, angle)  # Only rotate around Z-axis
    bpy.context.active_object.name="edge_{}".format(i['key'])
    material = bpy.data.materials['circleMaterial']  #get material
    bpy.context.object.data.materials.append(material)  #assign material
    count+=1
    
def add_object_to_existing_collection(object_name, collection_name):
    """
    Adds an object to an existing collection in Blender.
    
    :param object_name: The name of the object to be added.
    :param collection_name: The name of the collection to which the object should be added.
    """
    # Get the object
    obj = bpy.data.objects.get(object_name)
    
    # Get the collection
    collection = bpy.data.collections.get(collection_name)
    
    
    # Unlink the object from all current collections (optional)
    for coll in obj.users_collection:
        coll.objects.unlink(obj)
    
    # Add the object to the specified collection
    collection.objects.link(obj)
    
for i in networkData["nodes"]: #add nodes to collection
    add_object_to_existing_collection("node_{}".format(i['key']),"group_{}".format(i["attributes"]['color']))

for i in networkData["edges"]: #add edges to collection
    for k in networkData["nodes"]:
        if i['source']==k['key']:
           add_object_to_existing_collection('edge_{}'.format(i['key']),"group_{}".format(k["attributes"]['color']))    
