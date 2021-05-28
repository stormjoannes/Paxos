from paxos import proposer as pp
from paxos import acceptor as ap
from paxos import message as msg
from paxos import network as net

proposals = 0

events = [[0, [], [], 1, 42]]
maxTicks = 15
amountProposers = 1
amountAcceptors = 3

def createComputer(amount, type, network, acceptors=None):
    computerSet = set()
    for i in range(amount):
        if type == 'P':
            computerSet.add(pp.Proposer(type + str(i), acceptors, network))
        else:
            computerSet.add(ap.Acceptor(type + str(i), network))

    return computerSet

def Simulatie(n_p, n_a, tmax, E):
    """Initialize Proposer and Acceptor sets, create network"""
    N = net.network(E)
    A = createComputer(n_a, 'A', N)
    P = createComputer(n_p, 'P', N, A)

    for t in range(tmax):
        # If there are no messages or events, the simulation will end.
        if len(N.queue) == 0 or len(E) == 0:
            return

        # Process event E if existing
        for x in E:
            print(x, 'boep')
            if x[0] == t:
                e = x

        if e is not None:
            E.remove(e)
            t, F, R, pi_c, pi_v = e
            pi_c = list(P)[pi_c - 1]
            for c in F:
                c.failed = True
            for c in R:
                c.failed = False
            if pi_v is not None and pi_c is not None:
                m = msg.Message()
                m.type = 'propose'
                m.src = None  # PROPOSE-message begin out of network
                m.dst = pi_c
                m.value = pi_v
                pi_c.deliverMessage(m)

        else:
            m = N.ExtractMessage()
            if m is not None:
                m.dst.deliverMessage(m)

        output(t, m)
    print('\n')
    for proposer in P:
        print(f'{proposer.id} heeft wel consensus (voorgesteld: {proposer.proposeID}, geaccepteerd: '
              f'{proposer.acceptedValue})')

def output(tick, msg):
    print(f'{tick}: {msg.src} -> {msg.dst.id} {msg.type} extra')


Simulatie(amountProposers, amountAcceptors, maxTicks, events)