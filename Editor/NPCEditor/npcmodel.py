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

class NPC():
    '''
    Class to represent NPC, creates walkBehavior class on instanciation
    '''
    def __init__(self):
        self.name = ''
        self.animation = ''
        self.convoFile = ''
        self.walkBehavior = WalkBehavior()

class WalkBehavior():
    '''
    Class to reprsent type of walking behavior. Type can be 0 = stand still,
    1 = spin in place, 2 = follow path, 3 = wander freely
    '''
    def __init__(self):
        self.type = 0           #initialize to standing still
        self.motionType = 0     #Used if  motion is type 1
                                #0 = Clockwise, 1 = Counterclockwise, 2 = random
        self.wanderRadius = 5       #Used if motion type is set to 3
        self.reverseLoop = 0        #Used if motion type is set to 2
        self.nodes = []             #Path for npc to take if motion is type 2
    def addNode(self,direction,steps,ind=-1):
        '''
        Adds node at given index, if it's not given it will append to back
        '''
        if ind == -1:
            self.nodes.append( Node(direction,steps) )
        else:
            self.nodes.insert( ind, Node() )
    def deleteNode(self, ind=-1):
        '''
        Deletes node at given index, if none are given, node is deleted from
        the back
        '''
        if ind == -1:
            self.nodes.pop()
        else:
            self.nodes.pop(ind)


class Node():
    '''
    Class to represnt part of a path
    '''
    def __init__(self,direction,numSteps):
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
            print('error',self.direction)
    def setDirection(self,code):
        print('code;   ',code)
        if code == 0:
            self.direction = 'up'
        elif code == 1:
            self.direction = 'right'
        elif code == 2:
            self.direction = 'down'
        elif code == 3:
            self.direction = 'left'