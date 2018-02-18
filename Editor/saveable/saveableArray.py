import enum

from observable import Observable
from Editor.saveable.saveable import SaveableType
from Editor.saveable.saveableInt import saveable_int
from Editor.signal import Signal


class ChangeType(enum.Enum):
    """
    Constant used for Observables to notify observers that something has been changed or removed
    """
    ADD = 1
    REMOVE = 2


def array(array_type):
    """
    A saveable array type that can hold any number of a single type. Type is observable on adds and removes

    Args:
        array_type: The Saveable object type to store in the array

    Returns:
        A Saveable array type
    """
    class SaveableArray(SaveableType, Observable):
        def __init__(self):
            SaveableType.__init__(self)
            Observable.__init__(self)
            self.values = []
            self.signal_add = Signal()
            self.signal_remove = Signal()
            self.array_type = array_type
            self.signal_changed = Signal()

        def __iter__(self, *args, **kwargs):
            """
            Iterates through values of the internal list
            """
            return self.values.__iter__(*args, **kwargs)

        def __getitem__(self, item):
            return self.values[item]

        def __len__(self):
            return len(self.values)

        def __str__(self):
            return str(self.values)

        def set(self, values):
            for value in values:
                if not isinstance(value, array_type):
                    raise ValueError("Value '{}' in array is not of type {}".format(value, array_type))
            self.clear()
            self.values = list(values)

        def index(self, val):
            return self.values.index(val)

        def append(self, val):
            """
            Adds a value to the array and checks to make sure it's Saveable and notifies all observers

            Args:
                val: The array_type value to add
            """
            self.insert(len(self.values), val)

        def insert(self, ind, val):
            if not isinstance(val, array_type):
                try:
                    val = array_type(val)
                except:
                    raise ValueError('{} is not of type {}'.format(val, array_type))
            self.values.insert(ind, val)
            self.notify_observers(ChangeType.ADD, val)
            self.signal_add(ind, val)
            self.signal_changed(ind)
            if callable(getattr(val, 'signal_changed', None)):
                val.signal_changed.connect(self.signal_changed)

        def remove(self, val):
            """
            Removes a value from the internal list and notifies all observers

            Args:
                val: The value to remove
            """
            ind = self.values.index(val)
            self.pop(ind)

        def pop(self, ind):
            """
            Removes a value from the internal list and notifies all observers

            Args:
                val: The value to remove
            """
            val = self.values.pop(ind)
            self.notify_observers(ChangeType.REMOVE, val)
            self.signal_remove(ind, val)
            return val

        def clear(self):
            """
            Removes all values from the internal list and notifies all observers
            :return:
            """
            for ind in range(len(self.values)-1, -1, -1):
                self.pop(ind)

        def load_in_place(self, byte_array):
            self.clear()
            size = saveable_int('u16').from_byte_array(byte_array)
            for _ in range(size.value):
                obj = array_type.from_byte_array(byte_array)
                self.append(obj)

        def to_byte_array(self):
            size = saveable_int('u16')()
            size.set(len(self.values))
            _array = size.to_byte_array()
            for val in self.values:
                _array += val.to_byte_array()
            return _array

    return SaveableArray


if __name__ == '__main__':
    IntType = saveable_int('u16')
    ArrayType = array(IntType)
    a = ArrayType()
    for i in range(10):
        a.append(IntType(i))
    print(a)
    b = a.to_byte_array()
    print(b)
    a.load_in_place(b)
    print(a)