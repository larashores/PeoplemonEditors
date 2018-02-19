import tkinter as tk


def intValidate(entry_widget, limits=(None, None)):
    """
    Validates an entry_widget so that only integers within a specified range may be entered

    :param entry_widget: The tkinter.Entry widget to validate
    :param limits: The limits of the integer. It may be given as a (min, max) tuple or a
                   C-Type specifying whether it is signed and how many bits is is. Thus it may be
                   u8, s8, u16, s16, u32, or s32

    :return:       None
    """
    if type(limits) == str:
        intType = limits
        if intType == 'u8':
            limits = [0, 256]
        elif intType == 's8':
            limits = [-128, 127]
        elif intType == 'u16':
            limits = [0, 65535]
        elif intType == 's16':
            limits = [-32768, 32767]
        elif intType == 'u32':
            limits = [0, 4294967295]
        elif intType == 's32':
            limits = [-2147483648, 2147483647]
        else:
            raise Exception('Unknown type')
    num_str = entry_widget.get()
    current = None if (not _isInt(num_str)) else int(num_str)
    check = _NumberCheck(entry_widget, limits[0], limits[1], current=current)
    entry_widget.config(validate='all')
    entry_widget.config(validatecommand=check.vcmd)
    entry_widget.bind('<FocusOut>', lambda event: _validate(entry_widget, check))
    _validate(entry_widget, check)


def _isInt(num_str):
    """
    Returns whether or not a given string is an integer

    :param num_str: The string to test

    :return: Whether or not the string is an integer
    """
    try:
        num = int(num_str)
        return True
    except:
        return False


def _validate(entry, numCheck):
    """
    Validates an entry so if there is invalid text in it it will be replaced by the last valid text

    :param entry: The entry widget
    :param numCheck: The NumberCheck instance that keeps track of the last valid number

    :return:    None
    """
    try:
        int(entry.get())
    except:
        entry.delete(0, tk.END)
        entry.insert(0, str(numCheck.last_valid))


class _NumberCheck:
    """
    Class used for validating entry widgets, self.vcmd is provided as the validatecommand
    """

    def __init__(self, parent, min, max, current):
        self.parent = parent
        self.low = min
        self.high = max
        self.vcmd = parent.register(self.inIntegerRange), '%d', '%P'

        if _NumberCheck.inRange(0, min, max):
            self.last_valid = 0
        else:
            self.last_valid = min
        if current is not None:
            self.last_valid = current

    def inIntegerRange(self, _type, afterText):
        """
        Validates an entry to make sure the correct text is being inputted
        :param type:        0 for deletion, 1 for insertion, -1 for focus in
        :param afterText:   The text that the entry will display if validated
        :return:
        """

        if _type == '-1':
            if _isInt(afterText):
                self.last_valid = int(afterText)

        # Delete Action, always okay, if valid number save it
        if _type == '0':
            try:
                num = int(afterText)
                self.last_valid = num
            except:
                pass
            return True

        # Insert Action, okay based on ranges, if valid save num
        elif _type == '1':
            try:
                num = int(afterText)
            except ValueError:
                if self.canBeNegative() and afterText == '-':
                    return True
                return False
            if self.isValidRange(num):
                self.last_valid = num
                return True
            return False
        return False

    def canBeNegative(self):
        """
        Tests whether this given entry widget can have a negative number

        :return: Whether or not the entry can have a negative number
        """
        return (self.low is None) or (self.low < 0)

    def isValidRange(self, num):
        """
        Tests whether the given number is valid for this entry widgets range

        :param num: The number to range test

        :return: Whether or not the number is in range
        """
        return _NumberCheck.inRange(num, self.low, self.high)

    @staticmethod
    def inRange(num, low, high):
        """
        Tests whether or not a number is within a specified range inclusive

        :param num: The number to test if its in the range
        :param low: The minimum of the range
        :param high: The maximum of the range

        :return: Whether or not the number is in the range
        """
        if (low is not None) and (num < low):
            return False
        if (high is not None) and (num > high):
            return False
        return True
