from NLP.smoothing import AddKSmoothing
from NLP.utils import Parser, NgramGenerator

parser = Parser()
with open("../../resources/charmony_dove.txt", "r", encoding="utf-8") as f:
    sentence = f.read()
    parsed_sentence = parser.parse(sentence)

N = 10
ngrams = NgramGenerator(N).generate_ngrams(parsed_sentence)
allowed_error = 1e-6
vocab_size = 1000

def test_probs_sum_to_one():
    for k in range(1, 10):
        smoothing = AddKSmoothing(k, vocab_size)
        prob_dict = smoothing(ngrams).main_dict

        for n in range(1, N + 1):
            for context in prob_dict[n]:
                unseen_grams = vocab_size - len(prob_dict[n][context])
                assert (1 - (sum(prob_dict[n][context].values()) + unseen_grams * prob_dict[n][context].default_factory()) <= allowed_error)
