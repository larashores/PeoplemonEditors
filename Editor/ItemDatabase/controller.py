__author__ = 'Vincent'

import inspect

from Editor.Database.controller import Controller

class ItemController(Controller):
    def update(self,paramdict,options=list()):
        '''Updates the model and loads the view'''
        success = self.model.update(paramdict,[self.cur_ind])
        if success is False:
            return False

    def loadObj(self,ind):
        return self.model.load( ["id","name","desc"], [ind])

    def loadFromFile(self,path):
        Controller.loadFromFile(self,path)
        self.load()