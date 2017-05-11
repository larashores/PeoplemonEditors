from Editor.saveable.composite import Composite
from Editor.saveable.saveableString import SaveableString
from Editor.saveable.saveableInt import saveable_int
from Editor.saveable.saveableArray import array
from Editor.MoveAnimationEditor.saveables.Frame import Frame
from Editor.MoveAnimationEditor.saveables.AnimImage import AnimImage


class AnimImageOld(Composite):
    name = SaveableString
    x = saveable_int('u32')
    y = saveable_int('u32')
    width = saveable_int('u32')
    height = saveable_int('u32')


class Animation(Composite):
    images = array(AnimImage)
    frames = array(Frame)

    def load_in_place(self, byte_array, pre_generate_images=False):
        Composite.load_in_place(self, byte_array)

        names_to_image = {}
        for anim_image in self.images:
            names_to_image[anim_image.name] = anim_image

        for frm in self.frames:
            for drawn in frm.images:
                drawn.set_image(names_to_image[drawn.name])
            if pre_generate_images:
                frm.pre_generate_images()


class AnimationOld(Composite):
    texture = SaveableString
    images = array(AnimImageOld)
    frames = array(Frame)



