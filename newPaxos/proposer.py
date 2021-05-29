import message as ms


class Proposer(object):
    def __init__(self, name, network, acceptors):
        self.name = name
        self.network = network
        self.acceptors = acceptors
        self.failed = False
        self.propose_id = None
        self.accept_count = 0
        self.reject_count = 0
        self.propose_value = None

    def deliver_message(self, message):
        """
            Deliver an message to all acceptors based on the given message type

            - if message type is propose, sends an prepare message with the propose id to all acceptors
            - if message type is promise, sends an accept message with the propose value to all acceptors
        """

        if message.mtype == "propose":
            self.propose_value = message.value
            for acceptor in self.acceptors:
                msg = ms.Message(self, acceptor, 'prepare', self.propose_id)
                self.network.queue_message(msg)

        elif message.mtype == "promise":
            msg = ms.Message(self, message.src, "accept", [self.propose_id, self.propose_value])
            self.network.queue_message(msg)

    def resend(self):
        for acceptor in self.acceptors:
            msg = ms.Message(self, acceptor, 'prepare', self.propose_id)
            self.network.queue_message(msg)

    def accept_reject(self, message):
        """
            Check the amount of acceptors that accepted and the amount that rejected.
        """
        if message.mtype == "accepted":
            self.accept_count += 1
        elif message.mtype == "rejected":
            self.reject_count += 1

        if self.accept_count >= self.reject_count:
            self.propose_value = message.value

        else:
            self.resend()

    def receive_message(self, message):
        """The computer does what the given message says. It can call QueueMessage"""
        lower_case = message.mtype.lower()
        if lower_case == 'propose':
            self.deliver_message(message)
        elif lower_case == 'promise':
            self.deliver_message(message)
        elif lower_case == 'accepted' or lower_case == 'rejected':
            self.accept_reject(message)
