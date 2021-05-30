import proposer as p
import acceptor as a
import learner as l
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


def get_computer(name, p_set=None, a_set=None):
    """
        Get the correct proposer or acceptor based on the name given
    """
    if p_set is not None:
        for proposer in p_set:
            if proposer.name == name:
                return proposer

    if a_set is not None:
        for acceptor in a_set:
            if acceptor.name == name:
                return acceptor


def set_global_p_id(p_set):
    """
       updates all proposers global_proposer_id by getting the currently highest propose id
    """
    id_lst = []

    for proposer in p_set:
        id_lst.append(0 if proposer.propose_id is None else proposer.propose_id)

    highest = max(id_lst)

    for proposer in p_set:
        proposer.global_propose_id = highest



def simulation(amount_p, amount_a, tmax, E):
    """"""

    N = n.Network()
    A = create_computers(amount_a, "A", N)  # set with acceptors
    P = create_computers(amount_p, "P", N, A)  # set with proposers

    for tick in range(0, tmax):
        if len(N.queue) == 0 and len(E) == 0:
            # If the queue or the list with events are empty it simulation is done
            output(tick, end=P)
            return


        set_global_p_id(P)

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
                computer = get_computer(computer, P, A)
                # Breaks the computer(s) in F
                computer.failed = True
                output(tick, broken=computer)

            for computer in R:
                computer = get_computer(computer, P, A)
                # Repears the computer(s) in R
                computer.failed = False
                output(tick, repair=computer)

            if pi_v is not None and pi_c is not None:
                pi_c = get_computer("P" + str(pi_c), P, A)
                message = m.Message(None, pi_c, "propose", pi_v)
                pi_c.receive_message(message)
                output(tick, message=message)

        else:
            message = N.extract_message()
            if message is not None:
                message.dst.receive_message(message)
            output(tick, message=message)


def output(tick, message=None, broken=None, repair=None, end=None):
    if message is not None:
        if message.src is not None:
            name = message.src.name

        if message.mtype == "propose":
            print(f'{tick}:    -> {message.dst.name} {message.mtype} v={message.value}')

        elif message.mtype == "prepare":
            print(f'{tick}: {name} -> {message.dst.name} {message.mtype} n={message.value}')

        elif message.mtype == "promise":
            print(f'{tick}: {name} -> {message.dst.name} {message.mtype} n={message.value[0]} (Prior: {message.value[1]}, {message.value[2]})')

        elif message.mtype == "accept" or "accepted" or "rejected":
            print(f'{tick}: {name} -> {message.dst.name} {message.mtype} n={message.value[0]} v={message.value[1]}')


    elif broken is not None:
        print(f'{tick}: ** {broken.name} kapot **')

    elif repair is not None:
        print(f'{tick}: ** {repair.name} gerepareerd **')

    elif end is not None:
        print("")
        for proposer in end:
            if proposer.propose_id is not None:
                print(f'{proposer.name} heeft wel consensus (voorgesteld: {proposer.begin_id}, geaccepteerd: '
                      f'{proposer.accepted_value[1]})')
            else:
                print(f'{proposer.name} heeft geen consensus.')
    else:
        print(f'{tick}:')


simulation(2, 3, 100, [[0, [], [], 1, 42], [8, ["P1"], [], None, None], [11, [], [], 2, 37], [26, [], ["P1"], None, None]])
