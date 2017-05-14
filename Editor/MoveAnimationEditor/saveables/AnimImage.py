from Editor.saveable.composite import Composite
from Editor.saveable.saveableString import SaveableString
from Editor.saveable.saveableImage import SaveableImage


class AnimImage(Composite):
    name = SaveableString
    image = SaveableImage

