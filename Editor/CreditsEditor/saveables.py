from Editor.saveable.composite import Composite
from Editor.saveable.saveableInt import U8, U16
from Editor.saveable.saveableString import SaveableString
from Editor.saveable.union import Union


class ImageType(SaveableString):
    pass

    def __str__(self):
        return 'Image ({},{}): "' + self.get() + '"'


class TextType(Composite):
    text = SaveableString
    red = U8
    green = U8
    blue = U8
    size = U16

    def __str__(self):
        return 'Text ({},{}): "' + self.text.get() + '"'


class CreditType(Union):
    image = ImageType
    text = TextType


class Credit(Composite):
    x = U8
    y_buf = U16
    type = CreditType

    def __str__(self):
        return str(self.type).format(self.x, self.y_buf)
