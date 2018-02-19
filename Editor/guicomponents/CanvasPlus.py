import tkinter as tk
import logging


class CanvasPlus:
    def __init__(self, parent, *args, **kwargs):
        self.canvas = tk.Canvas(parent, *args, **kwargs)
        self.references = {}
        self._ids_to_reference = {}
        self.used_levels = set()

    def __getattr__(self, item):
        return getattr(self.canvas, item)

    def find_overlapping_references(self, x1, y1, x2, y2):
        return [self._ids_to_reference[id_] for id_ in self.canvas.find_overlapping(x1, y1, x2, y2)
                if id_ in self._ids_to_reference]

    def create_oval(self, *args, reference=None, level=None, **kwargs):
        return self._create_item(self.canvas.create_oval, reference, level, *args, **kwargs)

    def create_line(self, *args, reference=None, level=None, **kwargs):
        return self._create_item(self.canvas.create_line, reference, level, *args, **kwargs)

    def create_image(self, *args, reference=None, level=None, **kwargs):
        return self._create_item(self.canvas.create_image, reference, level, *args, **kwargs)

    def delete(self, reference):
        if reference in self.references:
            for _tag in self.references[reference]:
                self.canvas.delete(_tag)
                if _tag in self._ids_to_reference:
                    del self._ids_to_reference[_tag]
        else:
            if reference in self._ids_to_reference:
                del self._ids_to_reference[reference]
            self.canvas.delete(reference)

    def _create_item(self, create_func, reference, level, *args, **kwargs):
        _id = create_func(*args, **kwargs)
        if reference is not None:
            self._add_reference(reference, _id)
            self._ids_to_reference[_id] = reference
        if level is not None:
            higher_levels = [_level for _level in self.used_levels if _level > level]
            tag_str = ''
            for higher_level in higher_levels:
                if tag_str != '':
                    tag_str += '||'
                tag_str += '__level__-{}'.format(higher_level)
            self.canvas.tag_raise(tag_str, _id)
            if level not in self.used_levels:
                self.used_levels.add(level)
            self.canvas.addtag('__level__-{}'.format(level), 'withtag', _id)

        return _id

    def _add_reference(self, reference, _id):
        if reference not in self.references:
            self.references[reference] = list()
        self.references[reference].append(_id)


if __name__ == '__main__':
    main = tk.Tk()
    canvas = CanvasPlus(main)
    canvas.pack()

    class Test:
        pass

    test = Test()

    canvas.create_oval((50, 50, 100, 100), fill='black', reference=test, level=5)
    canvas.create_oval((40, 40, 90, 90), fill='green', reference=None, level=7)
    canvas.create_oval((20, 20, 80, 60), fill='red', reference=None, level=6)
    canvas.create_oval((30, 30, 80, 80), fill='blue', reference=None)

    #canvas.delete(test)

    main.mainloop()

