from collections import defaultdict

from NLP.smoothing.smoothing import Smoothing
from NLP.smoothing.utils import NgramProbDict

# TODO: implement this
class KneserNeySmoothing(Smoothing):
    def __init__(self, discount):
        super().__init__()
        self.d = discount

    def __call__(self, ngrams: dict) -> NgramProbDict:
        processed_ngrams = self.process_ngrams(ngrams)
        unigrams = ngrams[1]
        kn_probs = {}
        for n in ngrams:
            backoff_probs = None if (n - 1) not in ngrams else kn_probs[n - 1]
            kn_probs[n] = self.generate_kn_ngrams_probs(n, ngrams, processed_ngrams, unigrams, backoff_probs)
        return NgramProbDict(kn_probs, use_backoff=False)

    def generate_kn_ngrams_probs(self, n, ngrams, processed_ngrams, unigrams, backoff_probs):
        kn_ngram_probs = defaultdict(lambda: defaultdict(int))
        if n == 1:
            kn_ngram_probs[self.EPSILON] = self.generate_continuation_probs(unigrams, ngrams)
        else:
            for context in ngrams[n - 1]:
                LMDA = self.lmda(context, ngrams, processed_ngrams)

                kn_ngram_probs[context] = defaultdict(int)
                context_count = ngrams[n - 1][context]

                for next_word in unigrams:
                    next_word_count = ngrams[n][context + next_word]
                    main_term = max(next_word_count - self.d, 0) / context_count
                    backoff_term = LMDA * backoff_probs[context[1:]][next_word]
                    kn_ngram_probs[context][next_word] = main_term + backoff_term

        return kn_ngram_probs

    def generate_continuation_probs(self, unigrams: dict, ngrams: dict):
        continuation_probs = defaultdict(int)
        bigrams = ngrams[2]
        total_unique_bigrams = len(bigrams)
        for word in unigrams:
            context_count = 0
            for bigram in bigrams:
                if word == bigram[1:]:
                    context_count += 1
            continuation_probs[word] = context_count / total_unique_bigrams
        return continuation_probs
    
    def lmda(self, context, ngrams, processed_ngrams):
        n = len(context) + 1
        unique_next_word_count = len(processed_ngrams[n][context])
        context_count = ngrams[n - 1][context]
        LMDA = (self.d * unique_next_word_count) / context_count
        return LMDA
