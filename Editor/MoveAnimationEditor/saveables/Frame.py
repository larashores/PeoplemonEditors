from Editor.saveable.composite import Composite
from Editor.saveable.saveableArray import array
from Editor.saveable.saveableInt import saveable_int
from Editor.MoveAnimationEditor.saveables.DrawnImage import DrawnImage


class Frame(Composite):
    length = saveable_int('u32')
    images = array(DrawnImage)

    def __init__(self):
        Composite.__init__(self)
        length = 30

    def pre_generate_images(self):
        for img in self.images:
            img.create_image()

    def draw(self, canvas):
        _ids = {}
        for img in self.images:
            _id = img.draw(canvas)
            _ids[_id] = img
        return _ids

    def copy(self):
        new = Frame()
        new.length = self.length
        for image in self.images:
            new.images.append(image.copy())
        return new
