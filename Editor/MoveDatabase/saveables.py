from Editor.saveable.composite import Composite
from Editor.saveable.saveableInt import saveable_int
from Editor.saveable.saveableArray import array
from Editor.saveable.saveableString import SaveableString

U8 = saveable_int('u8')
U16 = saveable_int('u16')


class Move(Composite):
    id = U16
    name = SaveableString
    description = SaveableString
    is_special = U8
    attack = U16
    accuracy = U16
    priority = U16
    pp = U16
    type = U8
    effect = U8
    effect_chance = U8
    effect_intensity = U8
    effect_targets_self = U8
    attacker_anim = SaveableString
    defender_anim = SaveableString
    classification = U8
    effect_score = U8

    def __str__(self):
        return 'ID: {} | Name: {} | Desc: {}'.format(self.id.get(), self.name.get(), self.description.get())
