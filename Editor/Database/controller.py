__author__ = 'Vincent'

from abc import ABCMeta, abstractmethod, abstractstaticmethod

class Controller():

    __metaclass__ = ABCMeta

    def __init__(self,dataBaseType,dataType):
        self.model   = dataBaseType(dataType)  #Should have a Database Object attached
        self.cur_ind = -1
        self.loadfuncs = [] #each func is passed the current index as an argument
        self.sorts = [("Sort by Name",self.changeSort),("Sort by ID",self.changeSort)]



    def changeSort(self):
        """Changes the sort type of the database"""
        self.model.changeSort()
        if self.cur_ind == -1:
            return
        self.load()

    def up(self):
        """Moves the current index up"""
        if not self.cur_ind == 0:
            self.cur_ind -= 1
            self.load()

    def down(self):
        """Moves the current index down"""
        if not self.cur_ind == len(self.model)-1:
            self.cur_ind += 1
            self.load()

    def click(self,ind):
        """Given an index, changes the current index and then loads that index"""
        self.cur_ind = ind
        self.load()

    def addObj(self):
        """Adda a new object to the database"""
        ind = self.model.add()
        self.cur_ind = ind
        self.load()

    def delObj(self,ind):
        """Deletes an object from the database"""
        if ind < 0:
            return
        self.model.remove(ind)
        self.cur_ind -= 1
        if self.cur_ind <0:
            self.cur_ind = 0
        self.load()

    def load(self):
        """Loads all components"""
        for func in self.loadfuncs:
            func(self.cur_ind)

    def saveToFile(self,path):
        """Saves the model to 'path' """
        data = self.model.toByteArray()
        file = open(path,'wb')
        file.write(data)
        file.close()

    def loadFromFile(self,path):
        """Loads the model from specified 'path' """
        file = open(path,'rb')
        data = bytearray(file.read())
        file.close()
        db = self.model.fromByteArray(data)
        self.model = db
        self.load()

    def getStrings(self):
        """Get a list of strings representing all the objects"""
        return self.model.getStrings()