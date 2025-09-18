import typing

class CFG:
    def __init__(self, grammar: str):
        self.GRAMMAR = self.parse(grammar)

    def parse(self, grammar):
        pass

    def tokenise(self, line):
        tokens = [token.strip() for token in line.split("->")]
        tokens = [token.strip("()").split(",") for token in tokens]
        tokens = [[subtoken.strip() for subtoken in subtokenlist] for subtokenlist in tokens]
        return tokens