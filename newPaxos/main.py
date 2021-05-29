import proposer as p
import acceptor as a
import message as m
import network as n


def create_computers(amount:int, ctype:str, network, acceptors=None):
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
        if len(N.queue) == 0 and len(E) == 0:
            # If the queue or the list with events are empty it simulation is done
            return

        # Takes the event with the same tick as the tick of the simulation
        e = None
        for event in E:
            if event[0] == tick:
                e = event
                break

        if e is not None:
            E.remove(e)
            (t, F, R, pi_c, pi_v) = e
            for computer in F:
                # Breaks the computer(s) in F
                computer.failed = True

            for computer in R:
                # Repears the computer(s) in R
                computer.failed = False

            if pi_v is not None and pi_c is not None:
                gpid += 1

                for proposer in P:
                    if "P" + str(pi_c) == proposer.name:
                        pi_c = proposer

                pi_c.propose_id = gpid
                message = m.Message(None, pi_c, "propose", pi_v)
                pi_c.receive_message(message)

        else:
            message = N.extract_message()
            if message is not None:
                message.dst.receive_message(message)
        output(tick, message)


def output(tick, message):
    if message is None:
        return "empty"

    if message.src is None:
        name = ' '
    else:
        name = message.src.name
    print(f'{tick}: {name} -> {message.dst.name} {message.mtype} {message.value}')


simulation(1, 3, 20, [[0, [], [], 1, 42]])
