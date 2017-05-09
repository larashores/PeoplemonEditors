class IntegerCheck:
    def __init__(self, parent, intType):
        self.parent = parent
        if intType == 'u8':
            self.low = 0
            self.high = 256
        elif intType == 's8':
            self.low = -128
            self.high = 127
        elif intType == 'u16':
            self.low = 0
            self.high = 65535
        elif intType == 's16':
            self.low = -32768
            self.high = 32767
        elif intType == 'u32':
            self.low = 0
            self.high = 4294967295
        elif intType == 's32':
            self.low = -2147483648
            self.high = 2147483647
        else:
            raise Exception('Unknown type')
        self.vcmd = parent.register(self.inIntegerRange), '%d', '%P'

    def inIntegerRange(self, _type, afterText):
        """
        Validates an entry to make sure the correct text is being inputted
        :param type:        0 for deletion, 1 for insertion, -1 for focus in
        :param afterText:   The text that the entry will display if validated
        :return:
        """
        if _type == '0':
            return True
        elif _type == '1':
            try:
                num = int(afterText)
            except ValueError:
                if (self.low < 0) and (afterText == '-'):
                    return True
                else:
                    return False
            if (num >= self.low) and (num <= self.high):
                return True
        return False