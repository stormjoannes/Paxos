class Message(object):
    def __init__(self, src, dst, tp):
        self.src = src
        self.dst = dst
        self.type = tp