from Editor.saveable.composite import Composite
from Editor.saveable.saveablechar import SaveableChar
from Editor.saveable.saveableInt import U8, U16
from Editor.saveable.saveableArray import array
from Editor.saveable.saveableString import SaveableString
from Editor.saveable.union import Union


class Talk(SaveableString):
    def __str__(self):
        return '<Talk> {}'.format(self.get())


class Option(Composite):
    line = SaveableString
    next = SaveableString

    def __str__(self):
        return 'Line: {}, Next: {}'.format(self.line.get(), self.next.get())


class Options(Composite):
    line = SaveableString
    options = array(Option)

    def __str__(self):
        return '<Option> Line: {}, Options: {}'.format(self.line.get(),
                                                       [option.line.get() for option in self.options])


class Give(Composite):
    is_item = U8
    money_or_id = U16

    def __str__(self):
        if self.is_item.get():
            return '<Give Item> ID: {}'.format(self.money_or_id)
        else:
            return '<Give Money> Amount: ${}'.format(self.money_or_id)


class Take(Composite):
    is_item = U8
    money_or_id = U16
    fail_line = SaveableString

    def __str__(self):
        if self.is_item.get():
            return '<Take Item> ID: {}, Fail: {}'.format(self.money_or_id, self.fail_line)
        else:
            return '<Take Money> Amount: ${}, Fail: {}'.format(self.money_or_id, self.fail_line)


class Jump(SaveableString):
    def __str__(self):
        return '<Jump To> {}'.format(self.get())


class Save(SaveableString):
    def __str__(self):
        return '<Save Value> {}'.format(self.get())


class CheckSaved(Composite):
    value = SaveableString
    fail_line = SaveableString

    def __str__(self):
        return '<Check Saved> Value: {}, Fail: {}'.format(self.value, self.fail_line)


class JumpPoint(SaveableString):
    def __str__(self):
        return '<Jump Point> {}'.format(self.get())


class CheckTalked(SaveableString):
    def __str__(self):
        return '<Check Talked> Fail: {}'.format(self.get())


class Run(SaveableString):
    def __str__(self):
        return '<Run Script> {}'.format(self.get())


class Line(Union):
    TYPE_MAP = {Talk: 't', Options: 'o', Give: 'g', Take: 'r', Jump: 'j',
                Save: 's', CheckSaved: 'c', JumpPoint: 'l', CheckTalked: 'w', Run: 'z'}

    talk = Talk
    option = Options
    give = Give
    take = Take
    jump = Jump
    save = Save
    check = CheckSaved
    point = JumpPoint
    talked = CheckTalked
    run = Run

    def to_byte_array(self):
        code = SaveableChar()
        code.set(Line.TYPE_MAP[self.get()])
        array = code.to_byte_array()
        array += self.__current__.to_byte_array()
        return array

    def load_in_place(self, byte_array):
        code = SaveableChar()
        code.load_in_place(byte_array)
        inv_map = {v: k for k, v in Line.TYPE_MAP.items()}
        if code.get() not in inv_map:
            raise ValueError('Incorrect Conversation type: ' + code.get())
        line_type = inv_map[code.get()]
        if line_type not in self.__revtypemap__:
            raise ValueError('Could not find correct type ' + code.get())
        self.set(line_type)
        self.__current__.load_in_place(byte_array)