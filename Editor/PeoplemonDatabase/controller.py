__author__ = 'Vincent'

from Editor.ItemDatabase.controller import ItemController

class PeoplemonController(ItemController):
    def update(self,param,options=list()):
        '''Updates the model and loads the view'''
        success = self.model.update(param,[self.cur_ind]+options)
        if success is False:
            return False

    def loadPeoplemon(self,ind,params,options=list()):
        return self.model.load(params,[ind]+options)