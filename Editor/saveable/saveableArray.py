from observable import Observable
from saveable.saveable import SaveableType
from saveable.saveableInt import saveable_int

import enum


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

        def __iter__(self, *args, **kwargs):
            """
            Iterates through values of the internal list
            """
            return self.values.__iter__(*args, **kwargs)

        def __getitem__(self, item):
            return self.values[item]

        def __len__(self):
            return len(self.values)

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
            if not isinstance(val, array_type):
                raise ValueError('{} is not of type {}'.format(val, array_type))
            else:
                self.values.append(val)
                self.notify_observers(ChangeType.ADD, val)

        def insert(self, ind, val):
            if not isinstance(val, array_type):
                raise ValueError('{} is not of type {}'.format(val, array_type))
            else:
                self.values.insert(ind, val)
                self.notify_observers(ChangeType.ADD, val)

        def remove(self, val):
            """
            Removes a value from the internal list and notifies all observers

            Args:
                val: The value to remove
            """
            self.values.remove(val)
            self.notify_observers(ChangeType.REMOVE, val)

        def pop(self, ind):
            """
            Removes a value from the internal list and notifies all observers

            Args:
                val: The value to remove
            """
            val = self.values.pop(ind)
            self.notify_observers(ChangeType.REMOVE, val)

        def clear(self):
            """
            Removes all values from the internal list and notifies all observers
            :return:
            """
            for value in self.values:
                self.notify_observers(ChangeType.REMOVE, value)
            self.values.clear()

        def load_in_place(self, byte_array):
            self.clear()
            size = saveable_int('u16').from_byte_array(byte_array)
            for _ in range(size.value):
                obj = array_type.from_byte_array(byte_array)
                self.notify_observers(ChangeType.ADD, obj)
                self.values.append(obj)

        def to_byte_array(self):
            size = saveable_int('u16')()
            size.set(len(self.values))
            _array = size.to_byte_array()
            for val in self.values:
                _array += val.to_byte_array()
            return _array

    return SaveableArray
