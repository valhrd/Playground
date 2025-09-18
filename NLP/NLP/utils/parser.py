import re

class Parser:
    def __init__(self, REGEX=r"\b[a-zA-Z]+(?:'[a-zA-Z]+)?\b"):
        self.REGEX = REGEX

    def tokenize(self, sentence: str):
        sentence = sentence.lower()
        return re.findall(self.REGEX, sentence)