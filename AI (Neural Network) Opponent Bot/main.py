from NeuralNet import *


gameBoard = []


def setBoard(board):
    return ["1", "2", "3", "4", "5", "6", "7", "8", "9"]    # tic-tac-toe grid


def winChecker(board, botMode=False):
    winCheck = [True, 0]
    check1 = []  # column
    check2 = []  # row
    check3 = []  # diagonal 1
    check4 = []  # diagonal 2
    for x in range(len(board)):

        # column check
        check1.append(board[x])
        check1.append(board[(x + 3) % 9])
        check1.append(board[(x + 6) % 9])

        # row check
        if x in [0, 3, 6]:
            check2.append(board[x])
            check2.append(board[x+1])
            check2.append(board[x+2])

        # diagonal check
        if x == 0:  # diagonal 1
            check3.append(board[x])
            check3.append(board[4])
            check3.append(board[8])
        elif x == 6:  # diagonal 2
            check4.append(board[x])
            check4.append(board[4])
            check4.append(board[2])

        allChecks = [check1, check2, check3, check4]
        for x in range(len(allChecks)):     # calculates if there is a winner
            if winCheck[0]:
                if len(set(allChecks[x])) == 1:
                    winCheck[0] = False
                    if allChecks[x][0] == "X":  # checks which player has won
                        winCheck[1] = 1
                    else:
                        winCheck[1] = 2

        check1.clear()
        check2.clear()
        check3.clear()
        check4.clear()

    if botMode:
        return winCheck   # returns both player and Win bool
    else:
        if not winCheck[0]:
            print(f"Player {winCheck[1]} Wins!")
        return winCheck[0]


movesLeft = [1, 2, 3, 4, 5, 6, 7, 8, 9]
rand_Data, basicAI_Data, advancedAI_Data, neuralNetData = [], [], [], []   # data sets for the different Bot Modes


def botTurn(playerNum, mode, turn):

    global movesLeft

    if playerNum == 1:
        icon = "X"
    else:
        icon = "O"

    match mode:
        case 0:     # random bot

            botMove = random.choice(movesLeft)

        case 1:     # basic bot

            turnMoveWeights = rand_Data[turn-1]
            bestMove = 0
            for i in range(len(turnMoveWeights)):
                if i+1 in movesLeft:
                    if turnMoveWeights[i] > bestMove:
                        bestMove = turnMoveWeights[i]
                        botMove = i+1

        case 2:     # advanced bot

            botMove = gameBrain.calculateMove(turn, movesLeft, 1)   # calculates based on an all data trained on


    gameBoard[botMove-1] = icon
    movesLeft.remove(botMove)
    return botMove


playerWins = [0, 0]


def runTest(bot1Mode, bot2Mode, numTests, weightBonus=0, lossPenalty=1):

    global gameBoard, movesLeft, neuralNetData, playerWins
    randTesting = True
    testsRan = 0
    dataSave = []
    p1Wins, p2Wins = 0, 0

    while randTesting:

        movesLeft = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        randGameOn = True
        gameBoard = setBoard(gameBoard)  # not needed but to see games
        gameData = []
        draw = False

        while randGameOn:

            turnOn = len(gameData)
            if turnOn == 6:
                print(gameBoard)
            p1Move = botTurn(1, bot1Mode, turnOn)
            if len(movesLeft) != 0:
                p2Move = botTurn(2, bot2Mode, turnOn)
            else:
                draw = True

            winInfo = winChecker(gameBoard, True)   # winInfo[0] = win, [1] = player
            gameData.append([winInfo[0], winInfo[1], p1Move, p2Move])

            if not winInfo[0] or draw:  # ends game if there is a winner or draw
                randGameOn = False

        dataSave.append(gameData)

        testsRan += 1
        if testsRan >= numTests:
            randTesting = False

    turnMoves = []
    allTurnMoves = []

    for x in dataSave:
        gameIsWon = False
        if len(x) == 5:     # checks if it is a draw or win
            if not x[4][0]:
                gameIsWon = True
        elif len(x) < 5:
            gameIsWon = True

        playerWhoWon = x[len(x)-1][1]

        # saves winning moves and player data
        if gameIsWon:
            if playerWhoWon == 1:
                p1Wins += 1
            else:
                p2Wins += 1
            turnMoves.clear()
            for turn in x:
                turnMove = turn[playerWhoWon+1]
                turnMoves.append(turnMove)
            allTurnMoves.append(turnMoves[0:])

            # NeuralNet reinforcement learning value distribution
            if bot1Mode == 2 and playerWhoWon == 1:     # for position 1 win
                for turn in range(len(turnMoves)):
                    gameBrain.addWeight(turn, turnMoves[turn]-1, weightBonus)
            elif bot1Mode == 2 and playerWhoWon == 2:   # for position 1 loss
                for turn in range(len(turnMoves)):
                    gameBrain.setWeight(turn, turnMoves[turn] - 1, gameBrain.nnNet[turn][turnMoves[turn]-1].weight / lossPenalty)
            if bot2Mode == 2 and playerWhoWon == 2:     # for position 2 win
                for turn in range(len(turnMoves)):
                    gameBrain.addWeight(turn, turnMoves[turn]-1, weightBonus)
            elif bot2Mode == 2 and playerWhoWon == 1:   # for position 2 loss
                for turn in range(len(turnMoves)):
                    gameBrain.setWeight(turn, turnMoves[turn] - 1, gameBrain.nnNet[turn][turnMoves[turn]-1].weight / lossPenalty)


    # only sets nn data if nn is not being tested
    if bot1Mode not in [0, 2] and bot2Mode not in [0, 2]:
        neuralNetData += allTurnMoves                            # add cross validation here!
        #neuralNetData = allTurnMoves

    turnChoices = [[], [], [], [], []]
    for i in allTurnMoves:
        for k in range(len(i)):
            turnChoices[k].append(i[k])

    # 9 probabilities for each of the 5 turns possible
    turnProbs = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    # gets the max amount of turns of games (5)
    for turn in range(len(turnChoices)):
        for move in turnChoices[turn]:
            turnProbs[turn][move-1] += 1

    playerWins = [p1Wins, p2Wins]
    return turnProbs


# Model Accuracy Eval Metrics
win_Ratio = 0
winDraw_Ratio = 0
goalDeviation = 0



def calcEvalStats(playerNum, goalRatio, totalGames):

    # sets proper index for playerWins retrival
    playerNum = (playerNum-1) % 2
    opNum = (playerNum+1) % 2

    global win_Ratio, winDraw_Ratio, goalDeviation

    draws = totalGames - (playerWins[playerNum] + playerWins[opNum])
    win_Ratio = playerWins[playerNum] / totalGames
    winDraw_Ratio = (playerWins[playerNum] + draws) / totalGames
    goalDeviation = (winDraw_Ratio - goalRatio) * 100  # goal deviation from desired value


def getEvalStats(playerNum):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~")
    #print("PLAYER", playerNum, "STATS:")
    print("Win Ratio:       ", win_Ratio)
    print("Win/Draw Ratio:  ", winDraw_Ratio)
    print("Goal Deviation:  ", end="")
    if goalDeviation > 0:
        print("+", end="")
    print(round(goalDeviation, 2), end="%\n")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~")


# synthetic data creation
rand_Data = runTest(0, 0, 1000)
runTest(1, 0, 1000)
runTest(0, 1, 1000)
runTest(1, 1, 1000)


total_win_Ratio = 0
total_winDraw_Ratio = 0
total_goalDeviation = 0
total_EvalTests = 0

testAI_numTests = 100
testAI_weight = 1
testAI_penalty = 1


# AImode: 1 = p1 | 2 = p2 | 3 = both
# opMode: 0 = rand | 1 = basic | 2 = AI | 3 = rand+basic | 4 = all
def testAIModes(AImode, opMode, iterations=1, recurse=False):

    global total_win_Ratio, total_winDraw_Ratio, total_goalDeviation, total_EvalTests
    value = []

    for i in range(iterations):
        if AImode >= 3:
            testAIModes(1, opMode, iterations, True)
            testAIModes(2, opMode, iterations, True)
        elif AImode in [2, 4]:
            pass
            #gameBrain.resetWeights()

        if AImode < 3:
            if opMode == 3:  # recursively runs other opMode tests
                testAIModes(AImode, 0, iterations, True)
                testAIModes(AImode, 1, iterations, True)
            elif opMode >= 4:  # recursively runs other opMode tests
                testAIModes(AImode, 3, iterations, True)
                testAIModes(AImode, 2, iterations, True)
            else:
                if AImode == 1:
                    value = runTest(2, opMode, testAI_numTests, testAI_weight, testAI_penalty)
                if AImode == 2:
                    value = runTest(opMode, 2, testAI_numTests, testAI_weight, testAI_penalty)
                total_win_Ratio += win_Ratio
                total_winDraw_Ratio += winDraw_Ratio
                total_goalDeviation += goalDeviation
                total_EvalTests += 1
                calcEvalStats(1, .5, testAI_numTests)
                #print("AI = Player", AImode, " : Bot Mode =", opMode)
                #getEvalStats(AImode)
                #gameBrain.printWeights()

    # for final evaluation calculation
    if not recurse:
        total_win_Ratio = round(total_win_Ratio/total_EvalTests, 4)
        total_winDraw_Ratio = round(total_winDraw_Ratio/total_EvalTests, 4)
        total_goalDeviation = round(total_goalDeviation/total_EvalTests, 4)
        print("TOTALS:")
        print("Total Win Ratio:", total_win_Ratio)
        print("Total Win/Draw Ratio:", total_winDraw_Ratio)
        print("Total Goal Deviation:", total_goalDeviation, end="%\n")
        print("Total Evaluation Test:", total_EvalTests)

        total_win_Ratio, total_winDraw_Ratio, total_goalDeviation, total_EvalTests = 0, 0, 0, 0


gameBrain = NeuralNet(neuralNetData, 5, 9)

# AImode: 1 = p1 | 2 = p2 | 3 = both
# opMode: 0 = rand | 1 = basic | 2 = AI | 3 = rand+basic | 4 = all
#testAIModes(3, 4, 2)


bestWeight, bestPenalty = 1, 1


def parameterTuning(numIterations, weightRange, penaltyRange, evalMetric, lesserValue):

    global testAI_weight, testAI_penalty, bestWeight, bestPenalty

    for i in range(numIterations):

        bestEval = 0

        for k in range(weightRange):
            testAIModes(3, 4, 1, True)
            if lesserValue:
                match evalMetric:
                    case 0:  # win ratio
                        newEval = round(total_win_Ratio / total_EvalTests, 4)
                    case 1:  # win/draw ratio
                        newEval = round(total_winDraw_Ratio / total_EvalTests, 4)
                    case 2:  # goal deviation
                        newEval = round(total_goalDeviation / total_EvalTests, 4)
                if newEval <= bestEval:
                    bestEval = newEval
                    bestWeight = k
            else:
                newEval = 0
                if newEval >= bestEval:
                    bestEval = newEval
                    bestWeight = k
            testAI_weight += 1
        testAI_weight = bestWeight

        for k in range(penaltyRange):
            testAIModes(3, 4, 1, True)
            if lesserValue:
                match evalMetric:
                    case 0:  # win ratio
                        newEval = round(total_win_Ratio / total_EvalTests, 4)
                    case 1:  # win/draw ratio
                        newEval = round(total_winDraw_Ratio / total_EvalTests, 4)
                    case 2:  # goal deviation
                        newEval = round(total_goalDeviation / total_EvalTests, 4)
                if newEval < bestEval:
                    bestEval = newEval
                    bestPenalty = k
            else:
                newEval = 0
                if newEval > bestEval:
                    bestEval = newEval
                    bestPenalty = k
            testAI_penalty += 1
        testAI_penalty = bestPenalty

    #print(bestWeight, bestPenalty)


print("Before Optimization:")
testAIModes(3, 4, 1)
parameterTuning(10, 10, 10, 10, False)      # parameterTuning(numIterations, weightRange, penaltyRange, evalMetric, lesserValue)
print("\nAfter Optimization:")
testAIModes(3, 4, 1)


def playerTurn(playerNum):
    if playerNum == 1:
        icon = "X"
    else:
        icon = "O"
    square = input("Select an open Square: ")
    if square in gameBoard:
        index = gameBoard.index(square)
        if gameBoard[index] in ["X", "O"]:
            print("ERROR: Please choose an open Square")
            playerTurn(playerNum)
        else:
            gameBoard[index] = icon
    else:
        print("ERROR: Please choose an open Square")
        playerTurn(playerNum)

    movesLeft.remove(int(square))


'''
print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")     # separates AI Model from Player-AIbot Match-Up


gameOn = True
gameBoard = setBoard(gameBoard)
gameStarted = False
while gameOn:

    if not gameStarted:
        player = 0
        while player not in [1, 2]:
            player = int(input("Select Player: 1 or 2?\n\n"))
            print()
            if player not in [1, 2]:
                print("ERROR: Please choose either '1' or '2'")
            else:
                gameStarted = True
                gameTurn = 0
                movesLeft = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    if player == 1:

        print(gameBoard[0], gameBoard[1], gameBoard[2])
        print(gameBoard[3], gameBoard[4], gameBoard[5])
        print(gameBoard[6], gameBoard[7], gameBoard[8])

        playerTurn(1)

        botTurn(2, 2, gameTurn)

    else:

        botTurn(1, 2, gameTurn)

        print(gameBoard[0], gameBoard[1], gameBoard[2])
        print(gameBoard[3], gameBoard[4], gameBoard[5])
        print(gameBoard[6], gameBoard[7], gameBoard[8])

        playerTurn(2)

    gameOn = winChecker(gameBoard)

    gameTurn += 1

    if not gameOn:
        newGame = input("\nEnter y to play again: ")
        if newGame == "y":
            gameOn = True
            gameBoard = setBoard(gameBoard)
            gameTurn = 0
            gameStarted = False

'''

