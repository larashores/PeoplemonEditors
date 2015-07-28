__author__ = 'Vincent'

from Editor.TrainerEditor.trainer import Trainer
from Editor.TrainerEditor.constants import *

from tkinter.messagebox import showerror

class Controller:
    def __init__(self):
        self.model = Trainer()
        self.load_funcs = []
        self.apply_funcs = []

    def updateModel(self, code, value):
        if code == 'name':
            self.model.paramDict['name'] = value
        elif code == 'anim':
            self.model.paramDict['animation'] = value
        elif code == 'beforeConvo':
            self.model.paramDict['beforeConvo'] = value
        elif code == 'afterConvo':
            self.model.paramDict['afterConvo'] = value
        elif code == 'lostText':
            self.model.paramDict['lostText'] = value
        elif code == 'sight':
            self.model.paramDict['sightRange'] = value
        elif code == 'aiType':
            self.model.paramDict['aiType'] = value
        elif code == 'add-peoplemon':
            self.model.peoplemonList.addFileName(value)
        elif code == 'add-item':
            self.model.itemList.addItem(value)
        elif code == 'del-peoplemon':
            self.model.peoplemonList.deleteFileName(value)
        elif code == 'del-item':
            self.model.itemList.deleteItem(value)
        elif code == 'behavior':
            if value == B_STILL:
                self.model.walkBehavior.type = 0
            elif value == B_SPIN:
                self.model.walkBehavior.type = 1
            elif value == B_FOLLOW:
                self.model.walkBehavior.type = 2
            elif value == B_WANDER:
                self.model.walkBehavior.type = 3
        elif code == 'direction':
            if value == D_CLOCK:
                self.model.walkBehavior.motionType = 0
            elif value == D_COUNTER:
                self.model.walkBehavior.motionType = 1
            elif value == D_RANDOM:
                self.model.walkBehavior.motionType = 2
        elif code == 'add':
            self.model.walkBehavior.addNode(*value)   #Should be a tuple
        elif code == 'del':
            self.model.walkBehavior.deleteNode(int(value))
        elif code == 'rev':
            self.model.walkBehavior.reverseLoop = value
        elif code == 'wander':
            self.model.walkBehavior.wanderRadius = value
        else:
            raise Exception('Unknown code' + str(code))

    def loadAttribs(self, names):
        results = []
        for name in names:
            results.append(self.model.paramDict[name])
        return results

    def save(self, path):
        try:
            file = open(path, 'wb')
            data = self.model.toByteArray()
            file.write(data)
            file.close()
        except:
            showerror(title='Error', message='Error Saving File')

    def load(self, path):
        try:
            file = open(path, 'rb')
            data = bytearray(file.read())
            model = self.model.fromByteArray(data)
            self.model = model
            for func in self.load_funcs:
                func()
        except:
            showerror(title='Error', message='Error Loading File')
            return

    def getPeoplemon(self):
        return self.model.peoplemonList.peoplemon

    def getItems(self):
        return self.model.itemList.items

    def getType(self):
        type_code = self.model.walkBehavior.type
        for name, code in {B_STILL: 0, B_SPIN: 1, B_FOLLOW: 2, B_WANDER: 3}.items():
            if type_code == code:
                return name

    def getDirection(self):
        direction_code = self.model.walkBehavior.motionType
        for name, code in {D_CLOCK: 0, D_COUNTER: 1, D_RANDOM: 2}.items():
            if direction_code == code:
                return name

    def getWanderRadius(self):
        return self.model.walkBehavior.wanderRadius

    def getReverseLoop(self):
        return self.model.walkBehavior.reverseLoop

    def getNodes(self):
        nodes = []
        for node in self.model.walkBehavior.nodes:
            nodes.append((node.direction, node.numSteps))
        return nodes

    def apply(self):
        for func in self.apply_funcs:
            func()
