import message as ms


class Proposer(object):
    def __init__(self, name, network, acceptors, learners):
        self.name = name
        self.network = network
        self.acceptors = acceptors
        self.learners = learners
        self.failed = False
        self.begin_id = None
        self.propose_id = None
        self.reject_count = 0
        self.accept_count = 0
        self.propose_value = None
        self.accepted_value = None
        self.global_propose_id = None
        self.count = 0

    def deliver_message(self, message):
        """
            Deliver an message to all acceptors based on the given message type

            - if message type is propose, sends an prepare message with the propose id to all acceptors
            - if message type is promise, sends an accept message with the propose value to all acceptors
        """

        if message.mtype == "propose":
            self.begin_id = message.value
            self.propose_id = self.global_propose_id + 1
            self.propose_value = message.value
            for acceptor in self.acceptors:
                msg = ms.Message(self, acceptor, 'prepare', self.propose_id)
                self.network.queue_message(msg)

        elif message.mtype == "promise":
            if message.value[2] is not None:
                self.propose_value = message.value[2]
                msg = ms.Message(self, message.src, "accept", [self.propose_id, message.value[2]])
            else:
                msg = ms.Message(self, message.src, "accept", [self.propose_id, self.propose_value])
            self.network.queue_message(msg)

    def resend(self):
        """
            if there are more acceptors that rejected than accepted. send an message with the same value but
            with a higher propose_id
        """
        self.propose_id = self.global_propose_id + 1

        for acceptor in self.acceptors:
            msg = ms.Message(self, acceptor, 'prepare', self.propose_id)
            self.network.queue_message(msg)

    def accept_reject(self, message):
        """
            Check the amount of acceptors that accepted and the amount that rejected.
            only check if all acceptors have send a message (count)
        """
        self.count += 1

        if message.mtype == "rejected":
            self.reject_count += 1
        else:
            self.accept_count += 1

        if self.count == len(self.acceptors):
            if round(len(self.acceptors) / 2) <= self.reject_count:
                self.reject_count = 0
                self.resend()

        if self.count == len(self.acceptors):
            if round(len(self.acceptors) / 2) <= self.accept_count:
                self.accept_count = 0
                self.accepted_value = message.value
                for learner in self.learners:
                    msg = ms.Message(self, learner, 'succes', message.value)
                    self.network.queue_message(msg)

            self.count = 0

    def receive_message(self, message):
        """The computer does what the given message says. It can call QueueMessage"""
        lower_case = message.mtype.lower()
        if lower_case == 'propose':
            self.deliver_message(message)
        elif lower_case == 'promise':
            self.deliver_message(message)
        elif lower_case == 'accepted' or lower_case == 'rejected':
            self.accept_reject(message)
