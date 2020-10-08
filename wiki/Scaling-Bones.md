# [Scaling Bones](https://github.com/luvoid/COM3D2-All-Bout-Bones/blob/main/wiki/Scaling-Bones.md)
**If you are attaching new bones for clothing to the pelvis or spine,** you may run into an issue where **those bones don't don't scale properly** when you adjust the in-game body sliders (e.g. A cape does not resize with the torso, so you end up with a reasonably tall maid with a comically small cape.)

This is because the game copies certain bones so that it can scale it without distorting all of its descendants. This can be fixed however by manually copying the bone in question.

### Step 1: Make the \_SCL_ Bone
* Make a copy of the bone you want your custom bones to scale with. (`Ctrl D` in Blender)
* Parent the copy to the original without moving it. (`P` > "Keep Transforms")
* Rename the bone so that it has `_SCL_` appended to it.
* Move all the custom bones that were in the original that need to be scaled with into the copy

So if the bone in question was `Bip01 Pelvis`, it should now have an identical child with the name `Bip01 Pelvis_SCL_` with all the to-be-scaled bones inside of it.

### Step 2: Fix the vertex groups
You will have to rename the respective vertex group in the model's mesh so that it also has `_SCL_` appended to it.

### Step 3: Edit the bone data
Using the Blender-CM3D2-Converter plugin, edit the bone data of the model.
* In BoneData, find the original bone's name, and change the number after it from `1` to `0`
* Then, copy and paste the entire line so that there are two of them now.
* In the copied line, for the first name, append `_SCL_` so that it matches the name of the `_SCL_` bone.
* In the copied line, for the second name, change it to the name of the original bone.

> Before: 
> ```
> Bip01 Pelvis, 1, Bip01, 123456789...
> ```
> After: 
> ```
> Bip01 Pelvis, 0, Bip01, 123456789...
> Bip01 Pelvis_SCL_, 0, Bip01 Pelvis, 123456789...
> ```
* Repeat this for the LocalBoneData as well, except don't change any numbers this time.

> Before:
> ```
> Bip01 Pelvis, 1, 2, 3, 4, 5, 6...
> ```
> After: 
> ```
> Bip01 Pelvis, 1, 2, 3, 4, 5, 6...
> Bip01 Pelvis_SCL_, 1, 2, 3, 4, 5, 6...
> ```
* After that copy the bone data back into the armature/object or whatever your preferred bone data export method is, and you're done!
