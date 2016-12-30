# -*- coding: utf-8 -*-
import re
import random
from Structures.Queue import Queue
from Structures.Graph import Graph


class Markov_Model:
    def __init__(self, corpus, order):
        self.order = order
        self.graph = Graph()
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
        current_node = self.graph.rand_next_node(current_node)
        sentence.append(current_node.word[0])

        while current_node.word is not "?":

            if current_node.word is "?":
                break
            else:
                sentence.append(current_node.word[-1])
                current_node = self.graph.rand_next_node(current_node)

        return " ".join(sentence) + "."

    # generates a graph based on the source material passed to it
    # either as a single line of text or multiple lines like if a
    # docment was opened
    def _gen_markov_model(self, text):
        lines = text.split("\n")

        for line in lines:
            queue = Queue(self.order + 1)
            tokens = self._tokenize_line(line)

            for index, token in enumerate(tokens):
                queue.enqueue(token)

                if len(queue.contents) >= self.order + 1:
                    if index == self.order:
                        begin_state = tuple(queue.contents[:2])
                        next_state = tuple(queue.contents[1:])

                        self.graph.insert_word(begin_state)
                        self.graph.insert_word(next_state)
                        self.graph.upsert_vert(".", begin_state)
                        self.graph.upsert_vert(begin_state, next_state)

                    elif token is tokens[-1]:
                        prev_state = tuple(queue.contents[:-1])
                        next_state = tuple(queue.contents[1:])

                        self.graph.insert_word(next_state)
                        self.graph.insert_word(prev_state)
                        self.graph.upsert_vert(prev_state, next_state)
                        self.graph.upsert_vert(next_state, "?")
                    else:
                        prev_state = tuple(queue.contents[:-1])
                        next_state = tuple(queue.contents[1:])

                        self.graph.insert_word(prev_state)
                        self.graph.insert_word(next_state)
                        self.graph.upsert_vert(prev_state, next_state)


    def _tokenize_line(self, line):
        words = map(lambda x: filter(lambda item: item is not "", x)[0],
                    self.pattern.findall(line))
        return words

    def _open_doc(source_text):
        doc = open(source_text)
        lines = doc.readlines()
        return lines


mm = Markov_Model("sanitized_corpus.txt", 2)
print(mm.gen_sentence())
