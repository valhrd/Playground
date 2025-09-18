from collections import Counter

class NgramGenerator:
    def __init__(self, n):
        self.all_ngram_counts = {i:Counter() for i in range(1, n + 1)}

        self.N = n
        self.SOS = '<s>'
        self.EOS = '</s>'

    def generate_ngrams(self, sentence: list) -> Counter:
        sentence = [self.SOS] * (self.N - 1) + sentence + [self.EOS]
        for n in range(1, self.N + 1):
            self.all_ngram_counts[n].update(self.get_ngrams(sentence, n))
        return self.all_ngram_counts

    def get_ngrams(self, sentence: list, n: int) -> Counter:
        ngram_counts = Counter()
        for i in range(len(sentence) - n + 1):
            ngram = tuple(sentence[i: i + n])
            ngram_counts[ngram] += 1
        return ngram_counts
