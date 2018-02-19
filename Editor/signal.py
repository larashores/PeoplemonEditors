class Signal:
    def __init__(self):
        self.connections = []
        self.debug = False

    def __call__(self, *args, **kwargs):
        for func in self.connections:
            try:
                func(*args, **kwargs)
            except Exception as e:
                raise ValueError('{}: {}'.format(func, e))

    def connect(self, func):
        if func not in self.connections:
            if self.debug:
                print('Connection ', func)
            self.connections.append(func)
        else:
            if self.debug:
                print('Repeat Connection ', func)

    def disconnect(self, func):
        if func in self.connections:
            if self.debug:
                print('Disconnection ', func)
            self.connections.remove(func)

    def clear(self):
        if self.debug:
            print('clear ')
        self.connections.clear()