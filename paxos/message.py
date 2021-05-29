class Message(object):
    def __init__(self) -> None:
        self.src = None
        self.dst = None
        self.type = None
        self.value = None
        self.extra = None

    def __str__(self):
        return f'Message({self.src},{self.dst},{self.type},{self.value}, {self.extra})'
