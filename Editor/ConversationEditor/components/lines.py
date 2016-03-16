"""
#-------------------------------------------------------------------------------
# Name:        module1

# Author:      Vincent
#
# Date Created:     01/25/2015
# Date Modified:    01/25/2015
#-------------------------------------------------------------------------------

Purpose:

"""

from Editor.Component_new import Component
from structreader import pack, unpack

from abc import ABCMeta, abstractmethod


class BaseLine(Component):
    __metaclass__ = ABCMeta

    def __init__(self):
        Component.__init__(self)

    # --------------------------Overridden Methods-----------------------
    def toByteArray(self):
        data = bytearray()
        pack(data, self.get_code(), 'chr')
        return data

    @staticmethod
    def fromByteArray(byteArray):
        classes = BaseLine.__subclasses__()
        codes = dict(zip(map(lambda line: line.get_code(), classes), classes))

        code = unpack(byteArray, 'chr')
        Line = codes[code]
        return Line.fromByteArray(byteArray)

    # ---------------------------Abstract Methods------------------------
    @staticmethod
    @abstractmethod
    def get_code():
        return '\0'


class TalkLine(BaseLine):
    """
    Line used for the NPC to say something
    """

    def __init__(self, line=''):
        BaseLine.__init__(self)
        self.addParam('line', line)

    def __str__(self):
        return '<Talk> ' + 'Line: {}'.format(self['line'])

    def changeLine(self, line):
        self['line'] = line

    # --------------------------Overridden Methods-----------------------
    def toByteArray(self):
        data = BaseLine.toByteArray(self)
        pack(data, self['line'], 'str')
        return data

    @staticmethod
    def fromByteArray(byteArray):
        string = unpack(byteArray, 'str')
        return TalkLine(string)

    @staticmethod
    def get_code():
        return 't'


class OptionLine(BaseLine):
    """
    Line used for giving options to the player after displaying a line, such as
    asking a yes or no question.
    """
    def __init__(self, line=''):
        BaseLine.__init__(self)
        self.addParam('line', line)
        self.addParam('options', [])

    def __str__(self):
        """
        Returns first 27 characters of line
        """
        return '<Option> ' + 'Line: {} | Options: {}'.format(self['line'], self['options'])

    def addOption(self, ind, line, jump):
        """
        Purpose: Adds an option to the list at a given index
        Inputs:
            ind:      Index to add option at ('end' adds to end)
            choice:   The option string
            jump:     (str) The jump point to go to
        """
        if ind == 'end':
            self['options'].append((line, jump))
        else:
            self['options'].insert(ind, (line, jump))

    def delOption(self, ind):
        """
        Purpose: Deletes an option from the list by its index
        Inputs:
            ind:      The option's index
        """
        self['options'].pop(ind)

    def getLine(self):
        """
        Gets the prompting line
        """
        return self['line']

    def getOptions(self):
        """
        Yields each (line,jump.name) pair
        """
        for line, jump in self['options']:
            yield (line, jump)

    # --------------------------Overridden Methods-----------------------
    def toByteArray(self):
        data = BaseLine.toByteArray(self)
        pack(data, self['line'], 'str')
        pack(data, len(self['options']), 'u16')
        for option in self['options']:
            pack(data, option[0], 'str')         # Line
            pack(data, option[1], 'str')         # Jump
        return data

    @staticmethod
    def fromByteArray(byteArray):
        string = unpack(byteArray, 'str')
        line = OptionLine(string)
        numOptions = unpack(byteArray, 'u16')
        for num in range(numOptions):
            choice = unpack(byteArray, 'str')
            jump = unpack(byteArray, 'str')
            line.addOption('end', choice, jump)
        return line

    @staticmethod
    def get_code():
        return 'o'


class GiveLine(BaseLine):
    """
    Line used for giving items or money
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        Component.__init__(self)

    # --------------------------Overridden Methods-----------------------
    def toByteArray(self):
        data = BaseLine.toByteArray(self)
        pack(data, self.is_item(), 'u8')
        return data

    @staticmethod
    def fromByteArray(byteArray):
        is_item = unpack(byteArray, 'u8')
        if is_item:
            return GiveItemLine.fromByteArray(byteArray)
        else:
            return GiveMoneyLine.fromByteArray(byteArray)

    @staticmethod
    def get_code():
        return 'g'

    # ---------------------------Abstract Methods------------------------
    @staticmethod
    @abstractmethod
    def is_item():
        pass


class GiveMoneyLine(GiveLine):
    """
    Line used for giving an item or money
    """

    def __init__(self, amount=0):
        super().__init__()
        self.addParam('amount', amount)

    def __str__(self):
        return '<Give Money> ' + 'Amount: {}'.format(self['amount'])

    @staticmethod
    def fromByteArray(byteArray):
        amount = unpack(byteArray, 'u16')
        return GiveMoneyLine(amount)

    def changeAmount(self, amount):
        """
        Purpose: Changes the amount of money given
        Inputs:
            amount:     Amount of money to change to
        """
        self['amount'] = amount

    def getAmount(self):
        """
        Purpose: Gets amount of money to be taken
        """
        return self['amount']

    # --------------------------Overridden Methods-----------------------
    def toByteArray(self):
        data = GiveLine.toByteArray(self)
        pack(data, self['amount'], 'u16')
        return data

    @staticmethod
    def is_item():
        return 0


class GiveItemLine(GiveLine):
    """
    Line used for giving an item
    """

    def __init__(self, _id=0):
        super().__init__()
        self.paramDict['id'] = _id

    def __str__(self):
        return '<Give Item> ' + 'ID: {}'.format(self['id'])

    def changeID(self, _id):
        """
        Purpose: Changes the id of the item given
        Inputs:
            id:     ID to change to
        """
        self['id'] = _id

    def getID(self):
        """
        Purpose: Gets id of item to be given
        """
        return self['id']

    # --------------------------Overridden Methods-----------------------
    def toByteArray(self):
        data = GiveLine.toByteArray(self)
        pack(data, self['id'], 'u16')
        return data

    @staticmethod
    def fromByteArray(byteArray):
        _id = unpack(byteArray, 'u16')
        return GiveItemLine(_id)

    @staticmethod
    def is_item():
        return 1


class TakeLine(BaseLine):
    """
    Line used for taking items or money
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        Component.__init__(self)

    # --------------------------Overridden Methods-----------------------
    def toByteArray(self):
        data = BaseLine.toByteArray(self)
        pack(data, self.is_item(), 'u8')
        return data

    @staticmethod
    def fromByteArray(byteArray):
        is_item = unpack(byteArray, 'u8')
        if is_item:
            return TakeItemLine.fromByteArray(byteArray)
        else:
            return TakeMoneyLine.fromByteArray(byteArray)

    @staticmethod
    def get_code():
        return 'r'

    # ---------------------------Abstract Methods------------------------
    @staticmethod
    @abstractmethod
    def is_item():
        pass


class TakeMoneyLine(TakeLine):
    """
    Line used for taking money, will jump to fail_line if not enough money can be
    taken
    """

    def __init__(self, amount=0, fail_line=''):
        TakeLine.__init__(self)
        self.addParam('amount', amount)
        self.addParam('fail', fail_line)

    def __str__(self):
        return '<Take Money> ' + 'Amount: {} | Fail Line: {}'.format(self['amount'], self['fail'])

    def changeAmount(self, amount):
        """
        Purpose: Changes the amount of money taken
        Inputs:
            amount:     Amount to change to
        """

        self['amount'] = amount

    def changeFail(self, jump_name):
        """
        Purpose: Changes the line to go to when failed
        Inputs:     JumpPoint point ot go to
        """

        self['fail'] = jump_name

    def getAmount(self):
        """
        Purpose: Gets amount of money to be taken
        """
        return self['amount']

    def getFail(self):
        """
        Gets line to go to when take fails
        """
        return self['fail']

    # --------------------------Overridden Methods-----------------------
    def toByteArray(self):
        data = TakeLine.toByteArray(self)
        pack(data, self['amount'], 'u16')
        pack(data, self['fail'], 'str')
        return data

    @staticmethod
    def fromByteArray(byteArray):
        amount = unpack(byteArray, 'u16')
        jump = unpack(byteArray, 'str')
        return TakeMoneyLine(amount, jump)

    @staticmethod
    def is_item():
        return 0


class TakeItemLine(TakeLine):
    """
    Line used for taking an item, will jump to fail_line if the item can't be
    taken
    """

    def __init__(self, _id=0, fail_line=''):
        TakeLine.__init__(self)
        self.addParam('id', _id)
        self.addParam('fail', fail_line)

    def __str__(self):
        return '<Take Item> ' + 'ID: {} | Fail: {}'.format(self['id'], self['fail'])

    def changeID(self, _id):
        """
        Purpose: Changes the id of the item taken
        Inputs:
            id:     ID to change to
        """
        self['id'] = _id

    def changeFail(self, jump_name):
        """
        Purpose: Changes the line to go to when failed
        Inputs:     Jump point ot go to
        """
        self['fail'] = jump_name

    def getID(self):
        """
        Purpose: Gets id of item to be taken
        """
        return self['id']

    def getFail(self):
        """
        Gets line to go to when take fails
        """
        return self['fail']

    # --------------------------Overridden Methods-----------------------
    def toByteArray(self):
        data = TakeLine.toByteArray(self)
        pack(data, self['id'], 'u16')
        pack(data, self['fail'], 'str')
        return data

    @staticmethod
    def fromByteArray(byteArray):
        _id = unpack(byteArray, 'u16')
        jump = unpack(byteArray, 'str')
        return TakeItemLine(_id, jump)

    @staticmethod
    def is_item():
        return 1


class Jump(BaseLine):
    """
    Line used to jump to somewhere else
    """

    def __init__(self, jump_name=''):
        BaseLine.__init__(self)
        self.addParam('name', jump_name)

    def __str__(self):
        return '<Jump> ' + 'Location: {}'.format(self['name'])

    def changeName(self, jump_name):
        """
        Purpose: Changes the jump point to go to
        Inputs:
            name:   Jump point to go to
        """
        self['name'] = jump_name

    def getName(self):
        """
        Purpose: Gets name of the jump point to go to
        """
        return self['name']

    # --------------------------Overridden Methods-----------------------
    def toByteArray(self):
        data = BaseLine.toByteArray(self)
        pack(data, self['name'], 'str')
        return data

    @staticmethod
    def fromByteArray(byteArray):
        name = unpack(byteArray, 'str')
        return Jump(name)

    @staticmethod
    def get_code():
        return 'j'


class JumpPoint(BaseLine):

    def __init__(self, name=''):
        BaseLine.__init__(self)
        self.addParam('name', name)

    def __str__(self):
        return '<Jump Point> ' + 'Label: {}'.format(self['name'])

    def changeName(self, name):
        """
        Purpose: Changes the jump point's name
        Inputs:
            name:   Jump point name
        """
        self['name'] = name

    def getName(self):
        """
        Purpose: Gets name of the jump point
        """
        return self['name']

    # --------------------------Overridden Methods-----------------------
    def toByteArray(self):
        data = BaseLine.toByteArray(self)
        pack(data, self['name'], 'str')
        return data

    @staticmethod
    def fromByteArray(byteArray):
        name = unpack(byteArray, 'str')
        return JumpPoint(name)

    @staticmethod
    def get_code():
        return 'l'


class Save(BaseLine):
    """
    Line used for saving a value, idk why
    """
    def __init__(self, value=''):
        BaseLine.__init__(self)
        self.addParam('value', value)

    def __str__(self):
        return '<Save> ' + 'Value: {}'.format(self['value'])

    def changeValue(self, value):
        """
        Purpose: Changes the value to be saved
        Inputs:
            value:  String value to be saved
        """
        self['value'] = value

    def getValue(self):
        """
        Purpose: Gets value to be saved
        """
        return self['value']

    # --------------------------Overridden Methods-----------------------
    def toByteArray(self):
        data = BaseLine.toByteArray(self)
        pack(data, self['value'], 'str')
        return data

    @staticmethod
    def fromByteArray(byteArray):
        string = unpack(byteArray, 'str')
        return Save(string)

    @staticmethod
    def get_code():
        return 's'


class CheckSave(BaseLine):
    """
    Line used for checking if a value is saved, goes to fail_line if it is not
    """

    def __init__(self, value='', fail_line=''):
        BaseLine.__init__(self)
        self.addParam('value', value)
        self.addParam('fail', fail_line)

    def __str__(self):
        return '<Check Saved> ' + 'Value: {} | Fail: {}'.format(self['value'], self['fail'])

    def changeValue(self, value):
        """
        Purpose: Changes value to search for
        Inputs:
            value:   String value to search for
        """
        self['value'] = value

    def changeFail(self, jump_name):
        """
        Purpose: Changes jump point to go to when failed
        Inputs:
            jump:   Jump point to go to
        """
        self['fail'] = jump_name

    def getValue(self):
        """
        Purpose: Gets value to check
        """
        return self['value']

    def getFail(self):
        return self['fail']

    # --------------------------Overridden Methods-----------------------
    def toByteArray(self):
        data = BaseLine.toByteArray(self)
        pack(data, self['value'], 'str')
        pack(data, self['fail'], 'str')
        return data

    @staticmethod
    def fromByteArray(byteArray):
        value = unpack(byteArray, 'str')
        fail = unpack(byteArray, 'str')
        return CheckSave(value, fail)

    @staticmethod
    def get_code():
        return 'c'


class CheckTalked(BaseLine):
    """
    Line used for checking if player has been talked to
    """

    def __init__(self, fail_line=''):
        BaseLine.__init__(self)
        self.addParam('fail', fail_line)

    def __str__(self):
        return '<Check Talked> ' + 'Fail: {}'.format(self['fail'])

    def changeFail(self, jump_name):
        """
        Purpose: Changes jump point to go to when failed
        Inputs:
            jump:   Jump point to go to
        """
        self['fail'] = jump_name

    def getFail(self):
        return self['fail']

    # --------------------------Overridden Methods-----------------------
    def toByteArray(self):
        data = BaseLine.toByteArray(self)
        pack(data, self['fail'], 'str')
        return data

    @staticmethod
    def fromByteArray(byteArray):
        fail_line = unpack(byteArray, 'str')
        return CheckTalked(fail_line)

    @staticmethod
    def get_code():
        return 'w'


class ScriptLine(BaseLine):
    """
    Line used for running a script
    """

    def __init__(self, script=''):
        BaseLine.__init__(self)
        self.addParam('script', script)

    def __str__(self):
        return '<Run Script> ' + 'Name: {}'.format(self['script'])

    # --------------------------Overridden Methods-----------------------
    def toByteArray(self):
        data = BaseLine.toByteArray(self)
        pack(data, self['script'], 'str')
        return data

    @staticmethod
    def fromByteArray(byteArray):
        script = unpack(byteArray, 'str')
        return ScriptLine(script)

    @staticmethod
    def get_code():
        return 'z'
