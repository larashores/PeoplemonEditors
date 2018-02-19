from Editor.saveable.composite import Composite
from Editor.saveable.saveableArray import array
from Editor.saveable.saveableInt import saveable_int
from Editor.MoveAnimationEditor.saveables.DrawnImage import DrawnImage


class Frame(Composite):
    length = saveable_int('u32')
    images = array(DrawnImage)

    def __init__(self):
        Composite.__init__(self)
        self.length = 30
        self.last_selected = None
        self.half_transparent_images = []

    def pre_generate_images(self):
        for img in self.images:
            img.create_image()
            img.create_half_transparent()

    def draw(self, canvas):
        _ids = {}
        for ind, img in enumerate(self.images):
            img.level = ind
            _id = img.draw(canvas)
            _ids[_id] = img
        return _ids

    def pre_generate_half_transparent(self):
        for img in self.images:
            img.pre_generate_half_transparent()

    def draw_half_transparent(self, canvas):
        for img in self.images:
            img.draw_half_transparent(canvas)

    def copy(self):
        new = Frame()
        new.length = self.length
        for image in self.images:
            new.images.append(image.copy())
        if self.last_selected:
            new.last_selected = new.images[self.images.index(self.last_selected)]
        return new


