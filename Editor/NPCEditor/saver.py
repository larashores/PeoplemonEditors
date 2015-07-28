'''
#-------------------------------------------------------------------------------
# Name:        module2

# Author:      Vincent
#
# Date Created:     02/12/2015
# Date Modified:    02/12/2015
#-------------------------------------------------------------------------------

Purpose:

'''
from Editor.NPCEditor.npcmodel import *

from Editor.structreader import pack, unpack

def saveNPC(npc,file_path):
    data = bytearray()
    pack(data, npc.name, 'str')
    pack(data, npc.animation, 'str')
    pack(data, npc.convoFile, 'str')

    behavior = npc.walkBehavior

    pack(data,behavior.type,'u8')

    if behavior.type == 1:
        pack(data,behavior.motionType,'u8')
    if behavior.type == 2:
        pack(data,len(behavior.nodes),'u8')
        pack(data,behavior.reverseLoop,'u8')
        for node in behavior.nodes:
            pack(data,node.getDirection(),'u8')
            pack(data,node.numSteps,'u8')
    if behavior.type == 3:
        pack(data,behavior.wanderRadius,'u8')

    file = open(file_path,'wb')
    file.write(data)
    file.close()

def loadNPC(file_path):
    file = open(file_path,'rb')
    data = bytearray(file.read())
    file.close()

    npc = NPC()
    npc.name = unpack(data,'str')
    npc.animation = unpack(data,'str')
    npc.convoFile = unpack(data,'str')

    behavior = npc.walkBehavior
    behavior.type = unpack(data,'u8')

    if behavior.type == 1:
        behavior.motionType = unpack(data,'u8')
    elif behavior.type == 2:
        numNodes = unpack(data,'u8')
        npc.walkBehavior.reverseLoop = unpack(data,'u8')
        for _ in range(numNodes):
            direction = unpack(data,'u8')
            steps =  unpack(data,'u8')
            node = Node(direction,steps)
            node.setDirection(direction)
            behavior.nodes.append(node)
    elif behavior.type == 3:
        behavior.wanderRadius = unpack(data,'u8')
    return npc