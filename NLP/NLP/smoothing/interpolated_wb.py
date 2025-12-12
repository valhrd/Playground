from collections import defaultdict, Counter

from NLP.smoothing.smoothing import Smoothing
from NLP.smoothing.utils import NgramProbDict
from NLP.smoothing.backoffs import WBBackoff

class InterpolatedWittenBell(Smoothing):
    def __init__(self, unseen):
        super().__init__()
        self.Z = unseen

    def __call__(self, ngrams: dict) -> NgramProbDict:
        processed_ngrams = self.process_ngrams(ngrams)
        unigrams = ngrams[1]
        wb_probs = {}
        for n in ngrams:
            backoff_probs = None if (n - 1) not in ngrams else wb_probs[n - 1]
            wb_probs[n] = self.generate_known_probs(n, ngrams, processed_ngrams, unigrams, backoff_probs)
        return NgramProbDict(wb_probs, backoff=WBBackoff())
    
    def generate_known_probs(self, n, ngrams, processed_ngrams, unigrams, backoff_probs):
        wb_ngram_probs = defaultdict(lambda: defaultdict())
        if n == 1:
            N = sum(unigrams.values())
            T = len(unigrams)
            wb_ngram_probs[self.EPSILON] = defaultdict(
                lambda t=T, n=N, z=self.Z: (t / (n + t)) / z
            )
            wb_ngram_probs[()].update({word: count / (N + T) for word, count in unigrams.items()})
        else:
            for context in ngrams[n - 1]:
                LMDA = self.lmda(context, n, ngrams, processed_ngrams)

                unseen_backoff_prob = backoff_probs[context[1:]].default_factory()
                wb_ngram_probs[context] = defaultdict(
                    lambda lmda=LMDA, ub=unseen_backoff_prob: (1 - lmda) * ub
                )

                for next_word in unigrams:
                    ml_prob = ngrams[n][context + next_word] / ngrams[n - 1][context]
                    wb_backoff_prob = backoff_probs[context[1:]].get(next_word, backoff_probs[context[1:]].default_factory())
                    wb_ngram_probs[context][next_word] = LMDA * ml_prob + (1 - LMDA) * wb_backoff_prob

        return wb_ngram_probs


    def lmda(self, context, n, ngrams, processed_ngrams):
        context_count = ngrams[n - 1][context]
        LMDA = 0
        if context_count > 0:
            LMDA = context_count / (context_count + len(processed_ngrams[n][context]))
        return LMDA
