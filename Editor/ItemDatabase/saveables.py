from Editor.saveable.composite import Composite
from Editor.saveable.saveableInt import U16, U32
from Editor.saveable.saveableString import SaveableString


class Item(Composite):
    id = U16
    name = SaveableString
    description = SaveableString
    price = U32

    def __str__(self):
        return 'ID: {} | Name: {} | Desc: {}'.format(self.id.get(), self.name.get(), self.description.get())
