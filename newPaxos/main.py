import proposer as p
import acceptor as a
import message as m
import network as n


def create_computers(amount:int, ctype:str, network:n.Network, acceptors=None):
    """Create an amount of computers (proposers or acceptors) based on the parameters given above"""

    computerset = set()

    for x in range(1, amount + 1):
        if ctype.upper() == "P":
            computerset.add(p.Proposer(ctype + str(x), network, acceptors))
        else:
            computerset.add(a.Acceptor(ctype + str(x), network))

    return computerset


def simulatie(amount_p, amount_a, tmax, E):
    N = n.Network
    A = create_computers(amount_a, "A", N)  # set with acceptors
    P = create_computers(amount_p, "P", N, A)  # set with proposers

    for tick in range(0, tmax):
        pass
        # 1 computer kan kapot
        # 2 computer word gemaakt
        # 3 één ENKEL bericht word verstuurd
