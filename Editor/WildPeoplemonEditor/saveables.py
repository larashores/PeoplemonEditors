from Editor.saveable.composite import Composite
from Editor.saveable.saveableInt import U16
from Editor.saveable.saveableArray import array
from Editor.saveable.saveableString import SaveableString


class Override(Composite):
    code = SaveableString
    override = U16

    def __str__(self):
        return 'Code: {}, Value: {}'.format(self.code.get(), self.override.get())


class WildPeoplemon(Composite):
    id = U16
    min_lvl = U16
    max_lvl = U16
    rarity = U16
    overrides = array(Override)
