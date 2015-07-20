__author__ = 'Vincent'

from Editor.Component import Component
from Editor.structreader import pack, unpack

class Item(Component):
    def __init__(self):
        Component.__init__(self)
        self.addParam('id',0)
        self.addParam('name','')
        self.addParam('desc','')
        self.addParam('sellPrice',0)

    def __str__(self):
        return 'id: {} | name: {} | desc: {}'.format(self.paramDict['id'],self.paramDict['name'],self.paramDict['desc'])

    def toByteArray(self):
        data = bytearray()
        pack(data,self.paramDict['id'],'u16')
        pack(data,self.paramDict['name'],'str')
        pack(data,self.paramDict['desc'],'str')
        pack(data,self.paramDict['sellPrice'],'u32')
        return data

    def fromByteArray(self,byteArray):
        item = Item()
        id = unpack(byteArray,'u16')
        item.update({'id': id})
        item.update({'name': unpack(byteArray,'str')})
        item.update({'desc': unpack(byteArray,'str')})
        item.update({'sellPrice': unpack(byteArray,'u32')})
        return item


if __name__ == '__main__':

    from Editor.database import Database

    db = Database(Item)
    db.add()
    db.add()
    db.add()
    db.update( [0,5,'Vince','yay'] )
    db.update( [1,10,'Chris','yoo'] )
    db.update( [2,15,'Poop','too'] )
    print(db.toByteArray())