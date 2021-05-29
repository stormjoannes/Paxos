import message as ms


class Proposer(object):
    def __init__(self, name, network, acceptors):
        self.name = name
        self.network = network
        self.acceptors = acceptors
        self.failed = False
        self.propose_id = None
        self.a_value = None

    def deliver_message(self, message):
        """
            Deliver an message to all acceptors based on the given message type

            - if message type is propose, sends an prepare message with the propose id to all acceptors
            - if message type is promise, sends an accept message with the propose value to all acceptors
        """

        if message.mtype == "propose":
            for acceptor in self.acceptors:
                msg = ms.Message(self, acceptor, 'prepare', self.propose_id)
                self.network.queue_message(msg)

        elif message.mtype == "promise":
            msg = ms.Message(self, message.src, "accept", [self.propose_id, message.value])
            self.network.queue_message(msg)


    def accept_reject(self, message):
        """
            Check the amount of acceptors that accepted and the amount that rejected.
        """
        accepted = 0
        rejected = 0

        if message.mtype == "accepted":
            accepted += 1
        elif message.mtype == "rejected":
            rejected += 1

        if accepted > rejected:
            self.a_value = message.value
        else:
            return "not accepted"

    def receive_message(self, message):
        """The computer does what the given message says. It can call QueueMessage"""
        lower_case = message.mtype.lower()
        if lower_case == 'propose':
            self.deliver_message(message)
        elif lower_case == 'promise':
            self.deliver_message(message)
        elif lower_case == 'accepted' or lower_case == 'rejected':
            self.accept_reject(message)
        pass
