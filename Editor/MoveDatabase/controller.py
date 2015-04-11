__author__ = 'Vincent'

from Editor.Database.controller import Controller
from Editor.ItemDatabase.controller import ItemController


class MoveController(ItemController):
    def loadAttribs(self,ind,params,options=list()):
        return self.model.load(params,[ind]+options)