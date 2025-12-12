from NLP.utils import Parser, NgramGenerator
from NLP.smoothing import *

if __name__ == "__main__":

    parser = Parser()
    with open("resources/charmony_dove.txt", 'r', encoding='utf+8') as f:
        corpus = f.read()

    parsed_corpus = parser.tokenize(corpus)
    N = 4

    generator = NgramGenerator(N)
    ngrams = generator.generate_ngrams(parsed_corpus)
    # print(ngrams[1])

    test = parser.tokenize("one day dinner")
    context, word = tuple(test[:-1]), tuple(test[-1:])
    # print(context, word)

    smoothing = GoodTuringSmoothing()
    ngram_probs = smoothing(ngrams)
