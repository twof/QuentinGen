import random


def sentence_from_graph(graph, sentence_len):
    sentence = []
    current_node = graph.nodes[random.choice(list(graph.nodes.keys()))]

    for i in range(sentence_len):
        sentence.append(current_node.word)
        current_node = graph.rand_next_node(current_node)

    return " ".join(sentence)
