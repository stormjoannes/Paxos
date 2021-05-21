class Computer(object):
    def __init__(self, id: int) -> None:
        self.id = id
        self.failed = False


    def proposer(self, value: str, id: float):
        pass

    def acceptor(self, type: str):
        pass

    def Deliver_Message(self, m):
        """If this method gets called, does what message says and goes back to sleep."""
        pass
