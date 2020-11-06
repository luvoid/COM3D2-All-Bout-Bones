# [Exporting Bones](https://github.com/luvoid/COM3D2-All-Bout-Bones/blob/main/wiki/Exporting-Bones.md)
Maybe I'll add more here, but for now here are the plugins' tutorials.

### [Converter BoneData (Japanese)](https://github.com/trzr/Blender-CM3D2-Converter#%E3%83%9C%E3%83%BC%E3%83%B3)

### [BoneUtil BoneDataImport (Japanese)](https://github.com/trzr/Blender-CM3D2-BoneUtil/wiki/BoneDataImport)

## Vertex Groups
The names of vertex groups must match the case-sensitive name of an exported local bone for that vertex group to be exported from blender. If there is a vertex with no weight in any exported vertex groups, then Blender-CM3D2-Converter will throw an error.

### Deleted Bones
Just like how a vertex group must match a local bone to be exported from blender, likewise a local bone must match a vertex group to be loaded by the game. **If there are no vertices assigned to a local bone via a vertex group, the game will immediately delete that bone.**

### Vertex Group Limitations
A .model file will assign a vertex to exactly four vertex groups. It cannot store more than four. If there are less than four it will just assing the remaining others to null. (e.g. if the vertex is only assigned to one vertex group, it will store the other three as null.) **This means you can only assign a vertex to 4 exported vertex groups.**


## Roll Import Bug (_May only apply in Blender 2.8+_)
Be aware that Blender-CM3D2-Converter will give the blender bones an incorrect roll, so if you then use BoneUtil to update the BoneData of imported bones, using the blender bones, or simply export using the armature, your model may load into COM3D2 with twisted limbs. The improper roll values on the blender bones will also affect scripts like `COM3D2_BoneMorph.py`.
