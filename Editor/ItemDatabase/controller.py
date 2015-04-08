__author__ = 'Vincent'

from Editor.Database.controller import Controller

class ItemController(Controller):
    def update(self,param):
        '''Updates the model and loads the view'''
        success = self.model.update({'id':param[0],'name':param[1],'desc':param[2]},[self.cur_ind])
        if success is False:
            return False
        self.load()

    def loadObj(self,ind):
        return self.model.dataObjs[ind].load( ["id","name","desc"] )