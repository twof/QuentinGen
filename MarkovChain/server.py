from flask import Flask
from Markov_Model import Markov_Model
import os

app = Flask(__name__)

markov_model = Markov_Model("sanitized_corpus.txt", 2)


@app.route("/sentence", methods=['GET'])
def gen_rand_sentence():
    return markov_model.gen_sentence()


# The root route doesn't do anything right now
@app.route("/", methods=['GET'])
def get_root():
    return "Try hitting /sentence"


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
