from NLP.smoothing.backoffs.backoff import Backoff

class StupidBackoff(Backoff):
    def strategy(self, ngram_prob_dict, context, word):
        pass