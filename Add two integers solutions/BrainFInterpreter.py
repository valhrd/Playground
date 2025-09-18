class BrainFException(Exception):
    pass

class BrainFInterpreter():
    def __init__(self, memory_limit: int):
        self.log("BrainF intepreter does not support inputs from users")

        self.BYTE_LIMIT = 128
        self.JUMP_TO = {}

        self.memory = [0] * memory_limit
        self.pointer = 0
    
    def run(self, code: str) -> str:
        code = self.cleanup(code)

        if not self.is_valid_input(code):
            raise BrainFException("Unmatched square brackets")

        code_pointer = 0
        while code_pointer < len(code):
            c = code[code_pointer]
            match c:
                case '+':
                    self.memory[self.pointer] += 1
                    self.memory[self.pointer] %= self.BYTE_LIMIT
                case '-':
                    self.memory[self.pointer] -= 1
                    self.memory[self.pointer] %= self.BYTE_LIMIT
                case '>':
                    if self.pointer + 1 >= len(self.memory):
                        raise BrainFException("Memory limit exceeded!")
                    self.pointer += 1
                case '<':
                    if self.pointer - 1 < 0:
                        raise BrainFException("Memory pointer cannot go below 0!")
                    self.pointer -= 1
                case ']':
                    if self.memory[self.pointer] != 0:
                        code_pointer = self.JUMP_TO[code_pointer]
                case '.':
                    print(chr(self.memory[self.pointer]), end='', flush=True)
                case _:
                    pass
            code_pointer += 1
        print()
        self.log("Execution complete")
    
    def cleanup(self, code: str) -> str:
        cleaned = '\n'.join(line.strip() for line in code.strip().splitlines())
        cleaned = cleaned.split('\n')
        return "".join(cleaned)
            
    def is_valid_input(self, code: str) -> bool:
        stack = []
        corresponding_right_bracket = {}
        jump_to_dict = {}
        for i in range(len(code)):
            c = code[i]
            if c == '[':
                stack.append(i)
            elif c == ']':
                if not stack:
                    return False
                jump_to_dict[i] = stack.pop()
            else:
                continue
        if stack:
            return False
        self.JUMP_TO = jump_to_dict
        return True
    
    def log(self, msg: str) -> None:
        print(f"<---- {msg} ---->")

    

if __name__ == '__main__':
    bf = BrainFInterpreter(10)
    bf.run('''
        Code to print out "Hello World!"
        >+++++++++
        [
            <++++++++
            >-
        ]
        <
        .
        >+++++++
        [
            <++++
            >-
        ]
        <+
        .
        +++++++
        ..
        +++
        .
        >>>++++++++
        [
            <++++
            >-
        ]
        <
        .
        >>>++++++++++
        [
            <+++++++++
            >-
        ]
        <---
        .
        <<<<
        .
        +++
        .
        ------
        .
        --------
        .
        >>+
        .
        >++++++++++
        .
    ''')