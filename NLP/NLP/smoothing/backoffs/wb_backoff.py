from NLP.smoothing.backoffs.backoff import Backoff

class WBBackoff(Backoff):
    def strategy(self, ngram_prob_dict, context, word):
        curr_context = context
        curr_n = len(context) + 1
        while curr_context not in ngram_prob_dict[curr_n]:
            curr_context = curr_context[1:]
            curr_n -= 1
        return ngram_prob_dict[curr_n][curr_context][word]