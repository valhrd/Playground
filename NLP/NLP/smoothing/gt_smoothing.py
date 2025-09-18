from collections import defaultdict, Counter

from NLP.smoothing.smoothing import Smoothing
from NLP.smoothing.utils import NgramProbDict

# TODO: implement this
class GoodTuringSmoothing(Smoothing):
    def __init__(self):
        super().__init__()

    def __call__(self, ngrams: dict) -> NgramProbDict:
        unigrams = ngrams[1]
        total_observations = sum(unigrams.values())
        freq_of_counts = Counter(unigrams.values())

        adjusted_counts = {}
        for word in unigrams:
            word_count = unigrams[word]
            adjusted_counts[word] = (word_count + 1) * freq_of_counts[word_count + 1] / word_count
        print(adjusted_counts)