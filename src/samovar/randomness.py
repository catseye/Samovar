# Sources of randomness, for Samovar.


class CannedRandomness(object):
    def __init__(self):
        self.counter = 0
        self.limit = 1

    def advance(self):
        self.counter += 1
        if self.counter > self.limit:
            self.counter = 0
            self.limit += 1

    def choice(self, iterable):
        length = len(iterable)
        index = self.counter % length
        selection = iterable[index]
        self.advance()
        return selection
