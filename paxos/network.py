class network(object):
    def __init__(self, queue: list) -> None:
        self.queue = queue

    def QueueMessage(self, m):
        """"Add message to end of network(que)"""
        self.queue.append(m)

    def ExtractMessage(self):
        """Find first message in queue so that if 'm.src.failed=false' and 'm.dst.failed=false' message
        gets deleted from network and gets returned"""
        msg = self.queue[0]
        source = msg.src
        destination = msg.dst
        if source.failed == False and destination.failed == False:
            self.queue.remove(msg)
            return msg.value
        else:
            return None
