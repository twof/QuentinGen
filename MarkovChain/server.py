from flask import Flask, request
from sampling import sentence_from_graph
from histogram import gen_histogram_graph, open_doc
import os

app = Flask(__name__)


@app.route("/word", methods=['GET'])
def get_rand_word():
    sentence_len = int(request.args.get('q'))
    graph = gen_histogram_graph(open_doc("beeMovie.txt"))

    return sentence_from_graph(graph, sentence_len)


@app.route("/", methods=['GET'])
def get_root():
    return "Try using q as a parameter where q is the length of the sentence"


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
