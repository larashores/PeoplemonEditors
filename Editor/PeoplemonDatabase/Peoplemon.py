__author__ = 'Vincent'

from Editor.Component import Component
from Editor.Database.database import Database
from Editor.structreader import pack, unpack
from Editor.ItemDatabase.Item import Item


class Peoplemon(Component):
    def __init__(self):
        Component.__init__(self)
        self.addParam('id', 0)
        self.addParam('name', '')
        self.addParam('desc', '')
        self.addParam('type', 0)
        self.addParam('specialAbilityId', 0)
        self.baseStats = BaseStats()
        self.addParam('validMoves', [])
        self.addParam('learnMoves', [])
        self.addParam('evolveLevel', 0)
        self.addParam('evolveID', 0)
        self.addParam('baseXPYield',0)
        self.addParam('xpGroup',0)
        self.evAwards = EVAwards()
        self.validMoves = Database(ValidMove)
        self.learnMoves = Database(LearnMove)

    def __str__(self):
        return Item.__str__(self)

    def __repr__(self):
        return Item.__str__(self)

    def fromByteArray(self,byteArray):
        people = Peoplemon()
        people.paramDict['id'] = unpack(byteArray,'u16')
        people.paramDict['name'] = unpack(byteArray,'str')
        people.paramDict['desc'] = unpack(byteArray,'str')
        people.paramDict['type'] = unpack(byteArray,'u8')
        people.paramDict['specialAbilityId'] = unpack(byteArray,'u8')

        people.baseStats = self.baseStats.fromByteArray(byteArray)
        db = Database(ValidMove)
        people.validMoves = db.fromByteArray(byteArray)
        db = Database(LearnMove)
        people.learnMoves= db.fromByteArray(byteArray)
        people.paramDict['evolveLevel'] = unpack(byteArray,'u8')
        people.paramDict['evolveID'] = unpack(byteArray,'u8')
        people.paramDict['baseXPYield'] = unpack(byteArray,'u16')
        people.paramDict['xpGroup'] = unpack(byteArray,'u8')
        people.evAwards = self.evAwards.fromByteArray(byteArray)
        return people

    def toByteArray(self):
        data = bytearray()
        pack(data,self.paramDict['id'],'u16')
        pack(data,self.paramDict['name'],'str')
        pack(data,self.paramDict['desc'],'str')
        pack(data,self.paramDict['type'],'u8')
        pack(data,self.paramDict['specialAbilityId'],'u8')
        data += self.baseStats.toByteArray()

        data += self.validMoves.toByteArray()
        data += self.learnMoves.toByteArray()

        pack(data,self.paramDict['evolveLevel'],'u8')
        pack(data,self.paramDict['evolveID'], 'u8')

        pack(data,self.paramDict['baseXPYield'],'u16')
        pack(data,self.paramDict['xpGroup'],'u8')

        data += self.evAwards.toByteArray()
        return data


    def load(self,params,options=list()):
        if not options:
            return Component.load(self,params)
        elif options == ['baseStats']:
            return self.baseStats.load(params)
        elif options == ['evAwards']:
            return self.evAwards.load(params)

    def update(self,paramdict,options=None):
        if not options:
            return Component.update(self,paramdict)
        elif options == ['baseStats']:
            return self.baseStats.update(paramdict)
        elif options == ['evAwards']:
            return self.evAwards.update(paramdict)


class BaseStats(Component):
    stats = ('hp','atk','def','acc','evade','spd','crit','spatk','spdef')

    def __init__(self):
        Component.__init__(self)

        for stat in self.stats:
            self.addParam(stat,0)

    def fromByteArray(self,byteArray):
        stats = BaseStats()
        numStats = len(self.stats)
        for ind in range(numStats):
            stats.paramDict[self.stats[ind]] = unpack(byteArray,'u16')
        return stats

    def toByteArray(self):
        data = bytearray()
        for stat in self.stats:
            pack(data,self.paramDict[stat],'u16')
        return data

class EVAwards(BaseStats):
    pass

class ValidMove(Component):
    def __init__(self):
        Component.__init__(self)
        self.addParam('id',0)
    def __str__(self):
        return 'Move ID: {}'.format(self.paramDict['id'])
    def fromByteArray(self,byteArray):
        learnMove = ValidMove()
        learnMove.paramDict['id'] = unpack(byteArray,'u16')
        return learnMove

    def toByteArray(self):
        data = bytearray()
        pack(data,self.paramDict['id'],'u16')
        return data

class LearnMove(Component):
    def __init__(self):
        Component.__init__(self)
        self.addParam('level',0)
        self.addParam('id',0)

    def __str__(self):
        return 'Move ID: {} | Learn level: {}'.format(self.paramDict['id'],self.paramDict['level'])

    def fromByteArray(self,byteArray):
        learnMove = LearnMove()
        learnMove.paramDict['level'] = unpack(byteArray,'u8')
        learnMove.paramDict['id'] = unpack(byteArray,'u16')
        return learnMove

    def toByteArray(self):
        data = bytearray()
        pack(data,self.paramDict['level'],'u8')
        pack(data,self.paramDict['id'],'u16')
        return data