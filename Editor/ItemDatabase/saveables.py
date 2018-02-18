from Editor.saveable.composite import Composite
from Editor.saveable.saveableInt import saveable_int
from Editor.saveable.saveableArray import array
from Editor.saveable.saveableString import SaveableString


class Item(Composite):
    id = saveable_int('u16')
    name = SaveableString
    description = SaveableString
    price = saveable_int('u32')

    def __str__(self):
        return 'ID: {} | Name: {} | Desc: {}'.format(self.id.get(), self.name.get(), self.description.get())
