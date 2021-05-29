class Proposer(object):
    def __init__(self, name, network, acceptors):
        self.name = name
        self.network = network
        self.acceptors = acceptors
        self.failed = False

    def DeliverMessage(self, message):
        """The computer does what the given message says. It can call QueueMessage"""
        pass