'''
#-------------------------------------------------------------------------------
# Name:        module1

# Author:      Vincent
#
# Date Created:     02/12/2015
# Date Modified:    02/12/2015
#-------------------------------------------------------------------------------

Purpose:

'''


from Editor.NPCEditor.saver import *
from Editor.NPCEditor.constants import *

from tkinter.messagebox import showerror

class Controller():
    def __init__(self):
        self.model = NPC()
        self.load_funcs = {'name': None,
                           'animation': None,
                           'conversation': None,
                           'behavior': None,
                           'direction': None,
                           'wanderRadius': None,
                           'nodes': None}
        for func in self.load_funcs:
            self.load_funcs[func] = lambda x: None

    def updateModel(self,code,value):
        if code == 'name':
            self.model.name = value
        elif code == 'anim':
            self.model.animation = value
        elif code == 'convo':
            self.model.convoFile = value
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
            self.model.walkBehavior.addNode( *value )   #Should be a tuple
        elif code == 'del':
            self.model.walkBehavior.deleteNode(int(value))
        elif code == 'rev':
            self.model.walkBehavior.reverseLoop = value
        elif code == 'wander':
            self.model.walkBehavior.wanderRadius = value

    def save(self, path):
        try:
            saveNPC(self.model, path)
        except:
            showerror(title='Error', message='Error Saving File')

    def load(self,path):
        try:
            npc = loadNPC(path)
        except:
            showerror(title='Error', message='Error Loading File')
            return
        self.model = npc
        self.load_funcs['name'](self.model.name)
        self.load_funcs['animation'](self.model.animation)
        self.load_funcs['conversation'](self.model.convoFile)

        b_type = self.model.walkBehavior.type
        if b_type == 0:
            self.load_funcs['behavior'](B_STILL)
        elif b_type == 1:
            self.load_funcs['behavior'](B_SPIN)
        elif b_type == 2:
            self.load_funcs['behavior'](B_FOLLOW)
        elif b_type == 3:
            self.load_funcs['behavior'](B_WANDER)

        direction = self.model.walkBehavior.motionType
        if direction == 0:
            self.load_funcs['direction'](D_CLOCK)
        elif direction == 1:
            self.load_funcs['direction'](D_COUNTER)
        elif direction == 2:
            self.load_funcs['direction'](D_RANDOM)

        self.load_funcs['wanderRadius'](self.model.walkBehavior.wanderRadius)
        nodes = []
        for node in self.model.walkBehavior.nodes:
            nodes.append( (node.direction,node.numSteps) )
        self.load_funcs['nodes']( (self.model.walkBehavior.reverseLoop,nodes) )
