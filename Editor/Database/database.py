__author__ = 'Vincent'

from Editor.Component import Component
from Editor.structreader import pack, unpack

class Database(Component):
    """
    Represents a database
    """

    def __init__(self,dataType):
        Component.__init__(self)
        self.dataObjs = []
        self.dataType = dataType
        self.sortFunc = self.sortByIDKey

    def sort(self):
        """
        Sorts the database by using self.sortFunc
        """
        self.dataObjs.sort(key=self.sortFunc)

    def changeSort(self):
        """Swaps the type of sorting being used"""
        if self.sortFunc == self.sortByIDKey:
            self.sortFunc = self.sortByNameKey
        elif self.sortFunc == self.sortByNameKey:
            self.sortFunc = self.sortByIDKey
        self.sort()

    def sortByIDKey(self, obj):
        """Function to help sort items by their ID"""
        return obj.load( ['id'] )[0]

    def sortByNameKey(self, obj):
        """Function to help sort items by their name"""
        return obj.load( ['name'] )[0]

    def add(self):
        """
        Adda a default object to the database, returns the index in the database
        """

        obj = self.dataType()
        obj.update({'id':self.nextID()})
        self.dataObjs.append(obj)
        self.sort()
        return self.dataObjs.index(obj)

    def getIDs(self):
        """Gets a list of all IDs that are used in the database"""
        ids = []
        for obj in self.dataObjs:
            ids.append(obj.load(['id'])[0])
        return ids

    def nextID(self):
        """Returns the next unused ID in the list"""
        id = 0
        while id in self.getIDs():
            id += 1
        return id

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

    def updateObject(self,ind,paramdict):
        self.dataObjs[ind].update(paramdict)

    def update(self,paramdict,options=None):
        """
        Updates a method from the component, the parameter should be the index to update, and then any paramters of that object
        :param param:
        :return:
        """
        if not options:
            raise Exception("Bad index")
        ind = options[0]
        obj = self.dataObjs[ind]
        obj.update(paramdict)
        return self.dataObjs.index(obj)

    def load(self,params,options=None):
        if not options:
            raise Exception("Bad index")
        ind = options[0]
        obj = self.dataObjs[ind]
        return obj.load(params)

    def fromByteArray(self,byteArray):
        db = self.__class__(self.dataType)
        numObjs = unpack(byteArray,'u16')
        obj = self.dataType()
        for _ in range(numObjs):
            db.dataObjs.append(obj.fromByteArray(byteArray))
        return db
    
    def toByteArray(self):
        data = bytearray()
        pack(data,len(self.dataObjs),'u16')
        for obj in self.dataObjs:
            data += obj.toByteArray()
        return data


