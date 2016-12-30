import random


# Node class. Contains the word and a dictionary of each possible
# subsequent word
class _Node:
    def __init__(self, word):
        # dictionary where the key is the word
        # and the value is [Node, frequency]
        # using an array for easy incrementation
        self.verticies = {}
        self.word = word
        self.total_subsequence_count = 0

    # increments the frequency of the word if it exsits
    # otherwise insert it as a vertex with a frequency of 1
    def upsert_vert(self, the_word, node_dict):
        if the_word in self.verticies:
            self.verticies[the_word][1] += 1
            self.total_subsequence_count += 1
        else:
            self.verticies[the_word] = [node_dict[the_word], 1]
            self.total_subsequence_count += 1

    # takes a node and returns a subsequent node at random
    # based off of the frequency of the the verticies
    def rand_next_node(self):
        if self.total_subsequence_count-1 == -1:
            return -1  # This should never trigger under the current model

        rand_index = random.randint(0, self.total_subsequence_count-1)
        traversal_index = 0

        for key, value in self.verticies.items():
            if rand_index in range(traversal_index, value[1]
                                   + traversal_index):

                return self.verticies[key][0]
            else:
                traversal_index += value[1]

    # pretty self explanitory, prints the contents of the node
    # used this for debugging but thought I'd leave it in just in case
    # someone else wanted it
    def print_node(self):
        to_print = ""
        to_print += repr(self.word)
        to_print += " {"

        for key, value in self.verticies.items():
            to_print += repr(key) + ", "

        to_print += "}"
        print(to_print)


# Graph class. Just holds all the nodes.
class Graph:
    def __init__(self):
        # dictionary where the keys are words as strings and values
        # are node objects
        self.nodes = {}
        self.insert_word(".")
        self.insert_word("?")

    # inserts a word into the graph if it doesn't already exist
    # within the graph
    def insert_word(self, word):
        if word not in self.nodes:
            self.nodes[word] = _Node(word)

    # abstraction of the node.upsert_vert() fuction
    # trying to minimize interaction with raw nodes
    def upsert_vert(self, prev_word, subsequent_word):
        self.nodes[prev_word].upsert_vert(subsequent_word, self.nodes)

    # Similar to above, minimizing raw node interaction
    # There's a chance that a node won't have any verticies
    # If that's the case, we start at a new random location
    # within the graph
    def rand_next_node(self, node):
        return node.rand_next_node()

    # Runs through each node in the graph and prints it out
    # Also used primarily for debugging
    def print_graph(self):
        for key in self.nodes.keys():
            # dictionary of word: Node
            self.nodes[key].print_node()
