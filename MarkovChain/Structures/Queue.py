class Queue:
    def __init__(self, size_cap):
        self.size_cap = size_cap
        self.contents = []

    def enqueue(self, item):
        self.contents.append(item)

        if len(self.contents) > self.size_cap:
            self.contents.pop(0)
