__author__ = 'Vincent'

from Editor.Component import Component
from Editor.structreader import pack, unpack


class Trainer(Component):
    def __init__(self):
        Component.__init__(self)
        self.addParam('name', '')
        self.addParam('animation', '')
        self.addParam('beforeConvo', '')
        self.addParam('afterConvo', '')
        self.addParam('lostText', '')
        self.addParam('sightRange', 0)

        self.peoplemonList = PeoplemonFileList()
        self.itemList = ItemList()

        self.addParam('aiType', 0)

        self.walkBehavior = WalkBehavior()

    def fromByteArray(self, byteArray):
        data = byteArray
        trainer = Trainer()
        trainer.paramDict['name'] = unpack(data, 'str')
        trainer.paramDict['animation'] = unpack(data, 'str')
        trainer.paramDict['beforeConvo'] = unpack(data, 'str')
        trainer.paramDict['afterConvo'] = unpack(data, 'str')
        trainer.paramDict['lostText'] = unpack(data, 'str')
        trainer.paramDict['sightRange'] = unpack(data, 'u8')

        trainer.peoplemonList = self.peoplemonList.fromByteArray(data)
        trainer.itemList = self.itemList.fromByteArray(data)

        trainer.paramDict['aiType'] = unpack(data, 'u8')
        trainer.walkBehavior = self.walkBehavior.fromByteArray(data)
        return trainer

    def toByteArray(self):
        data = bytearray()
        pack(data, self.paramDict['name'], 'str')
        pack(data, self.paramDict['animation'], 'str')
        pack(data, self.paramDict['beforeConvo'], 'str')
        pack(data, self.paramDict['afterConvo'], 'str')
        pack(data, self.paramDict['lostText'], 'str')
        pack(data, self.paramDict['sightRange'], 'u8')

        data += self.peoplemonList.toByteArray()
        data += self.itemList.toByteArray()

        pack(data, self.paramDict['aiType'], 'u8')
        data += self.walkBehavior.toByteArray()
        return data


class PeoplemonFileList(Component):
    def __init__(self):
        Component.__init__(self)
        self.peoplemon = []

    def addFileName(self, file_name):
        self.peoplemon.append(file_name)

    def deleteFileName(self, ind):
        self.peoplemon.pop(ind)

    def fromByteArray(self, byteArray):
        fileList = PeoplemonFileList()
        num = unpack(byteArray, 'u16')
        for _ in range(num):
            name = unpack(byteArray, 'str')
            fileList.addFileName(name)
        return fileList

    def toByteArray(self):
        data = bytearray()
        num = len(self.peoplemon)
        pack(data, num, 'u16')
        for file_name in self.peoplemon:
            pack(data, file_name, 'str')
        return data


class ItemList(Component):
    def __init__(self):
        Component.__init__(self)
        self.items = []

    def addItem(self, file_name):
        self.items.append(file_name)

    def deleteItem(self, ind):
        self.items.pop(ind)

    def fromByteArray(self, byteArray):
        itemList = ItemList()
        num = unpack(byteArray, 'u8')
        for _ in range(num):
            name = unpack(byteArray, 'u16')
            itemList.addItem(name)
        return itemList

    def toByteArray(self):
        data = bytearray()
        num = len(self.items)
        pack(data, num, 'u8')
        for item_num in self.items:
            pack(data, item_num, 'u16')
        return data


class WalkBehavior(Component):
    """
    Class to reprsent type of walking behavior. Type can be 0 = stand still,
    1 = spin in place, 2 = follow path, 3 = wander freely
    """
    def __init__(self):
        Component.__init__(self)
        self.type = 0           # initialize to standing still
        self.motionType = 0     # Used if  motion is type 1
                                # 0 = Clockwise, 1 = Counterclockwise, 2 = random
        self.wanderRadius = 5       # Used if motion type is set to 3
        self.reverseLoop = 0        # Used if motion type is set to 2
        self.nodes = []             # Path for npc to take if motion is type 2

    def addNode(self, direction, steps, ind=-1):
        """
        Adds node at given index, if it's not given it will append to back
        """
        if ind == -1:
            self.nodes.append(Node(direction, steps))
        else:
            self.nodes.insert(ind, Node(direction, steps))

    def deleteNode(self, ind=-1):
        """
        Deletes node at given index, if none are given, node is deleted from
        the back
        """
        if ind == -1:
            self.nodes.pop()
        else:
            self.nodes.pop(ind)

    def toByteArray(self):
        data = bytearray()
        pack(data, self.type, 'u8')
        if self.type == 1:
            pack(data, self.motionType, 'u8')
        elif self.type == 2:
            pack(data, len(self.nodes), 'u8')
            pack(data, self.reverseLoop, 'u8')
            for node in self.nodes:
                data += node.toByteArray()
        elif self.type == 3:
            pack(data, self.wanderRadius, 'u8')

        return data

    def fromByteArray(self, byteArray):
        data = byteArray

        walk = WalkBehavior()
        walk.type = unpack(data, 'u8')
        if walk.type == 1:
            walk.motionType = unpack(data, 'u8')
        elif walk.type == 2:
            numNodes = unpack(data, 'u8')
            walk.reverseLoop = unpack(data, 'u8')
            n = Node(0, 0)
            for _ in range(numNodes):
                node = n.fromByteArray(data)
                walk.nodes.append(node)
        elif walk.type == 3:
            walk.wanderRadius = unpack(data, 'u8')

        return walk


class Node:
    """
    Class to represnt part of a path
    """
    def __init__(self, direction, numSteps):
        self.direction = direction
        self.numSteps = numSteps

    def getDirection(self):
        if self.direction == 'up':
            return 0
        elif self.direction == 'right':
            return 1
        elif self.direction == 'down':
            return 2
        elif self.direction == 'left':
            return 3
        else:
            print('error', self.direction)

    def setDirection(self, code):
        if code == 0 or code == 'up':
            self.direction = 0
        elif code == 1 or code == 'right':
            self.direction = 1
        elif code == 2 or code == 'down':
            self.direction = 2
        elif code == 3 or code == 'left':
            self.direction = 3

    def toByteArray(self):
        data = bytearray()
        pack(data, self.getDirection(), 'u8')
        pack(data, self.numSteps, 'u8')
        return data

    def fromByteArray(self, data):
        directions = {0: 'up', 1: 'right', 2: 'down', 3: 'left'}
        direction = unpack(data, 'u8')
        numSteps = unpack(data, 'u8')
        node = Node(directions[direction], numSteps)
        return node
