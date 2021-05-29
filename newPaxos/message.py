class Message(object):
    def __init__(self, src, dst, mtype, value):
        self.src = src
        self.dst = dst
        self.mtype = mtype
        self.value = value
