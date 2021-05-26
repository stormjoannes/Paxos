from paxos import message as msg
from paxos import network as net

class Computer(object):
    def __init__(self, id: int, proposer: bool) -> None:
        self.id = id
        self.failed = False
        self.proposer = proposer
        self.proposeID = None
        self.latestPID = None

    def propose(self, value: str):
        # je gaat proposen prepare bericht uitsturen/ ontvangt alleen proposer
        for acceptor in acceptors:
            m = msg.Message()
            m.src = self
            m.dst = acceptor
            m.type = 'prepare'
            m.value = value

            net.network.QueueMessage(m)

    def prepare(self, proposeID):
        # stuur je uit, promise of niets/ ontvangt alleen acceptor
        if proposeID > self.latestPID:
            self.latestPID = proposeID
            # return een promise message

    def accept(self, value: str, proposeID):
        # je stuurt terug accepted of rejected/ ontvangt alleen acceptor
        pass

    def promise(self):
        # ontvangt alleen proposer
        pass

    def acceptReject(self):
        # ontvangt alleen proposer
        pass

    def DeliverMessage(self, m):
        """If this method gets called, does what message says and goes back to sleep."""
        if m.type == 'propose':
            self.propose(m.value)
        elif m.type == 'prepare':
            self.prepare(m.src.proposeID)
        elif m.type == 'accept':
            self.accept(m.value, m.src.proposeID)
        elif m.type == 'promise':
            pass
        elif m.type == 'accepted' or m.type == 'rejected':
            pass

        pass
