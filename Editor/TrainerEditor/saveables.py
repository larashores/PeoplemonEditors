from Editor.saveable.composite import Composite
from Editor.saveable.saveableInt import U8, U16
from Editor.saveable.saveableArray import array
from Editor.saveable.saveableString import SaveableString
from Editor.saveable.union import Union


class Node(Composite):
    direction = U8
    num_steps = U8

    def __str__(self):
        node_to_string = ['Up', 'Right', 'Down', 'Left']
        return 'Direction: {}, Number of Steps: {}'.format(node_to_string[self.direction.get()], self.num_steps.get())


class StandStillBehavior(Composite):
    pass


class SpinInPlaceBehavior(Composite):
    motion = U8


class FollowPathBehavior(Composite):
    reverse_loop = U8
    nodes = array(Node)

    def to_byte_array(self):
        data = bytearray()
        num_nodes = U8(len(self.nodes))
        data += num_nodes.to_byte_array()
        data += self.reverse_loop.to_byte_array()
        for item in self.nodes:
            data += item.to_byte_array()
        return data

    def load_in_place(self, byte_array):
        num_nodes = U8
        num_nodes.load_in_place(byte_array)
        self.reverse_loop.load_in_place(byte_array)
        self.nodes.clear()
        for i in range(num_nodes):
            self.nodes.append(Node.from_byte_array(byte_array))


class WanderBehavior(Composite):
    radius = U8


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
    sight_range = U8
    peoplemon = array(Peoplemon)
    items = array(U16, U8)
    ai_type = U8
    behavior = Behavior
