# [Exporting Bones](https://github.com/luvoid/COM3D2-All-Bout-Bones/blob/main/wiki/Exporting-Bones.md)
Maybe I'll add more here, but for now here are the plugins' tutorials.

### [Converter BoneData (Japanese)](https://github.com/trzr/Blender-CM3D2-Converter#%E3%83%9C%E3%83%BC%E3%83%B3)

### [BoneUtil BoneDataImport (Japanese)](https://github.com/trzr/Blender-CM3D2-BoneUtil/wiki/BoneDataImport)

### Roll Import Bug (_May only apply in Blender 2.8+_)

Be aware that Blender-CM3D2-Converter will give the blender bones an incorrect roll, so if you then use BoneUtil to update the BoneData of imported bones, using the blender bones, or simply export using the armature, your model may load into COM3D2 with twisted limbs. The improper roll values on the blender bones will also affect scripts like `COM3D2_BoneMorph.py`.
