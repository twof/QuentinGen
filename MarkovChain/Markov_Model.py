# -*- coding: utf-8 -*-
import re
from Structures.Queue import Queue
from Structures.Graph import Graph


class Markov_Model:
    def __init__(self, corpus, order):
        # The order of the markov model.
        # A second order markov model would map a set of two previous words
        # to the next subsequent word.
        self.order = order
        self._graph = Graph()
        # The regular expression used for tokenization
        # TODO: This regex spits out tuples of len 3 for every token, two of
        # which are empty strings. I'm cleansing the empty strings right now,
        # but there ought to be a way to only return one capture group
        p = "(?:(?:'([\wÀ-ÿ]+[\'\-]?[\wÀ-ÿ]*)')"\
            "|((?:[\wÀ-ÿ]+[\'\-]?[\wÀ-ÿ]*[\'\-]?)+)"\
            "|((?:['\$]?[\wÀ-ÿ]+[\'\-]?[\wÀ-ÿ]*)+))"
        self.pattern = re.compile(p)

        with open(corpus, "r") as corpus:
            # generate a graph based on the text from the corpus
            self._gen_markov_model(str(corpus.read()))

    # generate a sentence from the markov model
    def gen_sentence(self):
        sentence = []
        current_node = self._graph.nodes["."]
        current_node = self._graph.rand_next_node(current_node)
        sentence.append(current_node.word[0])

        while current_node.word is not "?":
            if current_node.word is "?":
                break
            else:
                sentence.append(current_node.word[-1])
                current_node = self._graph.rand_next_node(current_node)

        return " ".join(sentence) + "."

    # generates a graph based on the source material passed to it
    # either as a single line of text or multiple lines like if a
    # docment was opened
    def _gen_markov_model(self, text):
        lines = text.split("\n")  # Get an array of lines of text
        # from the corpus

        # TODO: figure out how to clean this up
        def handle_begin(queue):
            begin_state = tuple(queue.contents[:2])
            next_state = tuple(queue.contents[1:])

            self._graph.insert_word(begin_state)
            self._graph.insert_word(next_state)
            self._graph.upsert_vert(".", begin_state)
            self._graph.upsert_vert(begin_state, next_state)

        def handle_end(queue):
            prev_state = tuple(queue.contents[:-1])
            next_state = tuple(queue.contents[1:])

            self._graph.insert_word(next_state)
            self._graph.insert_word(prev_state)
            self._graph.upsert_vert(prev_state, next_state)
            self._graph.upsert_vert(next_state, "?")

        def handle_rest(queue):
            prev_state = tuple(queue.contents[:-1])
            next_state = tuple(queue.contents[1:])

            self._graph.insert_word(prev_state)
            self._graph.insert_word(next_state)
            self._graph.upsert_vert(prev_state, next_state)

        for line in lines:
            queue = Queue(self.order + 1)
            tokens = self._tokenize_line(line)

            for index, token in enumerate(tokens):
                queue.enqueue(token)

                if len(queue.contents) >= self.order + 1:
                    # handles the start of sentences
                    if index == self.order:
                        handle_begin(queue)

                        # handles edge case where len of sentence == order + 1
                        if token is tokens[-1]:
                            handle_end(queue)

                    # handles the end of sentences
                    elif token is tokens[-1]:
                        handle_end(queue)
                    # handles everything else
                    else:
                        handle_rest(queue)

    def _tokenize_line(self, line):
        words = map(lambda x: filter(lambda item: item is not "", x)[0],
                    self.pattern.findall(line))
        return words

    def _open_doc(source_text):
        doc = open(source_text)
        lines = doc.readlines()
        return lines

    '''
    Possible extentions:
    Allow appending to existing markov models. This could be useful if your
    corpus is ongoing eg. tweets, serial novels

    Support combining markov models. This could be useful for mashups
    eg. Quentin Tarentino x The Muppets, Trump x Hitler
    '''
