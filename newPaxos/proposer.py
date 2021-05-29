import message as ms

class Proposer(object):
    def __init__(self, name, network, acceptors):
        self.name = name
        self.network = network
        self.acceptors = acceptors
        self.failed = False
        self.global_p_id = None

    def propose(self, value):
        """
            Receive a propose message
            Send new prepare message to network queue for acceptors to receive
        """
        for acceptor in self.acceptors:
            msg = ms.Message(self, acceptor, 'prepare', value)

            self.network.queue_message(msg)


    def promise(self, value):
        """
            Receive a promise message from the acceptors
            Send new accept message to network queue for acceptors to receive
        """



    def DeliverMessage(self, message):
        """The computer does what the given message says. It can call QueueMessage"""
        if message.type == 'propose':
            self.propose(message.value)
        elif message.type == 'promise':
            self.promise(message.value)
        elif message.type == 'accepted' or message.type == 'rejected':
            self.acceptReject(message)
        pass
