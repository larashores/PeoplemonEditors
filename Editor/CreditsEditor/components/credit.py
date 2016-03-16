__author__ = 'Vincent'

from Editor.Component import Component

from Editor.structreader import pack, unpack

class AllCredits(Component):
    def __init__(self):
        Component.__init__(self)
        self.credits = []

    def __iter__(self):
        for credit in self.credits:
            yield credit

    def __len__(self):
        return len(self.credits)

    def delete(self, ind):
        self.credits.pop(ind)

    def insertTextCredit(self, ind):
        self.credits.insert(ind, Credit('text'))

    def insertImageCredit(self, ind):
        self.credits.insert(ind, Credit('image'))

    def editTextCredit(self, ind, xPos, yBuf, text, red, green, blue, fontSize):
        credit = self.credits[ind]
        if type(credit.creditType) is not TextCredit:
            raise Exception('Bad Credit Type')
        credit.paramDict['xPos'] = xPos
        credit.paramDict['yBuf'] = yBuf
        credit.creditType.paramDict['text'] = text
        credit.creditType.paramDict['red'] = red
        credit.creditType.paramDict['green'] = green
        credit.creditType.paramDict['blue'] = blue
        credit.creditType.paramDict['fontSize'] = fontSize

    def editImageCredit(self, ind, xPos, yBuf, path):
        credit = self.credits[ind]
        if type(credit.creditType) is not ImageCredit:
            raise Exception('Bad Credit Type')
        credit.paramDict['xPos'] = xPos
        credit.paramDict['yBuf'] = yBuf
        credit.creditType.paramDict['path'] = path

    def loadTextCredit(self, ind):
        credit = self.credits[ind]
        if type(credit.creditType) is not TextCredit:
            raise Exception('Bad Credit Type')
        res = []
        res.extend([credit.paramDict['xPos'], credit.paramDict['yBuf']])
        for name in 'text', 'red', 'green', 'blue', 'fontSize':
            res.append(credit.creditType.paramDict[name])
        return res

    def loadImageCredit(self, ind):
        credit = self.credits[ind]
        if type(credit.creditType) is not ImageCredit:
            raise Exception('Bad Credit Type')
        res = []
        res.extend([credit.paramDict['xPos'], credit.paramDict['yBuf']])
        for name in ('path',):
            res.append(credit.creditType.paramDict[name])
        return res

    def getCreditType(self, ind):
        return self.credits[ind].type

    def fromByteArray(self, byteArray):
        data = byteArray
        credits = AllCredits()
        credit = Credit('text')

        num = unpack(data, 'u16')
        for _ in range(num):
            credits.credits.append(credit.fromByteArray(data))
        return credits

    def toByteArray(self):
        data = bytearray()
        pack(data, len(self.credits), 'u16')
        for credit in self.credits:
            data += credit.toByteArray()
        return data


class Credit(Component):
    def __init__(self, creditType):
        Component.__init__(self)
        self.addParam('type', 0)
        self.addParam('xPos', 0)
        self.addParam('yBuf', 0)
        self.type = creditType

        if creditType == 'text':
            self.paramDict['type'] = 1
            self.creditType = TextCredit()
        elif creditType == 'image':
            self.paramDict['type'] = 0
            self.creditType = ImageCredit()

    def __str__(self):
        return str(self.creditType)

    def fromByteArray(self, byteArray):
        data = byteArray

        type = unpack(data, 'u8')
        xPos = unpack(data, 'u16')
        yBuf = unpack(data, 'u16')

        if type == 1:
            credit = Credit('text')
        elif type == 0:
            credit = Credit('image')
        else:
            raise Exception('Bad type')
        credit.paramDict['xPos'] = xPos
        credit.paramDict['yBuf'] = yBuf
        credit.creditType = credit.creditType.fromByteArray(data)

        return credit


    def toByteArray(self):
        data = bytearray()
        pack(data, self.paramDict['type'], 'u8')
        pack(data, self.paramDict['xPos'], 'u16')
        pack(data, self.paramDict['yBuf'], 'u16')
        data += self.creditType.toByteArray()

        return data


class TextCredit(Component):
    def __init__(self):
        Component.__init__(self)
        self.addParam('text', '')
        self.addParam('red', 0)
        self.addParam('green', 0)
        self.addParam('blue', 0)
        self.addParam('fontSize', 0)

    def __str__(self):
        return 'Text Credit | ' + self.paramDict['text']

    def toByteArray(self):
        data = bytearray()
        pack(data, self.paramDict['text'], 'str')
        pack(data, self.paramDict['red'], 'u8')
        pack(data, self.paramDict['green'], 'u8')
        pack(data, self.paramDict['blue'], 'u8')
        pack(data, self.paramDict['fontSize'], 'u16')

        return data

    def fromByteArray(self, byteArray):
        data = byteArray
        credit = TextCredit()
        credit.paramDict['text'] = unpack(data, 'str')
        credit.paramDict['red'] = unpack(data, 'u8')
        credit.paramDict['green'] = unpack(data, 'u8')
        credit.paramDict['blue'] = unpack(data, 'u8')
        credit.paramDict['fontSize'] = unpack(data, 'u16')

        return credit


class ImageCredit(Component):
    def __init__(self):
        Component.__init__(self)
        self.addParam('path', '')

    def __str__(self):
        return 'Image Credit | ' + self.paramDict['path']

    def toByteArray(self):
        data = bytearray()
        pack(data, self.paramDict['path'], 'str')
        return data

    def fromByteArray(self, byteArray):
        data = byteArray
        credit = ImageCredit()
        credit.paramDict['path'] = unpack(data, 'str')
        return credit
