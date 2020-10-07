import bpy

SORT_GROUPS = False # sorting is very slow
VERTEX_MAPPING = 'POLYINTERP_NEAREST' # https://docs.blender.org/api/current/bpy.types.DataTransferModifier.html?highlight=vert_mapping#bpy.types.DataTransferModifier.vert_mapping
UPDATE_EXISTING = False # Potentially unstable as it is dependent entierly on the names of the modifiers.


TO_OBJECT = bpy.context.active_object
FROM_OBJECT = bpy.context.selected_editable_objects[0] if bpy.context.selected_editable_objects[0] != TO_OBJECT else bpy.context.selected_editable_objects[1] 

REFERENCE_LIST = {
	'Bip01 Pelvis_SCL_'  : 'Bip01 Pelvis_SCL_',
	'Bip01 Spine1_SCL_'  : 'Bip01 Spine1_SCL_',
	'Bip01 Spine1a_SCL_' : 'Bip01 Spine1a_SCL_',
	'Bip01 Neck_SCL_'    : 'Bip01 Neck_SCL_',
	'Bip01 ? Clavicle'   : 'Bip01 ? Clavicle',
	'Bip01 ? UpperArm'   : 'Bip01 ? UpperArm',
	'Uppertwist_?'       : 'Uppertwist_?',
	'Foretwist_?'        : 'Foretwist_?',
	'Bip01 ? Hand'       : 'Bip01 ? Hand',
	'Hip_?'              : 'Hip_?',
	'momotwist_?'        : 'momotwist_?',
	'Bip01 ? Calf_SCL_'  : 'Bip01 ? Calf_SCL_',
	
	'Bip01 ? Foot'       : 'Bip01 ? Foot',
	'Bip01 ? Toe1'       : 'Bip01 ? Toe1',
	'TW_leg_?'           : 'Bip01 ? Calf_SCL_',
	
	
}

# FOR TRANSFER LIST
# Name each set after the reference group in the destination mesh
# Put the names of each vertex group to transfer under
#    each refrence group it overlaps with (in order of similarity)
TRANSFER_LIST = {
	'Bip01 Pelvis_SCL_'  : [
		'Bip01 Pelvis_SCL_',
		'Bip01 Spine_SCL_',
		'Bip01 Spine0a_SCL_',
		'Hip_?',
		'Bip01 Spine1_SCL_',
		'momoniku_?',
		'Bip01 Spine1a_SCL_',
		'momotwist_?',
	],
	'Bip01 Spine1_SCL_'  : [
		'Bip01 Spine1_SCL_',
		'Bip01 Spine1a_SCL_',
		'Bip01 Spine_SCL_',
		'Bip01 Pelvis_SCL_',
	],
	'Bip01 Spine1a_SCL_' : [
		'Mune_?_sub',
		'Bip01 Spine1a_SCL_',
		'Bip01 Spine1_SCL_',
		'Bip01 Neck_SCL_',
		'Bip01 ? Clavicle'
		'Kata_?',
		'Bip01 Spine0a_SCL_',
		'Uppertwist_?',
	],
	'Bip01 Neck_SCL_'    : [
		'Bip01 Neck_SCL_',
		'Bip01 Head',
		'Bip01 ? Clavicle',
	],
	'Bip01 ? Clavicle'   : [
		'Bip01 ? Clavicle',
		'Kata_?',
		'Bip01 Spine1a_SCL_',
		'Uppertwist_?',
	],
	'Bip01 ? UpperArm'   : [
		'Bip01 ? UpperArm',
		'Uppertwist1_?',
		'Uppertwist_?',
		'Bip01 ? Clavicle',
		'Bip01 ? Forearm',
		'Bip01 Spine1a_SCL_',
		'Kata_?',
	],
	'Uppertwist_?'       : [
		'Uppertwist_?',
		'Uppertwist1_?',
		'Bip01 ? UpperArm',
		'Bip01 ? Clavicle',
		'Kata_?',
		'Bip01 Spine1a_SCL_',
	],
	'Foretwist_?'        : [
		'Foretwist_?',
		'Foretwist1_?',
		'Bip01 ? Forearm',
		'Bip01 ? UpperArm',
	],
	'Bip01 ? Hand'       : [
		'Bip01 ? Hand',
	],
	'Hip_?'              : [
		'Hip_?',
		'Bip01 Pelvis_SCL_',
		'momoniku_?',
		'momotwist_?',
		'Bip01 Spine_SCL_',
	],
	'momotwist_?'        : [
		'Bip01 ? Thigh_SCL_',
		'momoniku_?',
		'momotwist2_?',
		'momotwist_?',
		'Hip_?',
		'Bip01 Pelvis_SCL_',
		'Bip01 ? Calf_SCL_',
		'Bip01 Spine_SCL_',
		'Bip01 Spine0a_SCL_',
	],
	'Bip01 ? Calf_SCL_'  : [
		'Bip01 ? Calf_SCL_',
		'Bip01 ? Foot',
		'momotwist_?',
		'momoniku_?',
		'momotwist2_?',
	],
	
	'Bip01 ? Foot'       : [
		'Bip01 ? Foot',
		'Bip01 ? Calf_SCL_',
	],
	'TW_leg_?'           : [
		'Bip01 ? Foot',
		'Bip01 ? Calf_SCL_',
	],
}












def cpu_breathe(): # Update UI to make script feel less freezy
	# This method is considered unsafe, script should use modal operators instead.
	# But I'm lazy
	bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)


def SetActiveObject(object):
	if bpy.context.object == object:
		# skip setting active object 'cause takes a long time
		return
	
	a, b, c = bpy.app.version
	if a > 2 or b >= 80:  # if blender 2.80 or higher
		bpy.context.view_layer.objects.active = object
	else:
		bpy.context.scene.objects.active = object
		
		
def InsertTag(str, tag):
	newStr = str + "." + tag
	if ".L" in str:
		newStr = str.replace(".L", "."+tag+".L")
	elif ".R" in str:
		newStr = str.replace(".R", "."+tag+".R")
	return newStr


def GetGroup(list, name, flip=False, checkTag=None, requireTag=False):
	side = "R" if flip else "L"
	if checkTag:
		group = list.get(name.replace("?",side)+"."+checkTag) or list.get(name.replace("?","*")+"."+checkTag+"."+side)
		if group:
			return group
	if requireTag:
		return
	group = list.get(name.replace("?",side)) or list.get(name.replace("?","*")+"."+side)
	return group


def MakeGroup(object, name, index=None):
	newGroup = object.vertex_groups.new(name=name)
	name = newGroup.name

	#object.vertex_groups.active_index = newGroup.index
	#cpu_breathe()
	
	if index and SORT_GROUPS:
		SetActiveObject(object)
		object.vertex_groups.active_index = newGroup.index
		while newGroup.index > index:
			bpy.ops.object.vertex_group_move()  # this operator is really slow!
			#cpu_breathe()
	
	return newGroup



def MakeModifier(object, name='', type='VERTEX_WEIGHT_MIX', aboveArmature=True, useExisting=False):
	if useExisting:
		newModifier = object.modifiers.get(name)
		if newModifier:
			return newModifier
	
	newModifier = object.modifiers.new(name, type)
	name = newModifier.name
	newModifier.show_expanded = False
	
	if aboveArmature and object.modifiers.find('Armature') >= 0:
		SetActiveObject(object)
		while object.modifiers.find('Armature') < object.modifiers.find(newModifier.name):
			bpy.ops.object.modifier_move_up(modifier=name) # this operator is really slow!
			#cpu_breathe()
	
	return newModifier



def RefTransfer(src, ref, dst, mode='ADD', mask=True, srcObject=FROM_OBJECT, dstObject=TO_OBJECT, mapping=VERTEX_MAPPING, clear=False, flip=False):
	side = "R" if flip else "L"
	
	srcGroups = srcObject.vertex_groups
	dstGroups = dstObject.vertex_groups
	
	# check if source group has already been transfered from source mesh
	srcGroup = GetGroup(dstGroups, src, flip=flip, checkTag='src', requireTag=True)
	refGroup = GetGroup(dstGroups, ref, flip=flip, checkTag='ref') if ref else None
	dstGroup = GetGroup(dstGroups, dst, flip=flip)
	
	if ref and not refGroup:
		print('Could not find reference group "'+ref+'"')
		# if this is ever changed to not return, note that this ref group's abscence is ignored in the fixDependencies function
		return
	
	if dstObject == srcObject and not srcGroup:
		if not ref:
			srcGroup = GetGroup(srcGroups, src, flip=flip, checkTag='ref', requireTag = True)
		else:
			srcGroup = GetGroup(srcGroups, src, flip=flip)
		if not srcGroup:
			print('Could not find group "'+src+'" to use as source in destination object')
			return
	
	if not dstGroup:
		print('Creating destination group "'+dst+'"')
		dstGroup = MakeGroup(dstObject, dst.replace("?",side), index=refGroup and refGroup.index+1 or srcGroup.index+1)
		clear = False # no need to clear if it was just created
		
	if refGroup == dstGroup: # sholdn't happen because of fixDependencies but check anyways
		print('WARNING: refGroup == dstGroup; There may be dependency errors for reference group "'+refGroup.name+'"')
		newName = refGroup.name
		refGroup.name = InsertTag(refGroup.name,"ref")
		dstGroup = MakeGroup(dstObject, newName, index=refGroup.index+1)
	elif clear:
		newName = dstGroup.name
		dstGroup.name = InsertTag(dstGroup.name,"old")
		dstGroup = MakeGroup(dstObject, newName, index=refGroup and refGroup.index+1 or srcGroup.index+1)
		
	if not srcGroup: # transfer group from source mesh to target mesh
		srcGroup = GetGroup(srcGroups, src, flip=flip)
		if not srcGroup:
			print('Could not find source group "'+src+'"')
			return
		
		srcGroups.active_index = srcGroup.index
		
		newGroup = MakeGroup(dstObject, InsertTag(srcGroup.name,"src"), index=dstGroup.index)
		
		transferMod = MakeModifier(dstObject, type='DATA_TRANSFER', name="Trans "+srcGroup.name)
		transferMod.object = srcObject
		transferMod.data_types_verts = {'VGROUP_WEIGHTS'}
		transferMod.use_vert_data = True
		transferMod.layers_vgroup_select_src = srcGroup.name
		transferMod.layers_vgroup_select_dst = newGroup.name
		transferMod.vert_mapping = mapping
		
		dstGroups.active_index = newGroup.index
		cpu_breathe()
		
		srcGroup = newGroup
		
		#bpy.ops.object.data_transfer(use_reverse_transfer=False, use_freeze=False, data_type='', use_create=True, vert_mapping='NEAREST', edge_mapping='NEAREST', loop_mapping='NEAREST_POLYNOR', poly_mapping='NEAREST', use_auto_transform=False, use_object_transform=True, use_max_distance=False, max_distance=1.0, ray_radius=0.0, islands_precision=0.1, layers_select_src='ACTIVE', layers_select_dst='ACTIVE', mix_mode='REPLACE', mix_factor=1.0)
		#bpy.ops.object.data_transfer(use_reverse_transfer=True, data_type='VGROUP_WEIGHTS', vert_mapping='NEAREST')
	
	if mode == 'NONE':
		return
	
	# just some name cases
	symbol = "?"
	if mode == 'REPLACE':
		symbol = "="
	elif mode == 'ABOVE_THRESHOLD':
		symbol = ">"
	elif mode == 'BELOW_THRESHOLD':
		symbol = "<"
	elif mode == 'MIX':
		symbol = "%"
	elif mode == 'ADD':
		symbol = "+"
	elif mode == 'SUB':
		symbol = "-"
	elif mode == 'MUL':
		symbol = "*"
	
	refName = '' if not mask or not refGroup else refGroup.name
	modName = dstGroup.name[-20:]+symbol+"="+srcGroup.name[-20:]
	modName = modName+"*"+refName[-20:] if not refName == '' else modName
	
	# Now make the modifier
	mod = MakeModifier(dstObject, name=modName, useExisting=True)
	mod.vertex_group_a = dstGroup.name
	mod.vertex_group_b = srcGroup.name
	mod.mix_mode = mode
	mod.mix_set = 'ALL' if not (mode == 'MUL' or mode == 'SUB') else 'AND'
	mod.mask_vertex_group = refName
	
	dstGroups.active_index = dstGroup.index
	cpu_breathe()
	
	if not flip and ( src.find('?') or ref.find('?') or dst.find('?') ):
		RefTransfer(src, ref, dst, mode=mode, srcObject=srcObject, dstObject=dstObject, mapping=mapping, clear=clear, flip=True)
	
	return



def fixDependencies(name, flip=False):
	group = GetGroup(TO_OBJECT.vertex_groups, name, flip=flip, checkTag='ref', requireTag=True)
	if not group:
		group = GetGroup(TO_OBJECT.vertex_groups, name, flip=flip)
		if group:	
			group.name = InsertTag(group.name,"ref")
		#else: 
			# ignore if not found, assume it will never be created or needed
	
	if not flip and name.find('?'):
		fixDependencies(name, flip=True)
	
	return












def main():
    '''region Manual_RefTransfer'''
    # If you feel confident about what you are doing you can edit this region to call RefTransfer directly
    if False:
        TO_OBJECT   = TO_OBJECT
        FROM_OBJECT = FROM_OBJECT
    
        RefTransfer("Foretwist_?",         "Elbow_Mask",    "Bip01 ? Forearm",    mode='ADD')
        RefTransfer("Foretwist_?",         "Elbow_Mask",    "Foretwist_?",        mode='SUB')
        RefTransfer("Bip01 ? UpperArm",    "Arm_Band",      "Uppertwist1_?",      mode='ADD')
        RefTransfer("Bip01 ? UpperArm",    "Arm_Band",      "Bip01 ? UpperArm",   mode='SUB')
        RefTransfer("Bip01 ? UpperArm",    "Shoulder_Arms", "Uppertwist_?",       mode='ADD')
        RefTransfer("Bip01 ? UpperArm",    "Shoulder_Arms", "Bip01 ? UpperArm",   mode='SUB')
        RefTransfer("Uppertwist_?",        "Arm_Band",      "Uppertwist1_?",      mode='ADD')
        RefTransfer("Uppertwist_?",        "Arm_Band",      "Uppertwist_?",       mode='SUB')
        RefTransfer("Mune_?_sub",          "Chest_Plate",   "Bip01 Spine1a_SCL_", mode='ADD')
        RefTransfer("Mune_?_sub",          "Chest_Plate",   "Mune_?_sub",         mode='SUB')
        #RefTransfer("Bip01 Spine1a_SCL_", "Acc_Mune",      "DJ_mune_01",         mode='ADD')
        #RefTransfer("Bip01 Spine1a_SCL_", "Acc_Mune",      "Bip01 Spine1a_SCL_", mode='SUB')
        
        print("MANUAL DONE")
        return # skip automatic RefTransfers
    '''endregion Manual_RefTransfer'''
	
	bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
	
	clearList = {}
	for dst in REFERENCE_LIST:
		clearList[dst] = False
	
	# First fix dependencies
	for ref, src in REFERENCE_LIST.items():
		if REFERENCE_LIST.get(src):
			fixDependencies(ref)
		if TRANSFER_LIST.get(src):
			fixDependencies(ref)
	for ref, sources in TRANSFER_LIST.items():
		for src in sources:
			if REFERENCE_LIST.get(src):
				fixDependencies(ref)
			if TRANSFER_LIST.get(src):
				fixDependencies(ref)
	
	# Then do reference list
	for ref, dst in REFERENCE_LIST.items():
		RefTransfer(ref, None, dst, srcObject=TO_OBJECT, clear=not clearList[dst])
		clearList[dst] = True
	
	# Then do transfer list
	REFERENCE_LIST_values = REFERENCE_LIST.values()
	if True:
		for ref, sources in TRANSFER_LIST.items():
			for src in sources:
				if not src in REFERENCE_LIST_values:
					RefTransfer(src, ref, src)
					subref = REFERENCE_LIST.get(ref)
					if subref:
						RefTransfer(src, ref, subref, srcObject=TO_OBJECT, mode='SUB', mask=False)
	
	print("DONE")
			

if __name__ == "__main__":
	main()


