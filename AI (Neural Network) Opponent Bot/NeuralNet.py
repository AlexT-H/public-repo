import random


class Node:

    #personalWeights = 0    # for prob adjustments (if needed)
    weight = 1  # change weights based on mode (if loss - | if win +)
    probs = []  # move probabilities


    def __init__(self, probs):
        self.probs = probs


class NeuralNet:

    nnNet = []
    nnData = []


    def addColumn(self):
        self.nnNet.append([])   # adds another list to nn


    def addNode(self, column, probs):   # probs need to be  win weights based on move
        self.nnNet[column].append(Node(probs))


    def __init__(self, nnData, turns, numMoves):

        self.nnData = nnData

        defaultProbs = []
        for moves in range(numMoves):
            defaultProbs.append(1)

        for i in range(turns):
            self.addColumn()
            for k in range(numMoves):
                self.addNode(i, defaultProbs)

        # sets initial column probs
        for games in self.nnData:
            self.nnNet[0][games[0]-1].weight += 1

        for i in range(turns-1):
            for game in self.nnData:
                if i < (len(game)-1):
                    self.nnNet[i][game[i]-1].probs[game[i]-1] += 1  # adds a prob point for each next move that's successful


    def calculateMove(self, turnOn, movesLeft, mode=1):

        move = 0

        # modes: absolute (^), ratio (%), [richest (future incentives)]
        match mode:

            case 0:     # 'Absolute' mode: gets move with best weight * probability in a column

                bestMatch = 0

                for x in range(len(self.nnNet[turnOn])):
                    nodeOn = self.nnNet[turnOn][x]
                    for y in range(len(nodeOn.probs)):
                        if y in movesLeft:
                            if (nodeOn.weight * nodeOn.probs[y]) > bestMatch:
                                bestMatch = (nodeOn.weight * nodeOn.probs[y])
                                move = y


            case 1:     # 'Ratio' mode: selects move based on probabilities

                fullTotal = 0
                rowTotals = []

                # adds a total value counter for each row
                for n in range(len(self.nnNet[turnOn])):
                    rowTotals.append(0)

                # gets best move ratio data
                for x in range(len(self.nnNet[turnOn])):
                    nodeOn = self.nnNet[turnOn][x]
                    for y in range(len(nodeOn.probs)):
                        fullTotal += (nodeOn.weight * nodeOn.probs[y])
                        rowTotals[y] += (nodeOn.weight * nodeOn.probs[y])

                # gets a move selection based on probabilities
                offset = random.random()
                for x in range(len(rowTotals)):
                    if x+1 in movesLeft:
                        rowValue = (rowTotals[x] / fullTotal)
                        if offset < rowValue:
                            offset += rowValue
                        else:
                            move = x+1

        if move == 0:
            move = movesLeft[0]
        return move


    def addWeight(self, column, row, newWeight):
        self.nnNet[column][row].weight += newWeight


    def setWeight(self, column, row, newWeight):    # update for movesLeft
        self.nnNet[column][row].weight = newWeight


    def resetWeights(self):
        for column in self.nnNet:
            for row in column:
                row.weight = 1


    def printWeights(self):
        for column in self.nnNet:
            print()
            for row in column:
                print(row.weight, end=", ")
        print()



