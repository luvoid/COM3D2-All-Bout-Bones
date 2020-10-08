# [Meido-ify a Character](https://github.com/luvoid/COM3D2-All-Bout-Bones/blob/main/wiki/Meidoify-a-Character.md)

**NOTE: I haven't really tested this in many scenarios yet, so you may have to manually create certain properties, bones, etc, for the script to work right**

This is a more **advance** technique. You need to be more familiar with CM3D2 modding and blender to follow this.

_It is highly recommended to make **unique** backups before running scripts, you never know when you'll want to go back to a specific step._

_Character_ refers the the non-CM3D2 model that you want to import, and _CM3D2 body_ is the imported stock CM3D2 body model. 

### Step 1: Import to Blender
* Get your choice of CM3D2 body model loaded in at 1.0 scale. (Beware [import issues](Exporting-Bones.md#roll-import-bug-may-only-apply-in-blender-28))
* Get you non-CM3D2 Character in the same scene, and make sure that it matches the 1 unit = 1 meter scale. (You may be able to look up the character's cannon height if you're not sure what it should be)

### Step 2: Setup the Armatures
* Select the CM3D2 Body model and run [`COM3D2 BoneMorph.py`](../scripts/COM3D2%20BoneMorph.py)
* It may complain about missing bones or properties, so try adding those manually.
* Try and pose the character so that it is similar to the "motorcycle" pose of the CM3D2 body, but not to much as this needs fine tuning later.

### Step 3: Sliders
* Under the custom properties of the CM3D2 body object, there should be properties that act identically to the body sliders in game. If not you may need to go back to step 2.
* Using **only the sliders** adjust the CM3D2 body to try and get the proportions to match your character's.
* Move and repose the character as needed to help it line up with the CM3D2 body.
* Repeat the previous two sub-steps until you are satisfied with the alignment.


### Step 4: Vertex Groups
* First, apply the armature-mesh-modifier all of the character's meshes (make a copy of the object first).
* Then, apply the current pose of the character as it's new rest pose.
* Repeat the previous sub-steps for the CM3D2 body, but also apply it's shapekeys (make a copy of the object first, it is needed later).
* Next the vertex groups need to be transferred from the CM3D2 body to the character. This can be done the old fashion way, or using CM3D2-Converter, or using [`COM3D2_Referenced_Vertex_Weight_Transfer.py`](../scripts/COM3D2_Referenced_Vertex_Weight_Transfer.py).
* Join (`Ctrl J`) the copy of the character into the CM3D2 body to become what will now be referred to as the _CM3D2 Character_. 
* Make sure to add new armature-mesh-modifiers into both of the new meshes.

### Step 5: Bones
* Move extra bones from the character's half of the CM3D2 character's armature to some appropriate bones in the CM3D2 body's half.
* Decide what bones you want to be scaled with [_SCL_ bones](Scaling-Bones.md) and follow their step 1 & 2 (but not step 3 yet).
* Sort out and rename your [dynamic bones](Dynamic-Bones.md) now, or else you'll need to come back to this step later if you need to change their hierarchy to be under a different _SCL_ bone.

### Step 6: Magic!
This step is going to make use of animations and poses, so you may wanna know how that works in blender. The goal is to invert all the transforms you made on the CM3D2 body earlier, and morph the character mesh with it, so that in the COM3D2 game, when you create a maid with the same settings, it has the same proportions as the original character.

(i.e. _character_ - (_body_ + _sliders_) = _character_ - _sliders_ - _body_ --> export model --> setting body and sliders in-game = (_character_ - _sliders_ - _body_) + (_sliders_ + _body_) = _character_. **TADA!**)
* Using the original CM3D2 body, make sure you are recording keyframes, then apply visual transform to pose.
* Save the current pose as a new NLA Strip named something like "Character Pose"
* Clear CM3D2 body's animation data (not the NLA track though) and then clear all user transforms. CM3D2 should now be back to its default state. You may need to disable the NLA track in the NLA editor.
* While CM3D2 body is in its default state, repeat sub-step 1 & 2, and name it something like "Default Pose".
* Create two new NLA Tracks under CM3D2 Character (you may want to make a copy first)
* Put the "Default Pose" NLA strip in the top NLA track, and set its blending mode to "add"
* Put the "Character Pose" NLA strip in the second NLA track directly under "Default Pose", and set it's mode to "Subtract"

If everything was done correctly, the character mesh should be morphed to fit the default posed CM3D2 body.

### Step 7: Cleanup
Now is the time to clean vertex groups and shape keys. If something was morphed in a strange way it's likely due to bad vertex weights. Vertex weights can be cleaned up by hand without having to reverse any steps.

### Step 8: Apply
* Apply the armature-mesh-modifier to the CM3D2 character mesh, and the rest pose to a copy of the CM3D2 armature. This is similar to steps 4.1-4.2.
* Add a new armature-mesh-modifier to the CM3D2 character mesh.
* Remove `_SCL_` from all the vertex groups (done easily with [`COM3D2_Cleanup_SCL_groups.py`](../scripts/COM3D2_Cleanup_SCL_groups.py)), except the ones you need to keep for your [Scaling Bones: Step 3](Scaling-Bones.md#step-3-edit-the-bone-data) which you should also do now. 
* Use BoneUtil to add any custom bones to the bone data.
* Fix any shapekeys as needed. Try and make a shapekey of CM3D2 Character for every non-zero shapekey in the CM3D2 Body first that shapes it to match the zeros of their respective CM3D2 body shapekeys, and then CM3D2 Converter's shapekey scaling tool to get a new shapekey where _newSk_ = _Sk_ * ((_bodySkMax_-_bodySkValue_)/_bodySkMax_ + 1) and update the basis so that _newBasis_ = _Basis_ - _Sk_

### Step 9: Export
Finally, just follow the normal procedures that you would for any other CM3D2 model. There are many tutorials you can find detailing this.
