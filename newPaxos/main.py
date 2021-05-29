import proposer as p
import acceptor as a
import message as m
import network as n

def simulation(aantal_proposers, aantal_acceptors, tmax, E):
    """"""
    P = {} # Set with proposers
    A = {} # Set with acceptors
    N = n.Network() # Creates network

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
                message = m.Message()
                message.type = "PROPOSE"
                message.dst = pi_c
                message.value = pi_v
                pi_c.DeliverMessage(message)

        else:
            message = N.ExtractMessage()
            if message is not None:
                message.dst.DeliverMessage(m)