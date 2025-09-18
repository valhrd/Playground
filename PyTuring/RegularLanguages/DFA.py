from typing import Set, Dict

class FAException(Exception):
    pass

class DFA:
    def __init__(self, states: Set[str], alphabet: str, transitions: str, q0: str, accepting_states: Set[str]):
        assert q0 in states
        for state in accepting_states:
            if state not in states:
                raise FAException("Set of accepting states is not a subset of set of all states")
            
            self.STATES = states
            self.ALPHABET = alphabet
            self.START_STATE = q0
            self.ACCEPTING_STATES = accepting_states
            self.TRANSITIONS = self.parse(transitions)
        
    def parse(self, transitions: str) -> Dict[Dict]:
        pass