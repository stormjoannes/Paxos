from paxos import message as msg

class Acceptor(object):
    def __init__(self, id: int, network) -> None:
        self.id = id
        self.failed = False
        self.latestPID = None
        self.network = network

    def prepare(self, proposeID, dst):
        # stuur je uit, promise of niets/ ontvangt alleen acceptor
        if proposeID >= self.latestPID:
            self.latestPID = proposeID
            # return een promise message
            m = msg.Message()
            m.src = self
            m.dst = dst
            m.type = 'promise'
            m.value = None

            self.network.QueueMessage(m)

    def accept(self, value: str, proposeID, dst):
        # je stuurt terug accepted of rejected/ ontvangt alleen acceptor
        if proposeID >= self.latestPID:
            self.latestPID = proposeID
            # return een promise message
            m = msg.Message()
            m.src = self
            m.dst = dst
            m.type = 'accepted'
            m.value = value

            self.network.QueueMessage(m)
        else:
            m = msg.Message()
            m.src = self
            m.dst = dst
            m.type = 'rejected'
            m.value = value

            self.network.QueueMessage(m)

    def deliverMessage(self, m):
        """If this method gets called, does what message says and goes back to sleep."""
        if m.type == 'prepare':
            self.prepare(m.src.proposeID, m.src)
        elif m.type == 'accept':
            self.accept(m.value, m.src.proposeID, m.src)
