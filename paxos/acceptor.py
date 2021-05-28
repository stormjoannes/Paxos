from paxos import message as msg

class Acceptor(object):
    def __init__(self, id: int, network) -> None:
        self.id = id
        self.failed = False
        self.latestPID = 1
        self.network = network
        self.prior = None

    def prepare(self, proposeID, dst, value):
        # stuur je uit, promise of niets/ ontvangt alleen acceptor
        if proposeID >= self.latestPID:
            if proposeID != self.latestPID:
                if self.prior is None:
                    self.prior = 1
                else:
                    self.prior += 1

            self.latestPID = proposeID
            # return een promise message
            m = msg.Message()
            m.src = self
            m.dst = dst
            m.type = 'promise'
            m.value = value
            m.extra = f'n={proposeID} (Prior: {self.prior})'

            self.network.QueueMessage(m)

    def accept(self, value, proposeID, dst):
        # je stuurt terug accepted of rejected/ ontvangt alleen acceptor
        if proposeID >= self.latestPID:
            self.latestPID = proposeID
            # return een promise message
            m = msg.Message()
            m.src = self
            m.dst = dst
            m.type = 'accepted'
            m.value = value
            m.extra = f'n={proposeID} v={value}'

            self.network.QueueMessage(m)
        else:
            m = msg.Message()
            m.src = self
            m.dst = dst
            m.type = 'rejected'
            m.value = value
            f'n={proposeID} v={value}'

            self.network.QueueMessage(m)

    def deliverMessage(self, m):
        """If this method gets called, does what message says and goes back to sleep."""
        if m.type == 'prepare':
            self.prepare(m.src.proposeID, m.src, m.value)
        elif m.type == 'accept':
            self.accept(m.value, m.src.proposeID, m.src)
