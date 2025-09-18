from abc import ABC, abstractmethod
from collections import Counter, defaultdict

from NLP.smoothing.utils import NgramProbDict

class Smoothing(ABC):

    def __init__(self):
        self.EPSILON = ()

    @abstractmethod
    def __call__(self, ngrams: dict) -> NgramProbDict:
        pass

    def process_ngrams(self, ngrams):
        processed = {}
        for n in ngrams:
            if n == 1:
                grams = Counter({k: v for k, v in ngrams[n].items()})
            else:
                grams = defaultdict(lambda: Counter())
                for gram, count in ngrams[n].items():
                    grams[gram[:-1]][gram[-1:]] = count
            processed[n] = grams
        return processed