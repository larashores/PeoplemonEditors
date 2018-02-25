from Editor.saveable.composite import Composite
from Editor.saveable.saveableInt import saveable_int
from Editor.saveable.saveableArray import array
from Editor.saveable.saveableString import SaveableString


class Override(Composite):
    code = SaveableString
    override = saveable_int('u16')

    def __str__(self):
        return 'Code: {}, Value: {}'.format(self.code.get(), self.override.get())


class WildPeoplemon(Composite):
    id = saveable_int('u16')
    min_lvl = saveable_int('u16')
    max_lvl = saveable_int('u16')
    rarity = saveable_int('u16')
    overrides = array(Override)
