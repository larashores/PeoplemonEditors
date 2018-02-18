from Editor.saveable.composite import Composite
from Editor.saveable.saveableInt import saveable_int
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
    is_item = saveable_int('u8')
    money_or_id = saveable_int('u16')

    def __str__(self):
        if self.is_item.get():
            return '<Give Item> ID: {}'.format(self.money_or_id)
        else:
            return '<Give Money> Amount: ${}'.format(self.money_or_id)


class Take(Composite):
    is_item = saveable_int('u8')
    money_or_id = saveable_int('u16')
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
