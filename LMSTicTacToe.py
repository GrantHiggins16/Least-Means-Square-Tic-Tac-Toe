import random
import copy

class Game(object):
    """
    class representing a tic tac toe board. Initialized empty
    """
    def __init__(self):
        """
        creates empty board of size 9
        first 3 represent 1 row, 2nd 3 the next, ect
        then defines group of indexes representing different parts of the board
        """
        self.board = [0]*9
        self.col1 = [0, 3, 6]
        self.col2 = [1, 4, 7]
        self.col3 = [2, 5, 8]
        self.row1 = [0, 1 ,2]
        self.row2 = [3, 4, 5]
        self.row3 = [6, 7, 8]
        self.diagonal1 = [0, 4, 8]
        self.diagonal2 = [2, 4, 6]
        self.winConditions = [self.col1, self.col2, self.col3, self.row1, self.row2, self.row3, self.diagonal1, self.diagonal2]

    def __str__(self):
        """
        string rep of board
        """
        translatedList = [0]*9
        for i, val in enumerate(self.board):
            if val == 0:
                translatedList[i] = i
            elif val == 1:
                translatedList[i] = 'X'
            else:
                translatedList[i] = 'O'

        toReturn = ""
        toReturn += str(translatedList[0]) + "|" + str(translatedList[1]) + "|" + str(translatedList[2]) +"\n"
        toReturn += ("------") + "\n"
        toReturn += str(translatedList[3]) + "|" + str(translatedList[4]) + "|" + str(translatedList[5]) + "\n"
        toReturn += ("------") + '\n'
        toReturn += str(translatedList[6]) + "|" + str(translatedList[7]) + "|" + str(translatedList[8]) + '\n'
        return toReturn

    def isValidMove(self, index):
        """
        checks if placin g a char on a certain index is valid
        """
        if index > 8:
            return False
        if self.board[index] != 0:
            return False
        return True

    def placeX(self, index):
        """
        places an x on the board represented by a 1 in the correct index
        """
        assert self.isValidMove(index)
        self.board[index] = 1

    def placeO(self, index):
        """
        places an o on the board represented by a 2 in the correct index
        """
        assert self.isValidMove(index)
        self.board[index] = 2

    def determineWinner(self, boardState):
        """
        returns 0 if no winner, 1 if x wins, 2 if o wins, 3 if draw
        character is 1 or 2 for 'X' or 'O'"
        boardState is a 2-d list. used instead of self.board so this function can be used as a helper function
        """
        for winCondition in self.winConditions:
            if (boardState[winCondition[0]] == boardState[winCondition[1]] == boardState[winCondition[2]]):
                if boardState[winCondition[0]] == 1:
                    #x wins
                    return 1
                elif boardState[winCondition[0]] == 2:
                    #o wins
                    return 2
                else:
                    continue
        #check for draw
        boardFull = True
        for index in boardState:
            if index ==0:
                boardFull = False
        if boardFull:
            return 3
        #else board isnt full and isnt won
        return 0

    def getValidMoves(self):
        """
        returns list of indexes considered valid moves
        """
        validIndexes = []
        for i in range(0, 9):
            if self.isValidMove(i):
                validIndexes.append(i)
        return validIndexes

    def getNumWinningMovesX(self):
        """
        returns number of ways x can win next turn
        """
        validIndexes = self.getValidMoves()
        numWinningMoves = 0
        for index in validIndexes:
            tempBoard = copy.deepcopy(self.board)
            tempBoard[index] = 1
            if (self.determineWinner(tempBoard) == 1):
                numWinningMoves += 1
        return numWinningMoves

    def getNumWinningMovesO(self):
        """
        returns number of ways o can win next turn
        """
        validIndexes = self.getValidMoves()
        numWinningMoves = 0
        for index in validIndexes:
            tempBoard = copy.deepcopy(self.board)
            tempBoard[index] = 2
            if (self.determineWinner(tempBoard) == 2):
                numWinningMoves += 1
        return numWinningMoves

    def getEmptyPaths(self):
        """
        get number of empty rows, columns, and diagonals on a board
        """
        emptyPaths = 0
        boardState = self.board
        for winCondition in self.winConditions:
            if (boardState[winCondition[0]] == boardState[winCondition[1]] == boardState[winCondition[2]] == 0):
                emptyPaths += 1
        return emptyPaths

    def getPaths1(self, char):
        """
        returns number of paths with a single instance of char and nothing else on them
        char is 1 if x, 2 if o
        """
        checkAgainst = [0, 0]
        numPaths = 0
        boardState = self.board
        for winCondition in self.winConditions:
            tocheck = []
            tocheck.append(boardState[winCondition[0]])
            tocheck.append(boardState[winCondition[1]])
            tocheck.append(boardState[winCondition[2]])
            if char in tocheck:
                tocheck.remove(char)
                if tocheck == checkAgainst:
                    numPaths += 1
        return numPaths


class humanPlayer:
    """
    class representing a human player
    """
    def __init__(self, xFlag):
        """
        xFlag, true if player is x, false if player is o
        """
        self.xFlag = xFlag

    def makeMove(self, game):
        """
        makes move based on input from terminal
        """
        char = 0
        if self.xFlag:
            char = 1
        else:
            char = 2
        assert game.determineWinner(game.board) == 0
        validInput = False
        index = 1000
        while (not validInput):
            print(game)
            index = input("Please input index you wish to place your character: ")
            if game.isValidMove(int(index)):
                validInput = True
            else:
                print("That is not a valid input")
        if self.xFlag:
            game.placeX(int(index))
        else:
            game.placeO(int(index))

class RandomPlayer:
    """
    class representing a player who makes random moves
    """
    def __init__(self, xFlag):
        """
        xFlag, true if player is x, false if player is o
        """
        self.xFlag = xFlag

    def makeMove(self, game):
        """makes move based on random number generator"""
        assert game.determineWinner(game.board) == 0
        validMoves = game.getValidMoves()
        index = random.randint(0, (len(validMoves) - 1))
        move = validMoves[index]
        assert game.isValidMove(move)
        if self.xFlag:
            game.placeX(move)
        else:
            game.placeO(move)


class TicTacToeMachine:
    """
    class representing a learning tic tac toe player
    learns via the least means square method
    """
    def __init__(self, xFlag):
        """
        xFlag, true if player is x false if player is o
        emptypaths = number of empty cols, rows, and diagonals
        paths1 = number of cols, rows, and diagonals with 1 user char and nothing else
        paths2 = number of cols, rows, and diagonals with 2 user chars and nothing else
        win = 1 if user has won and 0 otherwise
        loss = 1 if user has lost and 0 otherwise
        draw = 1 if user has drawn and 0 otherwise
        oppPaths1 = number of cols, rows and diagonals with 1 opp char and nothing else
        weights are weights to be used with different above variables for LMS
        history is a trace of the current game
        """
        self.xFlag = xFlag
        self.emptyPaths = 0
        self.paths1 = 0
        self.paths2 = 0
        self.win = 0
        self.loss = 0
        self.draw = 0
        self.oppPaths1 = 0
        self.oppPaths2 = 0
        self.emptyPathsW = 1
        self.paths1W = 1
        self.paths2W = 1
        self.winW = 1
        self.lossW = 1
        self.oppPaths1W = 1
        self.oppPaths2W = 1
        self.drawW = 1
        self.generalW = 1
        self.history = []


    def evaluateBoard(self, game):
        """
        assign values for xs in lms equation and then evaluate
        """
        self.emptyPaths = game.getEmptyPaths()
        if self.xFlag:
            self.paths1 = game.getPaths1(1)
            self.paths2 = game.getNumWinningMovesX()
            if game.determineWinner(game.board) == 1:
                self.win = 1
                self.loss = 0
                self.draw = 0
            elif game.determineWinner(game.board) == 2:
                self.loss = 1
                self.win = 0
                self.draw =0
            elif game.determineWinner(game.board) == 3:
                self.draw = 1
                self.win = 0
                self.loss = 0
            else:
                self.draw = 0
                self.win = 0
                self.loss = 0
            self.oppPaths1 = game.getPaths1(2)
            self.oppPaths2 = game.getNumWinningMovesO()
        else:
            self.paths1 = game.getPaths1(2)
            self.paths2 = game.getNumWinningMovesO()
            if game.determineWinner(game.board) == 1:
                self.loss = 1
                self.win = 0
                self.draw = 0
            elif game.determineWinner(game.board) == 2:
                self.win = 1
                self.loss = 0
                self.draw = 0
            elif game.determineWinner(game.board) == 3:
                self.draw = 1
                self.win = 0
                self.loss = 0
            else:
                self.draw = 0
                self.win = 0
                self.loss = 0
            self.oppPaths1 = game.getPaths1(1)
            self.oppPaths2 = game.getNumWinningMovesX()
        estimatedValue = self.generalW + self.emptyPaths * self.emptyPathsW + self.paths1 * self.paths1W + self.paths2 * self.paths2W + self.win * self.winW + self.loss * self.lossW + self.draw * self.drawW + self.oppPaths1 * self.oppPaths1W + self.oppPaths2 * self.oppPaths2W
        return estimatedValue

    def makeMove(self, game):
        """
        finds move with highest value and executes it
        """
        highestValue = -200
        validMoves = game.getValidMoves()
        bestMove = validMoves[0]
        for move in validMoves:
            newGame = Game()
            newGame.board = copy.deepcopy(game.board)
            if self.xFlag:
                newGame.placeX(move)
            else:
                newGame.placeO(move)
            tempValue = self.evaluateBoard(newGame)
            if (tempValue > highestValue):
                bestMove = move
                highestValue = tempValue
        if self.xFlag:
            game.placeX(bestMove)
        else:
            game.placeO(bestMove)
        self.history.append(game.board)

    def critic(self, winValue):
        """
        looks at history and assigns an estimated value, then passes to generalizer
        winvalue, 0 for loss, 1 for win, 2 for draw
        """
        actualVal = 0
        if winValue == 0:
            actualVal = -100
        if winValue == 1:
            actualVal = 100
        for board in self.history:
            gameToEvaluate = Game()
            gameToEvaluate.board = board
            estimatedValue = self.evaluateBoard(gameToEvaluate)
            trainingExample = [actualVal, estimatedValue]
            self.generalizer(trainingExample)
        self.history = []

    def generalizer(self, trainingExample):
        """
        adjusts weights based on LMS equation
        trainingExample is list of size 2, [0] represents resultant value and [1] represents estimated value
        """
        self.emptyPathsW += .1 * (trainingExample[0] - trainingExample[1]) * self.emptyPaths
        self.paths1W += .1 * (trainingExample[0] - trainingExample[1]) * self.paths1
        self.paths2W += .1 * (trainingExample[0] - trainingExample[1]) * self.paths2
        self.winW += .1 * (trainingExample[0] - trainingExample[1]) * self.win
        self.lossW += .1 * (trainingExample[0] - trainingExample[1]) * self.loss
        self.drawW += .1 * (trainingExample[0] - trainingExample[1]) * self.draw
        self.oppPaths1W += .1 * (trainingExample[0] - trainingExample[1]) * self.oppPaths1W
        self.oppPaths2W += .1 * (trainingExample[0] - trainingExample[1]) * self.oppPaths2W
        self.generalW = trainingExample[0] - (self.emptyPathsW + self.paths1W + self.paths2W + self.winW + self.lossW + self.drawW  + self.oppPaths1W + self.oppPaths2W)


def teachProgram(numTests, machine):
    """
    teaches a machine against a random opponent a number of times equal to numTests
    """
    numWins = 0
    numLosses = 0
    numDraws = 0
    xFlag = True
    if machine.xFlag:
        xFlag = False
    randomOpponent = RandomPlayer(xFlag)
    i = 0
    while i < numTests:
        game = Game()
        notOver = True
        if xFlag:
            while (notOver):
                randomOpponent.makeMove(game)
                if (game.determineWinner(game.board) != 0):
                    notOver = False
                    continue
                machine.makeMove(game)
                if (game.determineWinner(game.board) != 0):
                    notOver = False
                    continue
            winner = game.determineWinner(game.board)
            if winner == 2:
                #machine won
                machine.critic(1)
                numWins += 1
            elif winner == 1:
                #machine lost
                machine.critic(0)
                numLosses += 1
            else:
                #machine drew
                machine.critic(2)
                numDraws += 1
        else:
            while (notOver):
                machine.makeMove(game)
                if (game.determineWinner(game.board) != 0):
                    notOver = False
                    continue
                randomOpponent.makeMove(game)
                if (game.determineWinner(game.board) != 0):
                    notOver = False
                    continue
            winner = game.determineWinner(game.board)
            if winner == 1:
                #machine won
                machine.critic(1)
                numWins += 1
            elif winner == 2:
                #machine lost
                machine.critic(0)
                numLosses += 1
            else:
                #machine drew
                machine.critic(2)
                numDraws += 1
        i += 1
    print("Stats against random opponent:")
    print("\tWins: " + str(numWins))
    print("\tLosses: " + str(numLosses))
    print("\tDraws: " + str(numDraws))

if __name__ == "__main__":
    #machine only currently works as intended if machine is Xs
    xFlag = False
    machineX = not xFlag
    machine = TicTacToeMachine(machineX)
    teachProgram(1000, machine)
    user = humanPlayer(xFlag)
    continuePlaying = True
    while (continuePlaying):
        game = Game()
        gameOn = True
        if not xFlag:
            while (gameOn):
                machine.makeMove(game)
                if (game.determineWinner(game.board) != 0):
                    gameOn = False
                    continue
                user.makeMove(game)
                if (game.determineWinner(game.board) != 0):
                    gameOn = False
                    continue
            winner = game.determineWinner(game.board)
            print(game)
            if (winner == 3):
                print("Draw")
            if (winner == 1):
                print("You lose")
            if (winner == 2):
                print("You win")
        else:
            while (gameOn):
                user.makeMove(game)
                if (game.determineWinner(game.board) != 0):
                    gameOn = False
                    continue
                machine.makeMove(game)
                if (game.determineWinner(game.board) != 0):
                    gameOn = False
                    continue
            winner = game.determineWinner(game.board)
            print(game)
            if (winner == 3):
                print("Draw")
            if (winner == 1):
                print("You win")
            if (winner == 2):
                print("You lose")

        selecting = True
        while (selecting):
            answer = input("Play again? (y/n) ")
            if answer == 'y':
                selecting = False
            elif answer == 'n':
                selecting = False
                continuePlaying = False
            else:
                print("invalid input")
