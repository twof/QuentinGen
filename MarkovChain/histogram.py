# -*- coding: utf-8 -*-
import random
import re


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
            return -1

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
        to_print += self.word
        to_print += " {"

        for key, value in self.verticies.items():
            to_print += key + ", "

        to_print += "}"
        print(to_print)


# Graph class. Just holds all the nodes.
class _Graph:
    def __init__(self):
        # dictionary where the keys are words as strings and values
        # are node objects
        self.nodes = {}
        self.insert_word(".")  # indicates the start of a thought
        self.insert_word("?")  # indicates the end of a thought

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


class Markov_Model:
    def __init__(self, corpus):
        self.graph = _Graph()
        p = "(?:(?:'([\wÀ-ÿ]+[\'\-]?[\wÀ-ÿ]*)')"\
            "|((?:[\wÀ-ÿ]+[\'\-]?[\wÀ-ÿ]*[\'\-]?)+)"\
            "|((?:['\$]?[\wÀ-ÿ]+[\'\-]?[\wÀ-ÿ]*)+))"
        self.pattern = re.compile(p)
        self.text = ""

        with open(corpus, "r") as corpus:
            self.text = str(corpus.read())

        self._gen_markov_model(self.text)

    def gen_sentence(self):
        sentence = []
        current_node = self.graph.nodes["."]

        while current_node.word is not "?":
            current_node = self.graph.rand_next_node(current_node)
            if current_node.word is "?":
                break
            else:
                sentence.append(current_node.word)

        return " ".join(sentence) + "."

    # generates a graph based on the source material passed to it
    # either as a single line of text or multiple lines like if a
    # docment was opened
    def _gen_markov_model(self, text):
        lines = text.split("\n")

        for line in lines:
            prev_word = "."
            tokens = self._tokenize_line(line)
            for token in tokens:
                self.graph.insert_word(token)
                self.graph.upsert_vert(prev_word, token)
                prev_word = token

                if token is tokens[-1]:
                    self.graph.upsert_vert(prev_word, "?")

    def _tokenize_line(self, line):
        words = map(lambda x: filter(lambda item: item is not "", x)[0],
                    self.pattern.findall(line))
        return words

    def _open_doc(source_text):
        doc = open(source_text)
        lines = doc.readlines()
        return lines


mm = Markov_Model("sanitized_corpus.txt")
print(mm.gen_sentence())
