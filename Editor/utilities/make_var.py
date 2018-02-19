import tkinter as tk


def make_combo_var(item, item_map, parent=None):
    inv_map = {v: k for k, v in item_map.items()}
    var = tk.StringVar(parent)

    def set_var(val):
        set_var.setting = True
        var.set(inv_map[val])
        set_var.setting = False
    set_var.setting = False

    def set_item(var_, i, op):
        if not set_var.setting:
            try:
                val = var.get()
                item.set(item_map[val])
            except ValueError:
                pass
    set_var(item.get())

    var.trace_variable('w', set_item)
    item.signal_changed.connect(set_var)
    return var


def make_int_var(item, parent=None):
    return _make_var(tk.IntVar(parent), item,)


def make_check_var(item, parent=None):
    return _make_var(tk.BooleanVar(parent), item)


def make_str_var(item, parent=None):
    return _make_var(tk.StringVar(parent), item)


def _make_var(var, item):
    var.set(item.get())

    def set_var(val):
        set_var.setting = True
        var.set(val)
        set_var.setting = False
    set_var.setting = False

    def set_item(var_, i, op):
        if not set_var.setting:
            try:
                val = var.get()
                item.set(val)
            except ValueError:
                pass

    var.trace_variable('w', set_item)
    item.signal_changed.connect(set_var)
    return var
