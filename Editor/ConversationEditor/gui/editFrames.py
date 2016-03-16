import tkinter as tk
import tkinter.ttk as ttk

from abc import ABCMeta, abstractmethod

from Editor.guicomponents.entrylabel_ttk import EntryLabel
from Editor.guicomponents.listchoice_new import ListChoice

from Editor.guicomponents.integercheck import IntegerCheck


class BdFrame(ttk.Frame):
    __metaclass__ = ABCMeta

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        frm = ttk.Frame(self)
        frm.pack(expand=tk.YES, fill=tk.X, side=tk.BOTTOM)
        ttk.Separator(self).pack(side=tk.TOP, expand=tk.YES, fill=tk.X, pady=(6, 5), padx=(5, 5))
        ttk.Separator(self).pack(side=tk.BOTTOM, expand=tk.YES, fill=tk.X, pady=(16, 10), padx=(50, 50))
        ttk.Button(frm,
                   text='Confirm',
                   command=self.update,
                   width=15).pack(side=tk.BOTTOM, pady=(0, 10), expand=tk.YES)

    def update(self):
        self.update_line()
        self.controller.update()

    @abstractmethod
    def update_line(self):
        pass


class TalkEdit(BdFrame):
    def __init__(self, parent,  controller, line):
        BdFrame.__init__(self, parent, controller)
        self.talk_line = line
        self.line_var = tk.StringVar(self)
        self.line = EntryLabel(self, text='Display Line: ', entry_variable=self.line_var)
        self.line_var.set(self.talk_line['line'])

        self.line.pack(expand=tk.YES, fill=tk.X, padx=(20, 20))

    def update_line(self):
        self.talk_line.changeLine(self.line_var.get())


class OptionEdit(BdFrame):
    def __init__(self, parent,  controller, line):
        BdFrame.__init__(self, parent, controller)
        self.option_line = line
        self.talk_line = line
        self.line_var = tk.StringVar(self)
        self.check_var = tk.IntVar(self)

        self.line = EntryLabel(self, text='Display Line: ', entry_variable=self.line_var)
        self.option_list = ListChoice(self, delete_cmd=self.delete_option, height=5)
        self.value = EntryLabel(self, text='Line display')
        self.jump = EntryLabel(self, text='Jump to')

        self.line_var.set(self.talk_line['line'])
        for value, jump in self.talk_line.getOptions():
            self.option_list.addChoice(self.choice_string(value, jump))

        self.line.pack(expand=tk.YES, fill=tk.X, padx=(20, 20), pady=(0, 5))
        ttk.Checkbutton(self, text='Add Before (Otherwise at end)', variable=self.check_var).pack()
        self.option_list.pack(expand=tk.YES, fill=tk.BOTH, padx=(30, 30))
        self.value.pack(expand=tk.YES, fill=tk.X, padx=(30, 30))
        self.jump.pack()
        ttk.Button(self, text='Add', command=self.add,).pack(pady=(10, 0))

    @staticmethod
    def choice_string(value, jump):
        return 'Value: ' + str(value) + ' | Jump: ' + str(jump)

    def add(self):
        if not self.check_var.get():
            ind = -1
        else:
            ind = self.option_list.getSelection()
            top = self.option_list.get_top()
        self.option_list.insertChoice(ind, self.choice_string(self.value.get(), self.jump.get()))

        if not self.check_var.get():
            self.option_list.setPosition(1.0)
        else:
            self.option_list.set_top(top)

        print(ind)
        self.option_list.setSelection(ind)

    def update_line(self):
        self.option_line['line'] = self.line.get()
        self.option_line['options'].clear()
        for choice in self.option_list:
            value = choice.split('|')[0][7:-1]
            jump = choice.split('|')[1][7:]
            self.option_line.addOption('end', value, jump)


    def delete_option(self, index):
        self.option_list.delete(index)
        if index == len(self.option_list):
            index -= 1
        if index < 0:   # Choices now empty
            return
        self.option_list.setSelection(index)


class GiveItemEdit(BdFrame):
    def __init__(self, parent, controller, line):
        BdFrame.__init__(self, parent, controller)
        self.give_line = line
        self.id_var = tk.IntVar(self)
        self.id_var.set(self.give_line['id'])

        self.id = EntryLabel(self, text='Item ID: ', entry_variable=self.id_var, validate='key',
                             validatecommand=IntegerCheck(self, 'u16').vcmd)
        self.id.pack()

    def update_line(self):
        self.give_line.changeID(self.id_var.get())


class TakeItemEdit(BdFrame):
    def __init__(self, parent, controller, line):
        BdFrame.__init__(self, parent, controller)
        self.take_line = line

        self.id_var = tk.IntVar(self)
        self.fail_var = tk.StringVar(self)
        self.id_var.set(self.take_line['id'])
        self.fail_var.set(self.take_line['fail'])

        self.fail = EntryLabel(self, text='Fail Line: ', entry_variable=self.fail_var)
        self.id = EntryLabel(self, text='Item ID: ', entry_variable=self.id_var, validate='key',
                             validatecommand=IntegerCheck(self, 'u16').vcmd)
        self.fail.pack(expand=tk.YES, fill=tk.X, padx=(20, 20))
        self.id.pack()

    def update_line(self):
        self.take_line.changeID(self.id_var.get())
        self.take_line.changeFail(self.fail_var.get())


class GiveMoneyEdit(BdFrame):
    def __init__(self, parent, controller, line):
        BdFrame.__init__(self, parent, controller)
        self.give_line = line
        self.amount_var = tk.IntVar(self)
        self.amount_var.set(line['amount'])
        self.amount = EntryLabel(self, text='Amount: ', entry_variable=self.amount_var)
        self.amount.pack()

    def update_line(self):
        self.give_line.changeAmount(self.amount_var.get())


class TakeMoneyEdit(BdFrame):
    def __init__(self, parent, controller, line):
        BdFrame.__init__(self, parent, controller)
        self.take_line = line

        self.amount_var = tk.IntVar(self)
        self.fail_var = tk.StringVar(self)
        self.amount_var.set(line['amount'])
        self.fail_var.set(line['fail'])

        self.fail = EntryLabel(self, text='Fail Line: ', entry_variable=self.fail_var)
        self.amount = EntryLabel(self, text='Amount: ', validate='key', entry_variable=self.amount_var,
                                 validatecommand=IntegerCheck(self, 'u16').vcmd)
        self.fail.pack(expand=tk.YES, fill=tk.X, padx=(20, 20))
        self.amount.pack()

    def update_line(self):
        self.take_line.changeAmount(self.amount_var.get())
        self.take_line.changeFail(self.fail_var.get())


class JumpEdit(BdFrame):
    def __init__(self, parent, controller, line):
        BdFrame.__init__(self, parent, controller)
        self.jump_line = line
        self.name_var = tk.StringVar(self)
        self.name_var.set(line['name'])

        self.name = EntryLabel(self, text='Jump Name: ', entry_variable=self.name_var)
        self.name.pack(expand=tk.YES, fill=tk.X, padx=(20, 20))

    def update_line(self):
        self.jump_line.changeName(self.name_var.get())


class JumpPointEdit(BdFrame):
    def __init__(self, parent, controller, line):
        BdFrame.__init__(self, parent, controller)
        self.jump_line = line
        self.name_var = tk.StringVar(self)
        self.name_var.set(line['name'])

        self.name = EntryLabel(self, text='Jump Name: ', entry_variable=self.name_var)
        self.name.pack(expand=tk.YES, fill=tk.X, padx=(20, 20))

    def update_line(self):
        self.jump_line.changeName(self.name.get())


class SaveEdit(BdFrame):
    def __init__(self, parent, controller, line):
        BdFrame.__init__(self, parent, controller)
        self.save_line = line
        self.value_var = tk.StringVar(self)
        self.value_var.set(line['value'])

        self.value = EntryLabel(self, text='String Value: ', entry_variable=self.value_var)
        self.value.pack(expand=tk.YES, fill=tk.X, padx=(20, 20))

    def update_line(self):
        self.save_line.changeValue(self.value_var.get())


class CheckSaveEdit(BdFrame):
    def __init__(self, parent, controller, line):
        BdFrame.__init__(self, parent, controller)
        self.check_line = line
        self.fail_var = tk.StringVar(self)
        self.value_var = tk.StringVar(self)
        self.fail_var.set(line['fail'])
        self.value_var.set(line['value'])

        self.fail = EntryLabel(self, text='FailLine: ', entry_variable=self.fail_var)
        self.value = EntryLabel(self, text='String Value: ', entry_variable=self.value_var)
        self.value.pack(expand=tk.YES, fill=tk.X, padx=(20, 20))
        self.fail.pack(expand=tk.YES, fill=tk.X, padx=(20, 20))

    def update_line(self):
        self.check_line.changeValue(self.value_var.get())
        self.check_line.changeFail(self.fail_var.get())


class CheckTalkedEdit(BdFrame):
    def __init__(self, parent, controller, line):
        BdFrame.__init__(self, parent, controller)
        self.check_line = line
        self.fail_var = tk.StringVar(self)
        self.fail_var.set(line['fail'])

        self.fail = EntryLabel(self, text='Fail Line: ', entry_variable=self.fail_var)
        self.fail.pack(expand=tk.YES, fill=tk.X, padx=(20, 20))

    def update_line(self):
        self.check_line.changeFail(self.fail_var.get())


class RunScriptEdit(BdFrame):
    def __init__(self, parent, controller, line):
        BdFrame.__init__(self, parent, controller)
        self.check_line = line
        self.script_var = tk.StringVar(self)
        self.script_var.set(line['script'])

        self.fail = EntryLabel(self, text='Script Name: ', entry_variable=self.script_var)
        self.fail.pack(expand=tk.YES, fill=tk.X, padx=(20, 20))

    def update_line(self):
        self.check_line['script'] = (self.script_var.get())
