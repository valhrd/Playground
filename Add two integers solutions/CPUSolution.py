class CPU():
    def __init__(self) -> None:
        self.REGISTERS = {'$' + str(i):0 for i in range(16)}
        self.MAX_INT = (1 << 31) - 1
        self.MIN_INT = -(1 << 31)
        self.INSTRUCTIONS = dict(
            LI=(self.li, 2),
            ADDI=(self.addi, 3)
        )

    def is_valid_reg(self, reg: str, overwritable: bool) -> bool:
        try:
            if overwritable:
                return 1 <= int(reg[1:]) < 16
            return 0 <= int(reg[1:]) < 16
        except:
            raise Exception("Invalid register name")
    
    def is_within_32bit(self, imm: int) -> bool:
        try:   
            return self.MIN_INT <= int(imm) <= self.MAX_INT
        except:
            raise ValueError("Not an integer")
    
    def li(self, rs: str, imm: str) -> None:
        if not self.is_within_32bit:
            raise Exception("Not within 32-bit limit")
        if not self.is_valid_reg(rs, True):
            raise Exception("Invalid register")
        self.REGISTERS[rs] = int(imm)

    def addi(self, rd: str, rs: str, imm: str) -> None:
        if not self.is_within_32bit(imm):
            raise Exception("Invalid immediate value")
        if not self.is_valid_reg(rd, False) or not self.is_valid_reg(rs, True):
            raise Exception("Invalid register")
        self.REGISTERS[rd] = self.REGISTERS[rs] + int(imm)

    def read(self, reg: str) -> int:
        if not self.is_valid_reg(reg, False):
            raise Exception("Can't read")
        return self.REGISTERS[reg]
    
    def parse(self, instruction_list: str):
        cleaned = '\n'.join(line.strip() for line in instruction_list.strip().splitlines())
        instructions = cleaned.split('\n')
        for line in instructions:
            tokens = line.split(" ")
            instruction = tokens[0]
            if instruction not in self.INSTRUCTIONS:
                print(f"Invalid instruction: {instruction}")
                return
            self.execute(instruction, tokens[1:])

    def execute(self, instruction, args):
        func, arg_count = self.INSTRUCTIONS[instruction]
        if arg_count != len(args):
            raise Exception("Incorrect number of arguments")
        func(*args)

class Solution:
    def sum(self, num1: int, num2: int) -> int:
        cpu = CPU()
        target_register = "$1"
        instruction_list =\
        f"""
            LI {target_register} {num1}
            ADDI {target_register} {target_register} {num2}
        """
        cpu.parse(instruction_list)
        return cpu.read(target_register)