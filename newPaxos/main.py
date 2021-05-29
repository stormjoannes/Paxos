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


def simulation(amount_p, amount_a, tmax, E):
    """"""

    gpid = 0
    N = n.Network()
    A = create_computers(amount_a, "A", N)  # set with acceptors
    P = create_computers(amount_p, "P", N, A)  # set with proposers

    for tick in range(0, tmax):
        if len(N.queue) == 0 or len(E) == 0:
            # If the queue or the list with events are empty it simulation is done
            return

        # Takes the event with the same tick as the tick of the simulation
        for event in E:
            if event[0] == tick:
                e = event
                break
            else:
                e = None

        if e is not None:
            E.remove(e)
            (t, F, R, pi_c, pi_v) = e
            for computer in F:
                # Breaks the computer(s) in F
                computer.failed = True

            for computer in R:
                # Repears the ccomputer(s) in R
                computer.failed = False

            if pi_v is not None and pi_c is not None:
                gpid += 1
                pi_c.global_p_id = gpid
                message = m.Message(None, pi_c, "PROPOSE", pi_v)
                pi_c.DeliverMessage(message)

        else:
            message = N.extract_message()
            if message is not None:
                message.dst.DeliverMessage(m)