from paxos import computer as pc
from paxos import message as msg
from paxos import network as net

proposals = 0


def createComputer(amount, type):
    computerSet = set()
    for i in range(amount):
        if type == 'P':
            computerSet.add(pc.Computer(type + str(i), True))
        else:
            computerSet.add(pc.Computer(type + str(i), False))

    return computerSet

def Simulatie(n_p, n_a, tmax, E):
    """Initialize Proposer and Acceptor sets, create network"""
    P = createComputer(n_p, 'P')
    A = createComputer(n_a, 'A')
    N = net.network([])

    print(P, '\n')
    print(A)

    for t in range(tmax):
        # If there are no messages or events, the simulation will end.
        if len(N.queue) == 0 or len(E) == 0:
            return

        # Process event E if existing
        e = [x for x in E if x[0] == t]
        if e is not None:
            E.remove(e)
            (t, F, R, pi_c, pi_v) = e
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
                pi_c.DeliverMessage(m)

        else:
            m = N.ExtractMessage()
            if m is not None:
                m.dst.DeliverMessage(m)

Simulatie(1, 2)