from utilities.callername import caller_name


class SimpleSaver:
    def __init__(self, saveable):
        self.saveable = saveable

    def load(self, path):
        file = open(path, 'rb')
        data = bytearray(file.read())
        self.saveable.load_in_place(data)
        file.close()

    def save(self, path):
        data = self.saveable.to_byte_array()
        file = open(path, 'wb')
        file.write(data)
        file.close()

    def new(self):
        new = type(self.saveable)()
        array = new.to_byte_array()
        self.saveable.load_in_place(array)

    def connect_to_menu(self, menu):
        menu.signal_save.connect(self.save)
        menu.signal_load.connect(self.load)
        menu.signal_new.connect(self.new)
