# Standard FIFO Queue with a fixed size
class Queue:
    def __init__(self, size_cap):
        self.size_cap = size_cap  # maximum size of the queue
        self.contents = []  # a list is used to hold the contents of the Queue

    def enqueue(self, item):  # appends an `item` to the end of the queue
        self.contents.append(item)

        if len(self.contents) > self.size_cap:  # if the max size of the queue
                                                # is reached
            self.contents.pop(0)  # remove the first item in the array
