'''
RED = 000
WHITE = 001
BLUE = 010
YELLOW = 011
GREEN = 100
ORANGE = 101
    __
 __|_R|__ __
|_W|_B|_Y|_O|
   |_G|
'''
def colouredSide(num):
    res = 0
    for i in range(9):
        res |= (num << 3 * i)
    return res

solved = []
for i in range(6):
    solved.append(colouredSide(i))

topMask = 0b00000111111111000000000000000000
middleHorizontalMask = 0b00000000000000111111111000000000
bottomMask = 0b00000000000000000000000111111111
leftMask = 0b00000111000000111000000111000000
middleVerticalMask = 0b00000000111000000111000000111000
rightMask = 0b00000000000111000000111000000111

def faceRotateRight(face):
    for i in range(2):
        for j in range(i + 1, 3):
            pass

def upRotate(state):
    left = state[1] & topMask
    front = state[2] & topMask
    right = state[3] & topMask
    back = state[4] & topMask
    for i in range(1, 5):
        state[i] %= (middleHorizontalMask | bottomMask)
    state[1] ^= front
    state[2] ^= right
    state[3] ^= back
    state[4] ^= left

    
    

print(faces)