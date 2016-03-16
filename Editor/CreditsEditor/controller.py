__author__ = 'Vincent'

from CreditsEditor.components.credit import AllCredits


class Controller:
    def __init__(self):
        self.credits = AllCredits()
        self.loadFunc = lambda: None

    def addTextCredit(self, ind):
        self.credits.insertTextCredit(ind)

    def addImageCredit(self, ind):
        self.credits.insertImageCredit(ind)

    def editTextCredit(self, ind, xPos, yBuf,text, red, green, blue, fontSize):
        self.credits.editTextCredit(ind, xPos, yBuf, text, red, green, blue, fontSize)

    def editImageCredit(self, ind, xPos, yBuf, path):
        self.credits.editImageCredit(ind, xPos, yBuf, path)

    def loadTextCredit(self, ind):
        return self.credits.loadTextCredit(ind)

    def loadImageCredit(self, ind):
        return self.credits.loadImageCredit(ind)

    def getCreditType(self, ind):
        return self.credits.getCreditType(ind)

    def getStrings(self):
        strings = []
        for credit in self.credits:
            strings.append(str(credit))
        return strings

    def getNumCredits(self):
        return len(self.credits)

    def delete(self, ind):
        self.credits.delete(ind)

    def saveToFile(self, path):
        data = self.credits.toByteArray()
        file = open(path, 'wb')
        file.write(data)
        file.close()

    def loadFromFile(self,path):
        file = open(path, 'rb')
        data = bytearray(file.read())
        file.close()

        credits = self.credits.fromByteArray(data)
        self.credits = credits
        self.loadFunc()
