__author__ = 'Vincent'

from Editor.Database.controller import Controller

class ItemController(Controller):
    def update(self,param):
        '''Updates the model and loads the view'''
        success = self.model.update( [self.cur_ind] + param)
        if success is False:
            return False
        self.load()

