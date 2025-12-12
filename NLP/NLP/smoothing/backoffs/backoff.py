from abc import ABC, abstractmethod

class Backoff(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def strategy(self, ngram_probs, context, word):
        pass