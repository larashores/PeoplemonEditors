__author__ = 'Vincent'

from Editor.Component import Component
from Editor.PeoplemonDatabase.Peoplemon import BaseStats
from Editor.structreader import pack, unpack

class Peoplemon(Component):

    def __init__(self):
        Component.__init__(self)
        self.addParam('nickname','')
        self.addParam('id',0)
        self.addParam('level',0)
        self.addParam('holdItemID',0)

        self.moveList = []
        for _ in range(4):
            self.moveList.append( [0,0] )

        self.IVs = IVs()
        self.EVs = EVs()


    def fromByteArray(self,byteArray):
        """
        Makes a new Component object from a bytearray

        :param byteArray:   The bytearray representing the object
        :return:            A Component object
        """
        data = byteArray
        peoplemon = Peoplemon()
        peoplemon.paramDict['nickname'] = unpack(data,'str')
        peoplemon.paramDict['id'] = unpack(data,'u16')
        peoplemon.paramDict['level'] = unpack(data,'u16')
        unpack(data,'u32')
        unpack(data,'u32')
        unpack(data,'u16')
        unpack(data,'u8')
        peoplemon.paramDict['holdItemID'] = unpack(data,'u16')
        for ind in range(4):
            peoplemon.moveList[ind][0] = unpack(data,'u16')
            peoplemon.moveList[ind][1] = unpack(data,'u16')

        peoplemon.IVs = self.IVs.fromByteArray(data)
        peoplemon.EVs = self.EVs.fromByteArray(data)
        return peoplemon


    def toByteArray(self):
        """
        Return a bytearray representation of the Component

        :return:            The bytearray
        """
        data = bytearray()
        pack(data,self.paramDict['nickname'],'str')
        pack(data,self.paramDict['id'],'u16')
        pack(data,self.paramDict['level'],'u16')
        pack(data,0,'u32')  #CurXP
        pack(data,0,'u32')  #XP till Next level up
        pack(data,0,'u16')  #Current HP
        pack(data,0,'u8')   #Current Ailment
        pack(data,self.paramDict['holdItemID'],'u16')
        for ID,PP in self.moveList:
            pack(data,ID,'u16')
            pack(data,PP,'u16')
        data += self.IVs.toByteArray()
        data += self.EVs.toByteArray()

        return data



class IVs(BaseStats):
    stats = ('hp','atk','def','spatk','spdef','acc','evade','spd','crit')

class EVs(IVs):
    pass