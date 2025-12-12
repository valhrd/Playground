class ProbDictError(Exception):
    def __init__(self, message):
        super().__init__(message)

class NgramProbDict(dict):
    def __init__(self, prob_dict: dict, backoff=None, use_backoff=True):
        self.main_dict = prob_dict
        self.use_backoff = use_backoff
        self.backoff = backoff
    
    def __call__(self, context: tuple[str], word: tuple[str]) -> float:
        assert len(word) == 1

        n = len(context) + 1
        subdict = self.main_dict[n]

        if not self.use_backoff:
            return subdict[context][word]

        if context in subdict:
            return subdict[context][word]
        else:
            if self.backoff is None:
                raise ProbDictError(f"Context is not in dictionary and no backoff was provided")
            return self.backoff.strategy(self.main_dict, context, word)
    
    def overwrite_backoff(self, new_backoff):
        self.backoff = new_backoff