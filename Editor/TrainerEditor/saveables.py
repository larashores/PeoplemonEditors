from Editor.saveable.composite import Composite
from Editor.saveable.saveableInt import saveable_int
from Editor.saveable.saveableArray import array
from Editor.saveable.saveableString import SaveableString
from Editor.saveable.saveable import SaveableType
from Editor.saveable.union import Union

from Editor.signal import Signal


class Node(Composite):
    direction = saveable_int('u8')
    num_steps = saveable_int('u8')


class StandStillBehavior(Composite):
    pass


class SpinInPlaceBehavior(Composite):
    motion = saveable_int('u8')


class FollowPathBehavior(Composite):
    reverse_loop = saveable_int('u8')
    nodes = array(Node)


class WanderBehavior(Composite):
    id = saveable_int('u8')
    radius = saveable_int('u8')


class Behavior(Union):
    still = StandStillBehavior
    spin = SpinInPlaceBehavior
    follow = FollowPathBehavior
    wander = WanderBehavior


class Peoplemon(SaveableString):
    def __str__(self):
        return '"' + self.get() + '"'


class Trainer(Composite):
    name = SaveableString
    animation = SaveableString
    before_convo = SaveableString
    after_convo = SaveableString
    lose_message = SaveableString
    playlist = SaveableString
    background_image = SaveableString
    sight_range = saveable_int('u8')
    peoplemon = array(Peoplemon)
    items = array(saveable_int('u16'))
    ai_type = saveable_int('u8')
    behavior = Behavior
