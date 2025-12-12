def evaluate(grid):

    for row in grid:
        if row[0] and row[0] == row[1] and row[1] == row[2]:
            return (True, -1 if row[0] == 'X' else 1)
    
    for col in range(len(grid[0])):
        if grid[0][col] and grid[0][col] == grid[1][col] and grid[0][col] == grid[2][col]:
            return (True, -1 if grid[0][col] == 'X' else 1)
    
    if grid[0][0] and grid[0][0] == grid[1][1] and grid[1][1] == grid[2][2]:
        return (True, -1 if grid[0][0] == 'X' else 1)
    
    if grid[0][2] and grid[0][2] == grid[1][1] and grid[1][1] == grid[2][0]:
        return (True, -1 if grid[0][2] == 'X' else 1)
    
    filled = sum([sum([1 if square else 0 for square in row]) for row in grid])

    return (True if filled == 9 else False, 0)

def valid(row, col):
    return not (row < 0 or row >= 3 or col < 0 or col >= 3)

def printGrid(grid):
    print("-------------------------------------------------------")
    for row in grid:
        print(row)

def makeMove(grid, available, row, col, player):
    grid[row][col] = 'X' if player == -1 else 'O'
    available.remove((row, col))
    printGrid(grid)

def ticTacToeBot(grid, available, advPlayer):

    moves = []
    def miniMax(grid, available, maximise, depth, currDepth):
        endGame, currEval = evaluate(grid)
        if endGame:
            return currEval

        resEval = None
        for nextRow, nextCol in available:
            remaining = available.copy()
            remaining.remove((nextRow, nextCol))
            grid[nextRow][nextCol] = 'X' if maximise == -1 else 'O'
            tempEval = miniMax(grid, remaining, -maximise, depth, currDepth - 1)
            if resEval is None:
                resEval = tempEval
            else:
                resEval = min(resEval, tempEval) if maximise == -1 else max(resEval, tempEval)
            if depth == currDepth:
                moves.append((tempEval, nextRow, nextCol))
            grid[nextRow][nextCol] = ''
        
        return resEval
    
    miniMax(grid, available, advPlayer, len(available), len(available))
    moves.sort(key = lambda x: x[0], reverse = False if advPlayer == -1 else True)
    makeMove(grid, available, moves[0][1], moves[0][2], advPlayer)
    

players = {'X': -1, 'O': 1}
available = set([(i, j) for i in range(3) for j in range(3)])
chosenPlayer = 0
currPlayer = 0
grid = [["","",""],
        ["","",""],
        ["","",""]]

while True:
    player = input("Play as X or O? ")
    if player not in players:
        print("Enter a valid player")
        continue
    else:
        chosenPlayer = players[player]
        currPlayer = chosenPlayer
        break

while True:
    if currPlayer != chosenPlayer:
        ticTacToeBot(grid, available, -chosenPlayer)
    else:
        try:
            row = int(input())
            col = int(input())
        except ValueError:
            print("Please enter a valid row and column")
            continue

        if not valid(row, col):
            print("Out of bounds")
            continue
        elif grid[row][col]:
            print("Square occupied")
            continue

        makeMove(grid, available, row, col, chosenPlayer)
    
    endGame, eval = evaluate(grid)
    if endGame:
        printGrid(grid)
        if eval == -1:
            print("X wins!")
        elif eval == 1:
            print("O wins!")
        else:
            print("Draw!")
        break
    currPlayer = -currPlayer
    