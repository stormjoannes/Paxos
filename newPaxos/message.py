class Message(object):
    def __init__(self, src, dst, mtype, value):
        self.src = src
        self.dst = dst
        self.mtype = mtype
        self.value = value

    def __str__(self):
        return f'Message {self.src.name}, {self.dst.name}, {self.mtype}, {self.value}'