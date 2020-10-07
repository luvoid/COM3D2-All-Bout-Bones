
# ****** ALWAYS MAKE A BACK-UP! ****** #

# ****** ALWAYS MAKE A BACK-UP! ****** #

# ****** ALWAYS MAKE A BACK-UP! ****** #


import bpy

# --------------------- #
# ------ OPTIONS ------ #
# --------------------- #
FIX_THIGH = True # The default shape of the thigh is the shape the thigh takes when it is standing.
                    # but the pose used is the motor-cycle pose, therefore, when the body is imported
                    # into the game, the thigh is changed to make the underside curve more naturally.
                    # If this is set to True, the pose angle of the momoniku bone will be changed to 
                    # match how it will look when in the motor-cycle pose in-game.
                    # * This is similar to "preserve volume" but only for the underside of the thigh.

ONLY_FIX_SETTINGS = False # only fix the custom property sliders, creating them if they do not exist
RESET_SETTINGS = False    # if fixing sliders and this is set to true, the sliders will be set to their default values





# --------------------- #
# ------- STUFF ------- #
# --------------------- #
class WideSlider_Props(bpy.types.PropertyGroup): 
	# was going to use this to make a special property category, but decided that was to much work
	THIPOS:     bpy.props.FloatVectorProperty(name="Property0")
	THI2POS:    bpy.props.FloatVectorProperty(name="Property1")
	HIPPOS:     bpy.props.FloatVectorProperty(name="Property2")
	MTWPOS:     bpy.props.FloatVectorProperty(name="Property3")
	MMNPOS:     bpy.props.FloatVectorProperty(name="Property4")
	SKTPOS:     bpy.props.FloatVectorProperty(name="Property5")
	SPIPOS:     bpy.props.FloatVectorProperty(name="Property6")
	S0APOS:     bpy.props.FloatVectorProperty(name="Property7")
	S1POS:      bpy.props.FloatVectorProperty(name="Property8")
	S1APOS:     bpy.props.FloatVectorProperty(name="Property9")
	NECKPOS:    bpy.props.FloatVectorProperty(name="PropertyA")
	CLVPOS:     bpy.props.FloatVectorProperty(name="PropertyB")
	MUNESUBPOS: bpy.props.FloatVectorProperty(name="PropertyC")
	MUNEPOS:    bpy.props.FloatVectorProperty(name="PropertyD")
	THIPOS:     bpy.props.FloatVectorProperty(name="PropertyE")
	THI2POS:    bpy.props.FloatVectorProperty(name="PropertyF")
	
	
	
	

def magnitude(v):
	return sqrt(pow(v[0],2)+pow(v[0],2)+pow(v[0],2))

# Add variable defined in this script into the drivers namespace.
bpy.app.driver_namespace["magnitude"] = magnitude






# --------------------- #
# ------ SLIDERS ------ #
# --------------------- #
def BoneMorph_GetArmature(override=None):
	override = override or bpy.context.copy()
	armature = override['object']
	if not armature or armature.type != 'ARMATURE':
		print("ERROR: Active object is not an armature")
		return None, None
	
	for area in bpy.context.screen.areas:
		#print(area,area.type)
		if area.type == 'OUTLINER':
			override.update({
				'blend_data': None,
				'area': area,
				'scene': bpy.context.scene,
				'screen': None,
				'space_data': area.spaces[0],
				'window': None,
				'window_manager': None,
				'object': armature,
				'active_object': armature,
				'edit_object': armature,
			})
			break
	
	if override['area'].type != 'OUTLINER':
		print("ERROR: There is no 3D View Present in the current workspace")
		return None, None
	
	if False:
		print("\n")
		for k,v in override.items():
			print(k)
		print("\n")
	return armature, override



def BoneMorph_GetPoseBone(boneName, flip=False, override=None):
	override = override or bpy.context.copy()
	side = "R" if flip else "L"
	armature, override = BoneMorph_GetArmature(override=override)
	if not armature:
		return
	
	poseBoneList = armature.pose.bones
	poseBone = poseBoneList.get(boneName.replace("?",side)) or poseBoneList.get(boneName.replace("?","*")+"."+side)
	
	# check if _SCL_ bone needs to be created
	if not poseBone and "_SCL_" in boneName:
		boneList = armature.data.edit_bones
		bpy.ops.object.mode_set(mode='EDIT')
		print("Make Scale Bone: "+boneName)
		copyBone = boneList.get(boneName.replace("_SCL_","").replace("?",side)) or boneList.get(boneName.replace("_SCL_","").replace("?","*")+"."+side)
		if copyBone:
			bpy.ops.armature.select_all(action='DESELECT')
			for v in bpy.context.selected_bones:
				v.select = False
				v.select_head = False
				v.select_tail = False
			copyBone.select = True
			copyBone.select_head = True
			copyBone.select_tail = True
			boneList.active = copyBone
			bpy.ops.armature.duplicate()
			bone = bpy.context.selected_bones[0]
			bone.name = bone.basename+"_SCL_" + ("."+side if ("."+side) in bone.name else "")
			boneList.active = copyBone
			bpy.ops.armature.parent_set(type='OFFSET')
			
			# rename vertex groups
			for child in armature.children:
				if child.type == 'MESH':
					vertexGroup = child.vertex_groups.get(copyBone.name)
					if vertexGroup:
						vertexGroup.name = bone.name
	
	poseBone = poseBoneList.get(boneName.replace("?",side)) or poseBoneList.get(boneName.replace("?","*")+"."+side)
	
	if not poseBone:
		print("WARNING: Could not find bone \""+boneName+"\"")
		return
	
	bpy.ops.object.mode_set(mode='POSE')
	return poseBone






def BoneMorph_AddPositionDriver(prop, bone, drivers, axis, value, default=50):
	value = value-1
	if value == 0:
		return
	
	driver = drivers[axis] or bone.driver_add("location",axis).driver
	prefix = " + "
	
	# if just created
	if not driver.use_self:
		driver.type = 'SCRIPTED'
		driver.use_self = True
		if axis == 1: # if y axis, include parent bone's length, because head coords are based on parent's tail
			driver.expression = "(self.parent.bone.length+self.bone.head[%d])_" % axis
		else:
			driver.expression = "self.bone.head[%d]_" % axis
		prefix = " * ("
	
	# if prop isn't already a factor
	if not prop in driver.expression:
		driver.expression = driver.expression[:-1] + prefix + ("(self.id_data['%s']-%g)*%g)" % (prop, default, value/(100-default) ))
		
	return


def BoneMorph_AddScaleDriver(prop, bone, drivers, axis, value, default=50):
	value = value-1
	if value == 0:
		return
	
	driver = drivers[axis] or bone.driver_add("scale",axis).driver
	
	# if just created
	if not driver.use_self:
		driver.type = 'SCRIPTED'
		driver.use_self = True
		driver.expression = "(1)"
	
	# if prop isn't already a factor
	if not prop in driver.expression:
		driver.expression = driver.expression[:-1] + (" + (self.id_data['%s']-%g)*%g)" % (prop, default, value/(100-default) ))
			
	return


def BoneMorph_GetDrivers(data_path, property, object=bpy.context.object):
	drivers = [None, None, None]
	if object and object.animation_data:
		for f in object.animation_data.drivers:
			fName = f.data_path
			#print("check",fName, "for", '["%s"].%s' % (data_path, property))
			if '["%s"].%s' % (data_path, property) in fName:
				#print("VALID!")
				drivers[f.array_index] = f.driver
	return drivers





def BoneMorph_SetPosition(prop, boneName, y, x, z, default=50):
	# Check if object has this property
	if not bpy.context.object.get(prop) or ONLY_FIX_SETTINGS:
		if ONLY_FIX_SETTINGS:
			return
		
	#x = (1-x)+1
	#y = (1-y)+1
	#z = (1-z)+1
		
	bone = BoneMorph_GetPoseBone(boneName)
	if bone:
		bone.bone.use_local_location = False
		drivers = BoneMorph_GetDrivers(bone.name,'location')
		
		BoneMorph_AddPositionDriver(prop, bone, drivers, 0, x, default=default)
		BoneMorph_AddPositionDriver(prop, bone, drivers, 1, y, default=default)
		BoneMorph_AddPositionDriver(prop, bone, drivers, 2, z, default=default)
	
	# repeat for left side
	if '?' in boneName:
		bone = BoneMorph_GetPoseBone(boneName, flip=True)
		if bone:
			bone.bone.use_local_location = False
			drivers = BoneMorph_GetDrivers(bone.name,'location')
			
			BoneMorph_AddPositionDriver(prop, bone, drivers, 0, x, default=default)
			BoneMorph_AddPositionDriver(prop, bone, drivers, 1, y, default=default)
			BoneMorph_AddPositionDriver(prop, bone, drivers, 2, (1-z)+1, default=default) # mirror z axis
	
	return



def BoneMorph_SetScale(prop, boneName, y, x, z, default=50):
	# Check if object has this property
	if not bpy.context.object.get(prop) or ONLY_FIX_SETTINGS:
		if ONLY_FIX_SETTINGS:
			return
	
	bone = BoneMorph_GetPoseBone(boneName)
	if bone:
		drivers = BoneMorph_GetDrivers(bone.name,'scale')
		
		BoneMorph_AddScaleDriver(prop, bone, drivers, 0, x, default=default)
		BoneMorph_AddScaleDriver(prop, bone, drivers, 1, y, default=default)
		BoneMorph_AddScaleDriver(prop, bone, drivers, 2, z, default=default)
	
	# repeat for left side
	if '?' in boneName:
		bone = BoneMorph_GetPoseBone(boneName, flip=True)
		if bone:
			drivers = BoneMorph_GetDrivers(bone.name,'scale')
			
			BoneMorph_AddScaleDriver(prop, bone, drivers, 0, x, default=default)
			BoneMorph_AddScaleDriver(prop, bone, drivers, 1, y, default=default)
			BoneMorph_AddScaleDriver(prop, bone, drivers, 2, z, default=default)
	
	return






# --------------------- #
# --- WIDER SLIDERS --- #
# --------------------- #
def WideSlider_AddPositionDriver(prop, index, bone, drivers, axis, value):
	if value == 0:
		return
	
	driver = drivers[axis] or bone.driver_add("location",axis).driver
	
	# if just created
	if not driver.use_self:
		driver.type = 'SCRIPTED'
		driver.use_self = True
		driver.expression = "0"
	
	# if prop isn't already a factor
	if not prop in driver.expression:
		driver.expression = driver.expression + (" + self.id_data['%s'][%d]*%g" % (prop,index,value))
			
	return


def WideSlider_AddScaleDriver(prop, index, bone, drivers, axis):
	if index < 0:
		return
	
	driver = drivers[axis] or bone.driver_add("scale",axis).driver
	
	# if just created
	if not driver.use_self:
		driver.type = 'SCRIPTED'
		driver.use_self = True
		driver.expression = "1"
	
	# if prop isn't already a factor
	if not prop in driver.expression:
		driver.expression = driver.expression + (" * self.id_data['%s'][%d]" % (prop,index))
			
	return



def WideSlider_AddVectorProperty(object, prop, value=None, default=0.0, min=-100, max=200):
	value = value or [default, default, default]
	object[prop] = not RESET_SETTINGS and object.get(prop) or value
	object['_RNA_UI'][prop] = {
		"description": "",
		"default": default,
		"min": min,
		"max": max,
		"soft_min": min,
		"soft_max": max,
	}
	return






def WideSlider_SetPosition(prop, boneName, uy, ux, uz, axisOrder=[0,1,2], axisFlip=None):
	prop = "~"+prop   # to separate these from normal sliders 
	
	# Check if object has this property
	if not bpy.context.object.get(prop) or ONLY_FIX_SETTINGS:
		WideSlider_AddVectorProperty(bpy.context.object, prop)
		if ONLY_FIX_SETTINGS:
			return
	
	bone = BoneMorph_GetPoseBone(boneName)
	if bone:
		bone.bone.use_local_location = False
		drivers = BoneMorph_GetDrivers(bone.name,'location')
	
		WideSlider_AddPositionDriver(prop, axisOrder[1], bone, drivers, 0, -ux)
		WideSlider_AddPositionDriver(prop, axisOrder[0], bone, drivers, 1, -uy)
		WideSlider_AddPositionDriver(prop, axisOrder[2], bone, drivers, 2, -uz)
	
	# repeat for left side
	if '?' in boneName:
		bone = BoneMorph_GetPoseBone(boneName, flip=True)
		if bone:
			bone.bone.use_local_location = False
			drivers = BoneMorph_GetDrivers(bone.name,'location')
			
			if axisFlip == 0:
				uy = -uy
			elif axisFlip == 1:
				ux = -ux
			elif axisFlip == 2:
				uz = -uz
			
			WideSlider_AddPositionDriver(prop, axisOrder[1], bone, drivers, 0, -ux)
			WideSlider_AddPositionDriver(prop, axisOrder[0], bone, drivers, 1, -uy)
			WideSlider_AddPositionDriver(prop, axisOrder[2], bone, drivers, 2, -uz)
	
	return


def WideSlider_SetScale(prop, boneName, axisOrder=[0,1,2]):
	prop = "~"+prop  # to separate these from normal sliders
	
	# Check if object has this property
	if not bpy.context.object.get(prop) or ONLY_FIX_SETTINGS:
		WideSlider_AddVectorProperty(bpy.context.object, prop, default=1.0, min=0.1, max=3.0)
		if ONLY_FIX_SETTINGS:
			return
	
	bone = BoneMorph_GetPoseBone(boneName)
	if bone:
		drivers = BoneMorph_GetDrivers(bone.name,'scale')
		
		WideSlider_AddScaleDriver(prop, axisOrder[1], bone, drivers, 0)
		WideSlider_AddScaleDriver(prop, axisOrder[2], bone, drivers, 1)
		WideSlider_AddScaleDriver(prop, axisOrder[0], bone, drivers, 2)
	
	# repeat for left side
	if '?' in boneName:
		bone = BoneMorph_GetPoseBone(boneName, True)
		if bone:
			drivers = BoneMorph_GetDrivers(bone.name,'scale')

			WideSlider_AddScaleDriver(prop, axisOrder[1], bone, drivers, 0)
			WideSlider_AddScaleDriver(prop, axisOrder[2], bone, drivers, 1)
			WideSlider_AddScaleDriver(prop, axisOrder[0], bone, drivers, 2)
	
	return






# -------------------- #
# ------- MAIN ------- #
# -------------------- #
def main():
	i=0
	while i<20:
		print()
		i=i+1
		
		
	bpy.utils.register_class(WideSlider_Props)
	
	
	BoneMorph_SetPosition("KubiScl", "Bip01 Neck",         1.05, 1, 1);
	BoneMorph_SetPosition("KubiScl", "Bip01 Head",          1.2, 1, 1);

	BoneMorph_SetScale(   "UdeScl", "Bip01 ? UpperArm",    1.15, 1, 1);

	BoneMorph_SetScale(   "HeadX", "Bip01 Head",            1, 1.1, 1.2);
	BoneMorph_SetScale(   "HeadY", "Bip01 Head",          1.2, 1.1,   1);

	BoneMorph_SetPosition("sintyou", "Bip01 Spine",           1, 1, 1.15);
	BoneMorph_SetPosition("sintyou", "Bip01 Spine0a",      1.12, 1, 1);
	BoneMorph_SetPosition("sintyou", "Bip01 Spine1",       1.12, 1, 1);
	BoneMorph_SetPosition("sintyou", "Bip01 Spine1a",      1.12, 1, 1);
	BoneMorph_SetPosition("sintyou", "Bip01 Neck",         1.03, 1, 1);
	BoneMorph_SetPosition("sintyou", "Bip01 Head",          1.1, 1, 1);
	BoneMorph_SetPosition("sintyou", "Bip01 ? Calf",       1.13, 1, 1);
	BoneMorph_SetPosition("sintyou", "Bip01 ? Foot",       1.13, 1, 1);
	BoneMorph_SetScale(   "sintyou", "Bip01 ? UpperArm",    1.1, 1, 1);
	BoneMorph_SetScale(   "sintyou", "Bip01 ? Thigh_SCL_", 1.13, 1, 1);
	BoneMorph_SetScale(   "sintyou", "momotwist_?",        1.13, 1, 1);
	BoneMorph_SetScale(   "sintyou", "Bip01 ? Calf_SCL_",  1.13, 1, 1);
	
	# for DouPer, any bone not a thigh or a decendant of one, it's values are inverted
	BoneMorph_SetPosition("DouPer", "Bip01 Spine",               1, 1, (1-1.06)+1);
	BoneMorph_SetPosition("DouPer", "Bip01 Spine0a",    (1-1.12)+1, 1, 1);
	BoneMorph_SetPosition("DouPer", "Bip01 Spine1",     (1-1.12)+1, 1, 1);
	BoneMorph_SetPosition("DouPer", "Bip01 Spine1a",    (1-1.12)+1, 1, 1);
	BoneMorph_SetPosition("DouPer", "Bip01 Neck",       (1-0.97)+1, 1, 1);
	BoneMorph_SetScale(   "DouPer", "Bip01 ? UpperArm", (1-1.02)+1, 1, 1);
	BoneMorph_SetPosition("DouPer", "Bip01 ? Calf",           1.13, 1, 1);
	BoneMorph_SetPosition("DouPer", "Bip01 ? Foot",           1.13, 1, 1);
	BoneMorph_SetScale(   "DouPer", "Bip01 ? Thigh_SCL_",     1.13, 1, 1);
	BoneMorph_SetScale(   "DouPer", "momotwist_?",            1.13, 1, 1);
	BoneMorph_SetScale(   "DouPer", "Bip01 ? Calf_SCL_",      1.13, 1, 1);

	BoneMorph_SetScale(   "koshi", "Bip01 Pelvis_SCL_",  1,  1.2, 1.08);
	BoneMorph_SetScale(   "koshi", "Bip01 Spine_SCL_",   1,    1,    1);
	BoneMorph_SetScale(   "koshi", "Hip_?",              1, 1.04,  1.1);
	BoneMorph_SetScale(   "koshi", "Skirt",              1,  1.2, 1.12);
	
	#BoneMorph_SetPosition("kata", "Bip01 ? Clavicle",    1.02, 1, 1.5, default=0);
	BoneMorph_SetPosition("kata", "Bip01 ? Clavicle",   1.02, 1, 1.15, default=0);
	BoneMorph_SetScale(   "kata", "Bip01 Spine1a_SCL_",    1, 1, 1.05, default=0);

	BoneMorph_SetScale(   "west", "Bip01 Spine_SCL_",   1, 1.05,  1.1);
	BoneMorph_SetScale(   "west", "Bip01 Spine0a_SCL_", 1, 1.15,  1.3);
	BoneMorph_SetScale(   "west", "Bip01 Spine1_SCL_",  1,  1.1, 1.15);
	BoneMorph_SetScale(   "west", "Bip01 Spine1a_SCL_", 1, 1.05, 1.05);
	BoneMorph_SetScale(   "west", "Skirt",              1, 1.08, 1.12);
	
	
	
	# WideSlider functions MUST be called AFTER all BoneMorph calls
	WideSlider_SetPosition("THIPOS",  "Bip01 ? Thigh",           0, 1/1000, 1/1000, axisFlip=2, axisOrder=[1, 2, 0])
	WideSlider_SetPosition("THI2POS", "Bip01 ? Thigh_SCL_", 1/1000, 1/1000, 1/1000, axisFlip=2, axisOrder=[1, 2, 0])
	WideSlider_SetPosition("HIPPOS",  "Hip_?",              1/1000, 1/1000, 1/1000, axisFlip=2, axisOrder=[1, 2, 0])
	WideSlider_SetPosition("MTWPOS",  "momotwist_?",          1/10,   1/10,  -1/10, axisFlip=2                     )
	WideSlider_SetPosition("MMNPOS",  "momoniku_?",           1/10,   1/10,  -1/10, axisFlip=1                     )
	WideSlider_SetPosition("SKTPOS",  "Skirt",               -1/10,  -1/10,   1/10,             axisOrder=[2, 1, 0])
	WideSlider_SetPosition("SPIPOS",  "Bip01 Spine",         -1/10,   1/10,   1/10                                 )
	WideSlider_SetPosition("S0APOS",  "Bip01 Spine0a",       -1/10,   1/10,   1/10                                 )
	WideSlider_SetPosition("S1POS",   "Bip01 Spine1",        -1/10,   1/10,   1/10                                 )
	WideSlider_SetPosition("S1APOS",  "Bip01 Spine1a",       -1/10,   1/10,   1/10                                 )
	WideSlider_SetPosition("NECKPOS", "Bip01 Neck",          -1/10,   1/10,   1/10                                 )
	WideSlider_SetPosition("CLVPOS",  "Bip01 ? Clavicle",    -1/10,   1/10,  -1/10, axisFlip=2                     )
	WideSlider_SetPosition("MUNESUBPOS", "Mune_?_sub",       -1/10,  -1/10,  -1/10, axisFlip=1, axisOrder=[1, 2, 0])
	WideSlider_SetPosition("MUNEPOS", "Mune_?",               1/10,  -1/10,  -1/10, axisFlip=2, axisOrder=[1, 2, 0])

	WideSlider_SetScale("THISCL",     "Bip01 ? Thigh"     , axisOrder=[0,1,-1])
	WideSlider_SetScale("MTWSCL",     "momotwist_?"       )
	WideSlider_SetScale("MMNSCL",     "momoniku_?"        )
	WideSlider_SetScale("PELSCL",     "Bip01 Pelvis_SCL_" )
	WideSlider_SetScale("THISCL2",    "Bip01 ? Thigh_SCL_")
	WideSlider_SetScale("CALFSCL",    "Bip01 ? Calf"      )
	WideSlider_SetScale("FOOTSCL",    "Bip01 ? Foot"      )
	WideSlider_SetScale("SKTSCL",     "Skirt"             )
	WideSlider_SetScale("SPISCL",     "Bip01 Spine_SCL_"  )
	WideSlider_SetScale("S0ASCL",     "Bip01 Spine0a_SCL_")
	WideSlider_SetScale("S1_SCL",     "Bip01 Spine1_SCL_" )
	WideSlider_SetScale("S1ASCL",     "Bip01 Spine1a_SCL_")
	WideSlider_SetScale("S1ABASESCL", "Bip01 Spine1a"     )
	WideSlider_SetScale("KATASCL",    "Kata_?"            )
	WideSlider_SetScale("UPARMSCL",   "Bip01 ? UpperArm"  )
	WideSlider_SetScale("FARMSCL",    "Bip01 ? Forearm"   )
	WideSlider_SetScale("HANDSCL",    "Bip01 ? Hand"      )
	WideSlider_SetScale("CLVSCL",     "Bip01 ? Clavicle"  )
	WideSlider_SetScale("MUNESCL",    "Mune_?"            )
	WideSlider_SetScale("MUNESUBSCL", "Mune_?_sub"        )
	WideSlider_SetScale("NECKSCL",    "Bip01 Neck_SCL_"   )
	WideSlider_SetScale("HIPSCL",     "Hip_?"             )
	WideSlider_SetScale("PELSCL",     "Hip_?"             ) # hips are also scaled with pelvis
	
	if FIX_THIGH:
		bone = BoneMorph_GetPoseBone("momoniku_?")
		bone.rotation_quaternion[0] = 0.997714
		bone.rotation_quaternion[3] = -0.06758
		bone = BoneMorph_GetPoseBone("momoniku_?", flip=True)
		bone.rotation_quaternion[0] = 0.997714
		bone.rotation_quaternion[3] = 0.06758
	
	return

	

if __name__ == "__main__":
	main()
