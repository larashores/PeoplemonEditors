__author__ = 'Vincent'

import inspect

from Editor.Database.controller import Controller

class ItemController(Controller):
    def loadObj(self,ind):
        return self.model.load( ["id","name","desc"], [ind])
