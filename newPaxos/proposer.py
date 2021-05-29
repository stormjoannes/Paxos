import message as ms


class Proposer(object):
    def __init__(self, name, network, acceptors):
        self.name = name
        self.network = network
        self.acceptors = acceptors
        self.failed = False
        self.propose_id = None
        self.a_value = None

    def deliver_message(self, value, mtype):
        """
            Deliver an message to all acceptors based on the given message type

            - if message type is propose, sends an prepare message with the propose id to all acceptors
            - if message type is promise, sends an accept message with the propose value to all acceptors
        """
        for acceptor in self.acceptors:
            if mtype == "propose":
                msg = ms.Message(self, acceptor, 'prepare', self.propose_id)
            elif mtype == "promise":
                msg = ms.Message(self, acceptor, "accept", [self.propose_id, value])

            self.network.queue_message(msg)

    def accept_reject(self, message):
        """
            Check the amount of acceptors that accepted and the amount that rejected.
        """

        accepted = 0
        rejected = 0

        if message.type == "accepted":
            accepted += 1
        elif message.type == "rejected":
            rejected += 1

        if accepted > rejected:
            self.a_value = accepted
        else:
            return "not accepted"

    def receive_message(self, message):
        """The computer does what the given message says. It can call QueueMessage"""
        if message.type == 'propose':
            self.deliver_message(message.value, 'propose')
        elif message.type == 'promise':
            self.deliver_message(message.value, 'promise')
        elif message.type == 'accepted' or message.type == 'rejected':
            self.accept_reject(message)
        pass
