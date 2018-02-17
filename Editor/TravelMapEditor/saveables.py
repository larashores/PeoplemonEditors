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