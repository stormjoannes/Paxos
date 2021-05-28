from paxos import proposer as pp
from paxos import acceptor as ap
from paxos import message as msg
from paxos import network as net

proposals = 0

# events = [[0, [], [], 1, 42], [8, [0], [], None, None], [11, [], [], 2, 37], [26, [], [0], 1, None]]
# maxTicks = 15
# amountProposers = 1
# amountAcceptors = 3

def createEvent():
    stop = False
    E = []

    PAT = input('Proposers, Acceptors, Ticks: ')
    PAT = PAT.split(' ')
    PAT = [int(x) for x in PAT]
    P, A, tmax = PAT

    while stop == False:
        inp = input('Event: ')

        inp = inp.split(' ')
        inp = [x.lower() for x in inp]

        if inp == ['']:
            continue

        elif inp[1] == 'end':
            stop = True

        elif inp[1] == "propose":
            E.append([int(inp[0]), [], [], int(inp[-2]) - 1, int(inp[-1])])

        elif inp[1] == "fail":
            E.append([int(inp[0]), [int(inp[-1]) - 1], [], None, None])

        elif inp[1] == "recover":
            E.append([int(inp[0]), [], [int(inp[-1]) - 1], None, None])

        else:
            print("This input is invalid. Pls try again.")

    return P, A, tmax, E

def createComputer(amount, type, network, acceptors=None):
    computerSet = set()
    for i in range(amount):
        if type == 'P':
            computerSet.add(pp.Proposer(type + str(i + 1), acceptors, network))
        else:
            computerSet.add(ap.Acceptor(type + str(i + 1), network))

    return computerSet

def Simulatie(n_p, n_a, tmax, E, proposals):
    """Initialize Proposer and Acceptor sets, create network"""
    N = net.network()
    A = createComputer(n_a, 'A', N)
    P = createComputer(n_p, 'P', N, A)

    for t in range(tmax):
        # If there are no messages or events, the simulation will end.
        if len(N.queue) == 0 and len(E) == 0:
            for proposer in P:
                print(f'\n{proposer.id} heeft wel consensus (voorgesteld: {proposer.value}, geaccepteerd: '
                      f'{proposer.acceptedValue})')
            return

        for proposer in P:
            proposer.globalProposals = proposals

        # Process event E if existing
        for x in E:
            if x[0] == t:
                e = x
        if E == []:
            e = None

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
                m.tick = t
                m.extra = f'v={pi_v}'
                x = pi_c.deliverMessage(m)
                if x is not None:
                    proposals = x

        else:
            m = N.ExtractMessage()
            if m is not None:
                x = m.dst.deliverMessage(m)
                if x is not None:
                    proposals = x

        output(t, m)

def output(tick, msg):
    src = '  ' if msg.src is None else msg.src.id
    print(f'{tick}: {src} -> {msg.dst.id} {msg.type} {msg.extra}')


amountProposers, amountAcceptors, maxTicks, events = createEvent()
Simulatie(amountProposers, amountAcceptors, maxTicks, events, proposals)
