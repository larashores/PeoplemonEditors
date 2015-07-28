__author__ = 'Vincent'

from Editor.TrainerPeoplemonEditor.peoplemon import Peoplemon

from tkinter.messagebox import showerror

class Controller():
    def __init__(self):
        self.model = Peoplemon()
        self.loadFunc = lambda: None #Put func here
        self.applyFunc = lambda: None #Samesies
    def update(self,paramdict):
        self.model.update(paramdict)
    def updateMove(self,moveNum,moveInd,pp):
        self.model.moveList[moveNum][0] = moveInd
        self.model.moveList[moveNum][1] = pp
    def updateIV(self,value,name):
        self.model.IVs.update({name: value})
    def updateEV(self,value,name):
        self.model.EVs.update({name: value})
    def load(self,loads):
        return self.model.load(loads)
    def loadMove(self,ind):
        return self.model.moveList[ind][0],self.model.moveList[ind][1]
    def loadEV(self):
        return self.model.EVs.load(self.model.EVs.stats)
    def loadIV(self):
        return self.model.IVs.load(self.model.IVs.stats)
    def saveToFile(self,path):
        """Saves the model to 'path' """
        self.applyFunc()
        try:
            data = self.model.toByteArray()
            file = open(path,'wb')
            file.write(data)
            file.close()
        except:
            showerror(title='Error', message='Error: Error Saving File')

    def loadFromFile(self,path):
        """Loads the model from specified 'path' """
        try:
            file = open(path,'rb')
            data = bytearray(file.read())
            file.close()

            peoplemon = self.model.fromByteArray(data)
            self.model = peoplemon
            self.loadFunc()
        except:
            showerror(title='Error', message='Error: Error loading file')