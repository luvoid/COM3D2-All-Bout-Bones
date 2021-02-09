# [Dynamic Bones](https://github.com/luvoid/COM3D2-All-Bout-Bones/blob/main/wiki/Dynamic-Bones.md)
Dynamic bones are bones in COM3D2 that have simulated physics (commonly used for skirts and hair)

If you are trying to add movement that is not necessarily dependent on gravity or physics (like wings or tails), then you may want to use an animated model instead.

## Types of Dynamic Bones
There are primarily 2 types of dynamic bones: yure bones and skirt bones.
* **Skirt** bones are used for, well, skirts (and sometimes things like sword sheaths on the hip.)
* **Yure** bones are used for almost everything else, including hair, scarfs, jewelry, etc.


### Yure Bones
Yure bones contain `_yure_` somewhere in the name of their bone, and their physics are described by a .phy file, and it's colliders by a .col file.

If there is a file with the same name as the model that the yure bone is in, then that will be used as the yure bone's .phy/.col file. (e.g. `MyModel.model` will load and use `MyModel.phy` if it exists, and if so then also `MyModel.col` if it also exists.)

If there case above is not met, then some default file will be loaded.

### Skirt Bones
Skirt bones contain `Skirt` somewhere in their name, and their physics are described by a .psk file that is selected following the same rules as yure bones.

There must be between 12-24 "branches" of skirt bones, otherwise there will be an error. The first skirt bone, or "root," in each branch must include  `_A_` in its name, and its consecutive descendants would have `_B_`, `_C_`, etc. The 12-24 "roots" can have varying and even no descendants.

## Organization / Discrepancies
**All _children_ (with a `_yure_` / `_yure_` *descendant*) of the *first yure bone's __parent__* will become dynamic bones.** If there are multiple yure branches, you can make sure they all become dynamic by adding a "dummy" yure bone to their first common ancestor. Keep in mind, all children of that ancestor with `_yure_` descendants will become dynamic though. This means that you cannot put bracelets with dangling jewels on each wrist. Either only one will become dynamic, or if you put a "dummy" yure bone in the top spine bone, then the arms will flop around too, (the neck however will not flop because it has no `_yure_` descendants).
 
**If there are both skirt and yure bones in the same model, then only the skirt bone can be customized,** and `default_yure.phy` will always be loaded for the yure bones. **Also in this case, the rule the regarding the first yure bone and its parent's descendants does not apply.** Instead, only yure bones, their decendants, and the skirt bones will become dynamic. This means that the bracelet jewelry example above would work if you added a "dummy" skirt armature, however you would not be able to customize the physics of the jewelry, and would be stuck with the default physics.



