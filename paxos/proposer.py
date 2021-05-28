from paxos import message as msg

class Proposer(object):
    def __init__(self, id: int, acceptors: set, network) -> None:
        self.id = id
        self.failed = False
        self.proposeID = None
        self.acceptors = acceptors
        self.network = network
        self.promised = 0
        self.accepted = 0
        self.acceptedValue = None
        self.globalProposals = None

    def propose(self):
        # je gaat proposen prepare bericht uitsturen/ ontvangt alleen proposer
        self.proposeID = self.globalProposals + 1
        for acceptor in self.acceptors:
            m = msg.Message()
            m.src = self
            m.dst = acceptor
            m.type = 'prepare'
            m.value = None

            self.network.QueueMessage(m)
        return self.proposeID

    def promise(self, value):
        # ontvangt alleen proposer
        self.promised += 1

        if self.promised > (len(self.acceptors) + 1) / 2:
            for acceptor in self.acceptors:
                m = msg.Message()
                m.src = self
                m.dst = acceptor
                m.type = 'accept'
                m.value = value

                self.network.QueueMessage(m)
            self.promised = 0

    def acceptReject(self, m):
        # ontvangt alleen proposer
        if m.type == 'accepted':
            self.accepted += 1
            if self.accepted > (len(self.acceptors) + 1) / 2:
                self.acceptedValue = m.value
                self.accepted = 0
        else:
            return

    def deliverMessage(self, m):
        """If this method gets called, does what message says and goes back to sleep."""
        if m.type == 'propose':
            self.propose()
        elif m.type == 'promise':
            self.promise(m.value)
        elif m.type == 'accepted' or m.type == 'rejected':
            self.acceptReject(m)

