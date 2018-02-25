import tkinter as tk
import tkinter.ttk as ttk

from Editor.ConversationEditor.edit_widgets import *
from Editor.ConversationEditor.saveables import *
from Editor.guicomponents.widgetgrid import WidgetGrid
from Editor.guicomponents.multiwidget import MultiWidget
from Editor.guicomponents.listchoice import ListChoice
from Editor.utilities.addbuttonconnector import AddButtonConnector
from Editor.utilities.arrayconnector import ArrayConnector
from Editor.utilities.make_var import make_str_var, make_int_var


class NoSelectionWidget(ttk.Frame):
    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent)
        ttk.Label(self, text='No Selection').pack()


class ConversationEditorGUI(ttk.Frame):
    BUTTONS = (('Talk', Talk, TalkEdit),
               ('Option', Options, OptionEdit),
               ('Give Item', Give, GiveItemEdit),
               ('Take Item', Take, TakeItemEdit),
               ('Jump To', Jump, JumpEdit),
               ('Jump Point', JumpPoint, JumpPointEdit),
               ('Give Money', Give, GiveMoneyEdit),
               ('Take Money', Take, TakeMoneyEdit),
               ('Save String', Save, SaveEdit),
               ('Check String', CheckSaved, CheckSavedEdit),
               ('Check Talked', CheckTalked, CheckTalkedEdit),
               ('Run Script', Run, RunScriptEdit))

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.check_var = tk.BooleanVar()
        self.button_map = {}

        left_frm = ttk.Frame(self)
        title = ttk.Label(left_frm, text='Conversation Editor', style='Title.TLabel')
        self.button_grid = WidgetGrid(left_frm, 4)
        for label, saveable_type, widget in self.BUTTONS:
            button = self.button_grid.add_widget(ttk.Button, text=label)
            self.button_map[button] = (saveable_type, widget)
        line_label = ttk.Label(left_frm, text='Lines', style='Subtitle.TLabel')
        self.lines = ListChoice(left_frm)
        sep = ttk.Separator(self, orient=tk.VERTICAL)
        edit_label = ttk.Label(self, text='Line Editor', style='Subtitle.TLabel')
        self.editor_widget = MultiWidget(self)

        left_frm.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        title.pack()
        self.button_grid.pack()
        line_label.pack()
        self.lines.pack(expand=tk.YES, fill=tk.BOTH)
        sep.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        edit_label.pack()
        self.editor_widget.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        self.change_editor_widget(NoSelectionWidget)

    def change_editor_widget(self, widget):
        self.editor_widget.change_widget(widget)
        self.editor_widget.pack_forget()
        if widget in (TalkEdit, OptionEdit, TakeItemEdit, TakeMoneyEdit,
                      CheckSavedEdit, CheckTalkedEdit, RunScriptEdit):
            expand = tk.YES
        else:
            expand = tk.NO
        self.editor_widget.pack(side=tk.LEFT, expand=expand, fill=tk.BOTH)


class ConversationEditor:
    def __init__(self, parent=None):
        self.gui = ConversationEditorGUI(parent)
        self.conversations = array(Line)()
        self.main_saveable = self.conversations

        self.option_connector = None
        self.array_connector = ArrayConnector(self.conversations, self.gui.lines, None)
        self.add_connector = AddButtonConnector(self.conversations, self.gui.lines, self.gui.button_map)
        self.array_connector.bind_move()

        self.add_connector.signal_about_to_add.connect(self.on_line_about_to_add)
        self.gui.lines.signal_select.connect(self.line_selected)
        self.conversations.signal_remove.connect(self.on_delete)

    def line_selected(self, ind):
        line = self.array_connector.cur_selection
        line_type = line.get()

        simple_map = {Talk: (TalkEdit, line.talk),
                      Options: (OptionEdit, line.option.line if line.option else None),
                      Jump: (JumpEdit, line.jump),
                      Save: (SaveEdit, line.save),
                      JumpPoint: (JumpPointEdit, line.point),
                      CheckTalked: (CheckTalkedEdit, line.talked),
                      CheckSaved: (CheckSavedEdit, line.check.value if line.check else None),
                      Run: (RunScriptEdit, line.run)}
        self.array_connector.clear_editing_widgets()
        if line_type in simple_map:
            widget, string = simple_map[line_type]
            self.gui.change_editor_widget(widget)
            self.gui.editor_widget.current_widget.label.entry.config(textvariable=make_str_var(string))
        if line_type == Give:
            self.gui.change_editor_widget(GiveItemEdit if line.give.is_item else GiveMoneyEdit)
            self.gui.editor_widget.current_widget.label.entry.config(textvariable=make_int_var(line.give.money_or_id))
        elif line_type == Take:
            self.gui.change_editor_widget(TakeItemEdit if line.take.is_item else TakeMoneyEdit)
            self.gui.editor_widget.current_widget.label.entry.config(textvariable=make_int_var(line.take.money_or_id))
            self.gui.editor_widget.current_widget.fail_line.entry.config(textvariable=make_str_var(line.take.fail_line))
        elif line_type == CheckSaved:
            self.gui.editor_widget.current_widget.fail_line.entry.config(
                textvariable=make_str_var(line.check.fail_line))
        elif line_type == Options:
            self.setup_option(line)

        self.array_connector.add_editing_widgets(self.gui.editor_widget.current_widget)

    def setup_option(self, line):
        widget = self.gui.editor_widget.current_widget
        if self.option_connector:
            self.option_connector.clear_editing_widgets()
            self.option_connector.disconnect()
        self.option_connector = ArrayConnector(line.option.options, widget.options, widget.add_option,
                                               widget.option_display, widget.jump)
        self.option_connector.bind_move()
        widget.options.signal_select.connect(self.option_selected)

    def option_selected(self, ind):
        if ind is None:
            return
        widget = self.gui.editor_widget.current_widget
        option = self.array_connector.cur_selection.option.options[ind]
        widget.option_display.entry.configure(textvariable=make_str_var(option.line))
        widget.jump.entry.configure(textvariable=make_str_var(option.next))

    def on_delete(self, ind, val):
        if not len(self.conversations):
            self.array_connector.clear_editing_widgets()
            self.gui.change_editor_widget(NoSelectionWidget)

    @staticmethod
    def on_line_about_to_add(line, type_tup):
        saveable_type, widget_type = type_tup
        line.set(saveable_type)
        if widget_type == GiveItemEdit:
            line.give.is_item = 1
        elif widget_type == TakeItemEdit:
            line.is_item = 1

    def pack(self, **kwargs):
        self.gui.pack(**kwargs)


if __name__ == '__main__':
    root = tk.Tk()
    editor = ConversationEditor(root)
    editor.pack(expand=tk.YES, fill=tk.BOTH, padx=10, pady=(5, 10))
    root.mainloop()

