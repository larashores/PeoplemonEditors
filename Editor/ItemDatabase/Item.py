__author__ = 'Vincent'

from Editor.Component import Component
from Editor.structreader import pack, unpack

class Item(Component):
    def __init__(self):
        self.id = 0
        self.name = ''
        self.desc = ''

    def __str__(self):
        return 'id: {} | name: {} | desc: {}'.format(self.id,self.name,self.desc)

    def toByteArray(self):
        data = bytearray()
        pack(data,self.id,'u16')
        pack(data,self.name,'str')
        pack(data,self.desc,'str')
        return data

    def fromByteArray(self,byteArray):
        item = Item()
        item.id = unpack(byteArray,'u16')
        item.name = unpack(byteArray,'str')
        item.desc = unpack(byteArray,'str')
        return item

    def load(self):
        return [self.id,self.name,self.desc]

    def update(self,param):
        if len(param) > 3:
            raise Exception("Too many paramaters")
        else:
            self.id = param[0]
            self.name = param[1]
            self.desc = param[2]

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