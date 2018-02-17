from Editor.saveable.composite import Composite
from Editor.saveable.saveableInt import saveable_int
from Editor.saveable.saveableArray import array
from Editor.saveable.saveableString import SaveableString


class Move(Composite):
    id = saveable_int('u16')
    pp = saveable_int('u16')


class Stats(Composite):
    hp = saveable_int('u16')
    attack = saveable_int('u16')
    defense = saveable_int('u16')
    special_attack = saveable_int('u16')
    special_defense = saveable_int('u16')
    accuracy = saveable_int('u16')
    evade = saveable_int('u16')
    speed = saveable_int('u16')
    critical = saveable_int('u16')


class TrainerPeoplemon(Composite):
    nickname = SaveableString
    id = saveable_int('u16')
    level = saveable_int('u16')
    cur_xp = saveable_int('u32')
    next_level_up_xp = saveable_int('u32')
    cur_hp = saveable_int('u16')
    cur_ail = saveable_int('u8')
    hold_item = saveable_int('u16')
    move1 = Move
    move2 = Move
    move3 = Move
    move4 = Move
    ivs = Stats
    evs = Stats
