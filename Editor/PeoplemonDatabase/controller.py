__author__ = 'Vincent'

from Editor.ItemDatabase.controller import ItemController

class PeoplemonController(ItemController):
    def update(self,paramdict,options=list()):
        '''Updates the model and loads the view'''
        print(paramdict)
        success = self.model.update(paramdict,[self.cur_ind]+options)
        if success is False:
            return False

    def loadPeoplemon(self,ind,params,options=list()):
        return self.model.load(params,[ind]+options)