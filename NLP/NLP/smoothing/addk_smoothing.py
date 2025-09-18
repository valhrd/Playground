from collections import defaultdict

from NLP.smoothing.smoothing import Smoothing
from NLP.smoothing.utils import NgramProbDict

class AddKSmoothing(Smoothing):
    def __init__(self, k, vocab_size):
        super().__init__()
        self.k = k
        self.V = vocab_size

    def __call__(self, ngrams: dict) -> NgramProbDict:
        assert 1 in ngrams

        smoothed_probs = {}
        for n in ngrams:
            assert isinstance(n, int) and n > 0
            smoothed_probs[n] = self.get_smoothed_ngrams(ngrams, n)
        return NgramProbDict(smoothed_probs, use_backoff=False)

    def get_smoothed_ngrams(self, ngrams, n):
        unigrams = ngrams[1]
        N = sum(unigrams.values())
        if n == 1:
            smoothed_ngrams = defaultdict(lambda: defaultdict(lambda: self.k / (N + self.k * self.V)))
            for w, count in unigrams.items():
                smoothed_ngrams[self.EPSILON][w] = (count + self.k) / (N + self.k * self.V)
        else:
            smoothed_ngrams = defaultdict(lambda: defaultdict(lambda: 1 / self.V))
            for gram, count in ngrams[n].items():
                context = gram[:-1]
                word = gram[-1:]
                smoothed_ngrams[context].default_factory = (
                    lambda ctx=context: self.k / (ngrams[n - 1][ctx] + self.k * self.V)
                )
                smoothed_ngrams[context][word] = (count + self.k) / (ngrams[n - 1][context] + self.k * self.V)
        return smoothed_ngrams


class LaplaceSmoothing:
    def __init__(self, vocab_size):
        self.V = vocab_size

    def __call__(self, ngrams):
        return AddKSmoothing(1, self.V)(ngrams)