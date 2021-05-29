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
        self.rejected = 0
        self.value = None
        self.acceptedValue = None
        self.globalProposals = None

    def propose(self, value):
        # je gaat proposen prepare bericht uitsturen/ ontvangt alleen proposer
        self.value = value
        self.proposeID = self.globalProposals + 1
        for acceptor in self.acceptors:
            m = msg.Message()
            m.src = self
            m.dst = acceptor
            m.type = 'prepare'
            m.value = value
            m.extra = f'n={self.proposeID}'

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
                m.extra = f'n={self.proposeID} v={value}'

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
            self.reject += 1
            if self.reject > (len(self.acceptors) + 1) / 2:
                self.reject = 0
                self.accepted = 0


    def deliverMessage(self, m):
        """If this method gets called, does what message says and goes back to sleep."""
        if m.type == 'propose':
            return self.propose(m.value)
        elif m.type == 'promise':
            self.promise(m.value)
        elif m.type == 'accepted' or m.type == 'rejected':
            self.acceptReject(m)


    def __str__(self):
        return f'proposer {self.proposeID}, {self.id}, {self.value}'
