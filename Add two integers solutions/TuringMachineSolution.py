class TMException(Exception):
    pass

class DeterministicTuringMachine():
    BLANK = '_'

    def __init__(self, input_alphabet: str, tape_alphabet_only: str, instructions: str, number_of_states: int, q_accept: int, q_reject: int, print_tape=False, in_strict_mode=False) -> None:
        assert q_accept != q_reject
        assert number_of_states > 0
        assert number_of_states > q_accept and number_of_states > q_reject

        self.EMPTY_STRING = ""
        self.START_STATE = 0
        self.ACCEPT_STATE = q_accept
        self.REJECT_STATE = q_reject
        self.TERMINAL_STATES = [self.ACCEPT_STATE, self.REJECT_STATE]
        self.MOVE_DICT = dict(
            L=-1,
            R=1
        )

        self.NUMBER_OF_STATES = number_of_states
        self.INPUT_ALPHABET = set(input_alphabet)
        self.TAPE_ALPHABET = self.INPUT_ALPHABET.union({self.BLANK}).union(set(tape_alphabet_only))

        # Settings
        self.print_tape = print_tape
        self.in_strict_mode = in_strict_mode

        self.INSTRUCTION_DICT = self.parse_instructions(instructions)

        self.tape = [self.BLANK]
        self.head_pos = 0
        self.head_state = self.START_STATE

        self.input = None

    def run(self, input: str) -> bool:
        print(self.INSTRUCTION_DICT)
        self.set_input(input)
        if self.print_tape:
            print(self)
        while self.head_state not in self.TERMINAL_STATES:
            try:
                next_state, char_write, move = self.INSTRUCTION_DICT[self.head_state][self.tape[self.head_pos]]
            except TypeError as e:
                raise TMException(f"An error occurred most likely due to undefined instructions, enable strict mode to ensure this does not happen")

            self.head_state = next_state
            self.tape[self.head_pos] = char_write

            # Head cannot move past left-most end of the tape
            self.head_pos = max(self.head_pos + self.MOVE_DICT[move], 0)
            if self.head_pos >= len(self.tape):
                assert self.head_pos == len(self.tape)
                self.tape.append(self.BLANK)

            if self.print_tape:
                print(self)
            
        if self.head_state == self.ACCEPT_STATE:
            print("String accepted")
            return True
        print("String rejected")
        return False

    def print_tape_setting(self, setting: bool):
        self.print_tape = setting

    def strict_mode_setting(self, setting: bool):
        self.in_strict_mode = setting

    def parse_instructions(self, instructions: str):
        instruction_dict = {state_no: {letter: None for letter in self.TAPE_ALPHABET} for state_no in range(self.NUMBER_OF_STATES) if state_no not in self.TERMINAL_STATES}
        cleaned = '\n'.join(line.strip() for line in instructions.strip().splitlines())
        instructions = cleaned.split('\n')

        for line in instructions:
            pre_instruction, post_instruction = self.tokenise(line)
            q_curr, char_read = pre_instruction
            try:
                q_curr = int(q_curr)
                if q_curr in self.TERMINAL_STATES:
                    raise TMException(f"Cannot assign instruction to accept/reject state {q_curr}")
                if instruction_dict[q_curr][char_read]:
                    raise TMException(f"Instruction already exists for head in state {q_curr} reading letter '{char_read}'")
            except KeyError as e:
                raise TMException(f"Invalid state or input letter {e}")
            except ValueError as e:
                raise TMException(f"Invalid state representation {e}")
            
            next_state, char_write, move = post_instruction

            try:
                if char_write not in self.TAPE_ALPHABET:
                    raise TMException(f"Provided character '{char_write}' is not in the tape alphabet")
                instruction_dict[q_curr][char_read] = (int(next_state), char_write, move)
            except ValueError as e:
                raise TMException(f"Invalid state representation {e}")

        if self.in_strict_mode and not self.is_populated(instruction_dict):
            raise TMException(f"Missing instructions")
        
        return instruction_dict

    def tokenise(self, line):
        tokens = [token.strip() for token in line.split("->")]
        tokens = [token.strip("()").split(",") for token in tokens]
        tokens = [[subtoken.strip() for subtoken in subtokenlist] for subtokenlist in tokens]
        return tokens
    
    def is_populated(self, instruction_dict):
        for state_no in range(self.NUMBER_OF_STATES):
            if state_no in self.TERMINAL_STATES:
                continue
            for letter in self.TAPE_ALPHABET:
                if instruction_dict[state_no][letter] is None:
                    return False
        return True

    def set_input(self, input: str) -> None:
        self.input = input
        self.clear_tape()
        if input == self.EMPTY_STRING:
            return
        
        self.tape.pop()
        for char in input:
            if char not in self.INPUT_ALPHABET:
                raise TMException(f"The character {char} is not a valid input letter.")
            self.tape.append(char)

    def clear_tape(self):
        self.tape = [self.BLANK]

    def __str__(self):
        return f"""
        Head position: {self.head_pos}
        Head state: {self.head_state}
        {[(f"[q{self.head_state}]" if i == self.head_pos else "") + self.tape[i] for i in range(len(self.tape))]}
        """

if __name__ == '__main__':
    """
        Provide instructions in the form of (q_curr, char_read) -> (q_next, char_write, move)
        The initial state q_0 must be represented by 0
        The acceptance and rejection states must be defined and must not be the same
        Move must either be L (left) or R (right)
    """
    blank = DeterministicTuringMachine.BLANK
    q_accept = 9
    q_reject = 10

    instructions = f"""
        (0, 1) -> (1, %, R)
        (1, 1) -> (1, 1, R)
        (1, +) -> (2, 1, R)
        (2, 1) -> (3, +, R)
        (3, 1) -> (3, 1, R)
        (3, _) -> (4, 1, R)
        (4, _) -> (4, $, L)
        (4, 1) -> (4, 1, L)
        (4, +) -> (4, +, L)
        (4, $) -> (4, $, L)
        (4, X) -> (5, X, R)
        (4, %) -> (5, %, R)
        (5, +) -> (5, X, R)
        (5, 1) -> (6, X, R)
        (5, $) -> (7, $, L)
        (6, 1) -> (6, 1, R)
        (6, +) -> (6, +, R)
        (6, $) -> (6, $, R)
        (6, _) -> (4, 1, L)
        (7, X) -> (7, X, L)
        (7, %) -> (8, _, R)
        (8, X) -> (8, _, R)
        (8, $) -> (9, _, R)
    """
    tm = DeterministicTuringMachine("1+", "X$%", instructions, 11, q_accept, q_reject)
    tm.print_tape_setting(True)
    tm.strict_mode_setting(False)
    tm.run("11111+1111")