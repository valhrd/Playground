import random

winMasks = [
    0b00000000000000000000000000101010,
    0b00000000000000000000101010000000,
    0b00000000000000101010000000000000,
    0b00000000000000000010000010000010,
    0b00000000000000001000001000001000,
    0b00000000000000100000100000100000,
    0b00000000000000100000001000000010,
    0b00000000000000000010001000100000,
]

def evaluate(grid):
    
    fillMask = 0b00000000000000101010101010101010
    squaresFilled = fillMask & grid

    for mask in winMasks:
        newMask = mask | (mask >> 1)
        res = grid & newMask
        if res == newMask:
            return (True, -1)
        elif res == mask:
            return (True, 1)

    return (squaresFilled == fillMask, 0)

def valid(row, col):
    return 0 <= row < 3 and 0 <= col < 3

def printGrid(grid):
    print("-------------------------------")
    res = [[],[],[]]
    i = 0
    for i in range(9):
        res[i // 3].append('X' if grid & 3 == 3 else ('O' if grid & 3 == 2 else ''))
        grid >>= 2
    for row in res:
        print(row)

def makeMove(grid, available, row, col, player):
    mask = 3 if player == -1 else 2
    grid ^= (mask << 2 * (3 * row + col))
    available[0] ^= (mask << 2 * (3 * row + col))
    printGrid(grid)
    return grid

def ticTacToeBot(grid, available, advPlayer):

    moves = []
    def miniMax(grid, available, alpha, beta, maximise, depth, currDepth):
        endGame, currEval = evaluate(grid)

        if endGame:
            return currEval
        
        mask = 3 if maximise == -1 else 2
        resEval = 1 if maximise == -1 else -1

        for i in range(9):
            if available[0] & (2 << (2 * i)) == 0:
                available[0] ^= (3 << (2 * i))
                grid ^= (mask << (2 * i))
                tempEval = miniMax(grid, available, alpha, beta, -maximise, depth, currDepth - 1)
                available[0] ^= (3 << (2 * i))
                grid ^= (mask << (2 * i))

                if maximise == -1:
                    resEval = min(resEval, tempEval)
                    beta = min(beta, tempEval)
                else:
                    resEval = max(resEval, tempEval)
                    alpha = max(alpha, tempEval)

                if depth == currDepth:
                    moves.append((tempEval, i // 3, i % 3))

                if alpha >= beta:
                    break

        return resEval
    
    eval = miniMax(grid, available, -float('inf'), float('inf'), advPlayer, size(available[0]), size(available[0]))
    print(f"Evaluation for {'X' if advPlayer == -1 else 'O'}: {eval}")
    moves.sort(key = lambda x: x[0], reverse = False if advPlayer == -1 else True)
    while len(moves) > 1 and moves[-1][0] == -advPlayer:
        moves.pop()
    randMove = random.randrange(0, len(moves))
    return makeMove(grid, available, moves[randMove][1], moves[randMove][2], advPlayer)

def size(bit):
    bit &= 0b00000000000000101010101010101010
    res = 0
    for i in range(9):
        if bit & (3 << (2 * i)) == 0:
            res += 1
    print(f"Occupied spaces: {res}")
    return res

players = {'X': -1, 'O': 1}
available = [0]
chosenPlayer = 0
currPlayer = 0
grid = 0

'''board = [["","O",""],
        ["","X",""],
        ["","",""]]

def occupy(available, squares):
    for n in squares:
        available[0] ^= (2 << 2 * n)

def convert(grid):
    res = 0
    shift = 0
    for i in range(9):
        c = grid[i // 3][i % 3]
        mask = 0
        if c == 'X':
            mask = 3
        elif c == 'O':
            mask = 2
        res ^= (mask << shift)
        shift += 2
    return res

grid = convert(board)
occupy(available, [1,4])

print(available)
print(ticTacToeBot(grid, available, -1))'''


'''while True:
    player = input("Play as X or O? ")
    if player not in players:
        print("Enter a valid player")
        continue
    else:
        currPlayer = players[player]
        chosenPlayer = currPlayer
        break

while True:
    if currPlayer != chosenPlayer:
        grid = ticTacToeBot(grid, available, -chosenPlayer)
    else:
        try:
            row = int(input("Enter row (0, 1, 2): "))
            col = int(input("Enter column (0, 1, 2): "))
        except ValueError:
            print("Please enter a valid row and column")
            continue

        if not valid(row, col):
            print("Out of bounds")
            continue
        elif grid & (3 << 2 * (3 * row + col)):
            print("Square occupied")
            continue

        grid = makeMove(grid, available, row, col, chosenPlayer)
    
    endGame, eval = evaluate(grid)
    if endGame:
        if eval < 0:
            print("X wins!")
        elif eval > 0:
            print("O wins!")
        else:
            print("Draw!")
        break
    currPlayer = -currPlayer'''

currPlayer = -1
while True:
    grid = ticTacToeBot(grid, available, currPlayer)
    endGame, eval = evaluate(grid)
    if endGame:
        if eval < 0:
            print("X wins!")
        elif eval > 0:
            print("O wins!")
        else:
            print("Draw!")
        break
    currPlayer = -currPlayer