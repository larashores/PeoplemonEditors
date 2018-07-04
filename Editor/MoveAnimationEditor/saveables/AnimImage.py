from Editor.saveable.composite import Composite
from Editor.saveable.saveableString import SaveableString
from Editor.saveable.saveableImage import SaveableImage


class AnimImage(Composite):
    RETURN_GET = True
    name = SaveableString
    image = SaveableImage

    def __str__(self):
        return self.name
