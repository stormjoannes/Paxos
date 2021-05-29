import message as ms

class Acceptor(object):
    def __init__(self, name, network):
        self.name = name
        self.network = network
        self.failed = False
        self.previous_propose_id = 0
        self.priorID = None
        self.priorValue = None

    def prepare(self, message):
        """"""
        if self.previous_propose_id <= message.value:
            m = ms.Message(self, message.src, 'promise', [message.value, self.priorID, self.priorValue])
            self.network.queue_message(m)
            self.priorID = message.value
            self.priorValue = message.value

    def accept(self, message):
        if message.value[0] >= self.priorID:
            self.priorID = message.value[0]
            m = ms.Message(self, message.src, 'accepted', message.value)
            self.network.queue_message(m)
        else:
            m = ms.Message(self, message.src, 'rejected', message.value)
            self.network.queue_message(m)

    def receive_message(self, message):
        """The computer does what the given message says. It can call QueueMessage"""
        lower_case = message.mtype.lower()
        if lower_case == 'prepare':
            self.prepare(message)
        elif lower_case == 'accept':
            self.accept(message)
