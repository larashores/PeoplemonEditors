__author__ = 'Vincent'

from Editor.Component import Component
from Editor.ItemDatabase.Item import Item
from Editor.structreader import pack, unpack


class Move(Component):
    def __init__(self):
        Component.__init__(self)
        self.addParam('id',0)
        self.addParam('name','')
        self.addParam('desc','')
        self.addParam('isSpecial',False)
        self.addParam('atk',0)
        self.addParam('acc',0)
        self.addParam('priority',0)
        self.addParam('pp',0)
        self.addParam('type',0)
        self.addParam('effect',0)
        self.addParam('chanceOfEffect',0)
        self.addParam('effectIntensity',0)
        self.addParam('effectTargetsSelf',False)
        self.addParam('attackerAnim','')
        self.addParam('defenderAnim','')
        self.addParam('classification',0)
        self.addParam('effectScore',0)

    def __str__(self):
        return Item.__str__(self)

    def fromByteArray(self,byteArray):
        move = Move()
        move.paramDict['id'] = unpack(byteArray,'u16')
        move.paramDict['name'] = unpack(byteArray,'str')
        move.paramDict['desc'] = unpack(byteArray,'str')
        move.paramDict['isSpecial'] = bool(unpack(byteArray,'u8'))
        move.paramDict['atk'] = unpack(byteArray,'u16')
        move.paramDict['acc'] = unpack(byteArray,'u16')
        move.paramDict['priority'] = unpack(byteArray,'u16')
        move.paramDict['pp'] = unpack(byteArray,'u16')
        move.paramDict['type'] = unpack(byteArray,'u8')
        move.paramDict['effect'] = unpack(byteArray,'u8')
        move.paramDict['chanceOfEffect'] = unpack(byteArray,'u8')
        move.paramDict['effectIntensity'] = unpack(byteArray,'u8')
        move.paramDict['effectTargetsSelf'] = int(unpack(byteArray,'u8'))
        move.paramDict['attackerAnim'] = unpack(byteArray,'str')
        move.paramDict['defenderAnim'] = unpack(byteArray,'str')
        move.paramDict['classification'] = unpack(byteArray,'u8')
        move.paramDict['effectScore'] = unpack(byteArray,'u8')
        return move
    def toByteArray(self):
        data = bytearray()
        pack(data,self.paramDict['id'],'u16')
        pack(data,self.paramDict['name'],'str')
        pack(data,self.paramDict['desc'],'str')
        pack(data,int(self.paramDict['isSpecial']),'u8')
        pack(data,self.paramDict['atk'],'u16')
        pack(data,self.paramDict['acc'],'u16')
        pack(data,self.paramDict['priority'],'u16')
        pack(data,self.paramDict['pp'],'u16')
        pack(data,self.paramDict['type'],'u8')
        pack(data,self.paramDict['effect'],'u8')
        pack(data,self.paramDict['chanceOfEffect'],'u8')
        pack(data,self.paramDict['effectIntensity'],'u8')
        pack(data,int(self.paramDict['effectTargetsSelf']),'u8')
        pack(data,self.paramDict['attackerAnim'],'str')
        pack(data,self.paramDict['defenderAnim'],'str')
        pack(data,self.paramDict['classification'],'u8')
        pack(data,self.paramDict['effectScore'],'u8')

        return data