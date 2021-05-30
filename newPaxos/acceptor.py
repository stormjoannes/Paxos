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
        """
            Checks if the previous propose id is smaller than the given id.
            And sends a promise message back when the given id is bigger than the previous one.
        """
        if self.previous_propose_id <= message.value:
            m = ms.Message(self, message.src, 'promise', [message.value, self.priorID, self.priorValue])
            self.network.queue_message(m)

    def accept(self, message):
        """
            Checks if the propose id is larger than the prior id.
            It changes its prior id and prior value and sends a accepted message when the check is True.
            Otherwise it changes its prior id and prior value and sends a rejected message.
        """
        # print("accept message")
        if self.priorID is None or message.value[0] > self.priorID:
            print("accept prior", message.value)
            self.priorID = message.value[0]
            self.priorValue = message.value[1]
            m = ms.Message(self, message.src, 'accepted', message.value)
            # print("HALLO")
            self.network.queue_message(m)
            self.priorValue = None
        else:
            self.priorID = message.value[0]
            self.priorValue = message.value[1]
            m = ms.Message(self, message.src, 'rejected', message.value)
            self.network.queue_message(m)

    def receive_message(self, message):
        """
            Calls the right function to react to the message.
        """
        lower_case = message.mtype.lower()
        if lower_case == 'prepare':
            self.prepare(message)
        elif lower_case == 'accept':
            self.accept(message)
