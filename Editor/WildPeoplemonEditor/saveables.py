from Editor.saveable.composite import Composite
from Editor.saveable.saveableInt import saveable_int
from Editor.saveable.saveableArray import array
from Editor.saveable.saveableString import SaveableString


class Override(Composite):
    code = SaveableString
    override = saveable_int('u16')


class WildPeoplemon(Composite):
    id = saveable_int('u16')
    min_lvl = saveable_int('u16')
    max_lvl = saveable_int('u16')
    rarity = saveable_int('u16')
    overrides = array(Override)
