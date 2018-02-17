from Editor.saveable.composite import Composite
from Editor.saveable.saveableInt import saveable_int
from Editor.saveable.saveableArray import array
from Editor.saveable.saveableString import SaveableString
from Editor.saveable.union import Union


class ImageType(SaveableString):
    pass

    def __str__(self):
        return 'Image ({},{}): "' + self.get() + '"'


class TextType(Composite):
    text = SaveableString
    red = saveable_int('u8')
    green = saveable_int('u8')
    blue = saveable_int('u8')
    size = saveable_int('u16')

    def __str__(self):
        return 'Text ({},{}): "' + self.text.get() + '"'


class CreditType(Union):
    image = ImageType
    text = TextType


class Credit(Composite):
    x = saveable_int('u8')
    y_buf = saveable_int('u16')
    type = CreditType

    def __str__(self):
        return str(self.type).format(self.x, self.y_buf)