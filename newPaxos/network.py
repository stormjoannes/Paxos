class Network(object):
    def __init__(self):
        self.queue = []

    def queue_message(self, message):
        """"Adds the given message to the end of the queue."""
        self.queue.append(message)

    def extract_message(self):
        """Takes the first message that can be send, removes it from queue and returns the message.
           If no message can be send, it returns None."""
        for m in self.queue:
            if m.src.failed == False and m.dst.failed == False:
                self.queue.remove(m)
                return m
        return None