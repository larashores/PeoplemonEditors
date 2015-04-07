__author__ = 'Vincent'

from Editor.Component import Component
from Editor.structreader import pack, unpack

class Database(Component):
    """
    Represents a database
    """

    def __init__(self,dataType):
        self.dataObjs = []
        self.dataType = dataType


    def add(self):
        """
        Adda a default object to the database, returns the index in the database
        """

        obj = self.dataType()
        self.dataObjs.append(obj)
        return self.dataObjs.index(obj)

    def remove(self,ind):
        """
        Removes an object from the database

        :param ind: The index to remove from
        :return:
        """

        self.dataObjs.pop(ind)

    def getStrings(self):
        """
        Get a list of strings representing the objects

        :return:
        """
        lst = []
        for obj in self.dataObjs:
            lst.append(str(obj))
        return lst

    def update(self,param):
        """
        Updates a method from the component, the parameter should be the index to update, and then any paramters of that object
        :param param:
        :return:
        """
        ind = param.pop(0)
        self.dataObjs[ind].update(param)

    def load(self):
        params = [len(self.dataObjs)]
        for obj in self.dataObjs:
            params += obj.load()
        return params

    def fromByteArray(self,byteArray):
        db = self.__class__(self.dataType)
        numObjs = unpack(byteArray,'u16')
        for _ in range(numObjs):
            obj = self.dataType()
            db.dataObjs.append(obj.fromByteArray(byteArray))

    def toByteArray(self):
        data = bytearray()
        pack(data,len(self.dataObjs),'u16')
        for obj in self.dataObjs:
            data += obj.toByteArray()
        return data


