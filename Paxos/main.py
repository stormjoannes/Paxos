import proposer as p
import acceptor as a
import learner as l
import message as m
import network as n

def get_input():
    """
        Creates formatted input for the simulation function by entering the right event commands
    """
    stop = False
    E = []

    print("Als je spaties wilt toevoegen bij de propose value doe dat dat met een '_'. Voorbeeld: 0 PROPOSE 1 nl:_g")
    PAT = input('Proposers, Acceptors, Learners, Ticks: ')
    PAT = PAT.split(' ')
    PAT = [int(x) for x in PAT]
    P, A, L, tmax = PAT

    while stop == False:
        inp = input('Event: ')

        inp = inp.split(' ')
        inp_split = [x.lower() for x in inp]

        if inp_split == ['']:
            continue

        elif inp_split[1] == 'end':
            stop = True

        elif inp_split[1] == "propose":
            if ":" in inp_split[-1] or ":" in inp_split[-2]:
                if len(inp_split[-1]) == 1:
                    inp_split[-2] = inp_split[-2] + " " + inp_split[-1]
                    inp_split.pop()
                value = inp_split[-1]
            else:
                value = int(inp_split[-1])
            E.append([int(inp_split[0]), [], [], int(inp_split[-2]), value])

        elif inp_split[1] == "fail":
            E.append([int(inp_split[0]), [inp_split[-2][0].upper() + inp_split[-1]], [], None, None])

        elif inp_split[1] == "recover":
            E.append([int(inp_split[0]), [], [inp_split[-2][0].upper() + inp_split[-1]], None, None])

        else:
            print("This input is invalid. Pls try again.")

    return P, A, L, tmax, E

def create_computers(amount:int, ctype:str, network, acceptors=None, learners=None):
    """
        Create an amount of computers (proposers or acceptors) based on the parameters given above
    """

    computerset = set()

    for x in range(1, amount + 1):
        if ctype.upper() == "P":
            computerset.add(p.Proposer(ctype + str(x), network, acceptors, learners))
        elif ctype.upper() == "A":
            computerset.add(a.Acceptor(ctype + str(x), network))
        else:
            computerset.add(l.Learner(ctype + str(x), network))

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
       Updates all proposers global_proposer_id by getting the currently highest propose id
    """
    id_lst = []

    for proposer in p_set:
        id_lst.append(0 if proposer.propose_id is None else proposer.propose_id)

    highest = max(id_lst)

    for proposer in p_set:
        proposer.global_propose_id = highest


def simulation(amount_p, amount_a, amount_l, tmax, E):
    """
        Simulate the paxos algorithme
    """

    N = n.Network()
    A = create_computers(amount_a, "A", N)  # set with acceptors
    L = create_computers(amount_l, "L", N)
    P = create_computers(amount_p, "P", N, A, L)  # set with proposers

    for tick in range(0, tmax):
        if len(N.queue) == 0 and len(E) == 0:
            # If the queue or the list with events are empty it simulation is done
            output(tick, tmax, end=P)
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
                output(tick, tmax, broken=computer)

            for computer in R:
                computer = get_computer(computer, P, A)
                # Repears the computer(s) in R
                computer.failed = False
                output(tick, tmax, repair=computer)

            if pi_v is not None and pi_c is not None:
                pi_c = get_computer("P" + str(pi_c), P, A)
                message = m.Message(None, pi_c, "propose", pi_v)
                pi_c.receive_message(message)
                output(tick, tmax, message=message)

        else:
            message = N.extract_message()
            if message is not None:
                message.dst.receive_message(message)
            output(tick, tmax, message=message)


def output(tick, tmax, message=None, broken=None, repair=None, end=None):
    """
        Prints rights output lines
    """
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
        # create whiteline before creating consensus line
        print()
        for proposer in end:
            if proposer.propose_id is not None:
                print(f'{proposer.name} heeft wel consensus (voorgesteld: {proposer.begin_id}, geaccepteerd: '
                      f'{proposer.accepted_value[1]})')
            else:
                print(f'{proposer.name} heeft geen consensus.')

    # if tmax is high its unnecessary to print the ticks where nothing happens
    elif tmax < 500:
        print(f'{tick}:')


amountProposers, amountAcceptors, amountLearners, maxTicks, events = get_input()
simulation(amountProposers, amountAcceptors, amountLearners, maxTicks, events)
