from Editor.saveable.composite import Composite
from Editor.saveable.saveableInt import saveable_int
from Editor.saveable.saveableArray import array
from Editor.saveable.saveableString import SaveableString


class Location(Composite):
    x = saveable_int('u16')
    y = saveable_int('u16')
    display_name = SaveableString
    reference_name = SaveableString
    map_name = SaveableString
    spawn_id = saveable_int('u16')

    def __str__(self):
        return 'Spawn ID: {}, Display Name: {}, Reference Name: {}, Map Name: {}'.  \
              format(self.spawn_id.get(), self.display_name.get(), self.reference_name.get(), self.map_name.get())