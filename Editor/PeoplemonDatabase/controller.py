__author__ = 'Vincent'

from Editor.ItemDatabase.controller import ItemController
from Editor.Database.database import Database
from Editor.PeoplemonDatabase.Peoplemon import ValidMove,LearnMove

class PeoplemonController(ItemController):
    def __init__(self,dataBase):
        ItemController.__init__(self,dataBase)
        self.validController = MoveController(Database(ValidMove))
        self.learnController = MoveController(Database(LearnMove))


    def addObj(self):
        ItemController.addObj(self)
        self.changeMoves(self.cur_ind)

    def delObj(self):
        ItemController.delObj(self)
        self.changeMoves(self.cur_ind)

    def click(self,ind):
        if self.cur_ind == -1:
            return
        self.changeMoves(ind)
        ItemController.click(self,ind)


    def changeMoves(self,ind):
        print(self.model.dataObjs[self.cur_ind].validMoves)
        self.validController.model = self.model.dataObjs[ind].validMoves
        self.learnController.model = self.model.dataObjs[ind].learnMoves
        self.validController.load()
        self.learnController.load()

    def update(self,paramdict,options=list()):
        '''Updates the model and loads the view'''
        success = self.model.update(paramdict,[self.cur_ind]+options)
        if success is False:
            return False

    def loadPeoplemon(self,ind,params,options=list()):
        return self.model.load(params,[ind]+options)


class MoveController(ItemController):
    def __init__(self,database):
        ItemController.__init__(self,database)

    def apply(self):
        ItemController.apply(self)