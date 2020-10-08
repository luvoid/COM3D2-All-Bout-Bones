import bpy

# Select the Object you want to remove _SCL_ vertex groups from then run this script. 


def main():
	obj = bpy.context.object
	if not obj:
		return
	
	vgroups = obj.vertex_groups
	
	for v in vgroups:
		if v:
			v.name = v.name.replace("_SCL_","")
	
	return


if __name__ == "__main__":
	main()
