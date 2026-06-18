class Board():

    EMPTY = 0
    WHITE = 1
    BLACK = 2

    def __init__(self):

        self.board = [self.EMPTY, self.EMPTY, self.EMPTY,
                      self.EMPTY, self.EMPTY, self.EMPTY,
                      self.EMPTY, self.EMPTY, self.EMPTY ]

        self.turn = self.WHITE

        self.outputIndex = {}
        self.legal_moves = None

        # white forward moves
        self.outputIndex["(6, 3)"] = 0
        self.outputIndex["(7, 4)"] = 1
        self.outputIndex["(8, 5)"] = 2
        self.outputIndex["(3, 0)"] = 3
        self.outputIndex["(4, 1)"] = 4
        self.outputIndex["(5, 2)"] = 5

        # black forward moves
        self.outputIndex["(0, 3)"] = 6
        self.outputIndex["(1, 4)"] = 7
        self.outputIndex["(2, 5)"] = 8
        self.outputIndex["(3, 6)"] = 9
        self.outputIndex["(4, 7)"] = 10
        self.outputIndex["(5, 8)"] = 11

        # white capture moves
        self.outputIndex["(6, 4)"] = 12
        self.outputIndex["(7, 3)"] = 13
        self.outputIndex["(7, 5)"] = 14
        self.outputIndex["(8, 4)"] = 15
        self.outputIndex["(3, 1)"] = 16
        self.outputIndex["(4, 0)"] = 17
        self.outputIndex["(4, 2)"] = 18
        self.outputIndex["(5, 1)"] = 19

        # black pawn moves
        self.outputIndex["(0, 4)"] = 20
        self.outputIndex["(1, 3)"] = 21
        self.outputIndex["(1, 5)"] = 22
        self.outputIndex["(2, 4)"] = 23
        self.outputIndex["(3, 7)"] = 24
        self.outputIndex["(4, 6)"] = 25
        self.outputIndex["(4, 8)"] = 26
        self.outputIndex["(5, 7)"] = 27

        # enumerate fields such that
        # WHITE_PAWN_CAPTURES[FROM IDX] lists all possible
        # target capture squares
        self.WHITE_PAWN_CAPTURES = [
            [],
            [],
            [],
            [1],
            [0,2],
            [1],
            [4],
            [3,5],
            [4]
        ]

        self.BLACK_PAWN_CAPTURES = [
            [4],
            [3,5],
            [4],
            [7],
            [6,8],
            [7],
            [],
            [],
            []
        ]


    def isTerminal(self):
        winner = None
        # black wins if she has placed a pawn on the 0th row
        if(self.board[6] == Board.BLACK or
                self.board[7] == self.BLACK or
                self.board[8] == self.BLACK):
            winner = self.BLACK
        # white wins if he placed a pawn on the 3rd row
        if (self.board[0] == self.WHITE or
                self.board[1] == self.WHITE or
                self.board[2] == self.WHITE):
            winner = self.WHITE
        if(winner != None):
            return (True, winner)
        else:
            # stalemate if there is no winner
            # and current player can't move
            if(len(self.generateMoves()) == 0):
                if(self.turn == Board.WHITE):
                    return (True, Board.BLACK)
                else:
                    return (True, Board.WHITE)
            else:
                return (False, None)

    def toString(self):
        if(self.turn == self.WHITE):
            return "w:"  + "".join([ str(x) for x in self.board])
        else:
            return "b:"  + "".join([ str(x) for x in self.board])

    def toDisplayString(self):
        s = ""
        for i in range(0,3):
            if(self.board[i] == self.WHITE):
                s += "W"
            if(self.board[i] == self.BLACK):
                s += "B"
            if(self.board[i] == self.EMPTY):
                s += "_"
        s += "\n"
        for i in range(3,6):
            if(self.board[i] == self.WHITE):
                s += "W"
            if(self.board[i] == self.BLACK):
                s += "B"
            if(self.board[i] == self.EMPTY):
                s += "_"
        s += "\n"
        for i in range(6,9):
            if(self.board[i] == self.WHITE):
                s += "W"
            if(self.board[i] == self.BLACK):
                s += "B"
            if(self.board[i] == self.EMPTY):
                s += "_"
        s += "\n"
        return s

    # turn the position + turn into
    # input for the network
    def toNetworkInput(self):
        posVec = []
        # white pawns
        for i in range(0,9):
            if(self.board[i] == Board.WHITE):
                posVec.append(1)
            else:
                posVec.append(0)
        # black pawns
        for i in range(0,9):
            if(self.board[i] == Board.BLACK):
                posVec.append(1)
            else:
                posVec.append(0)
        for i in range(0,3):
            if(self.turn == Board.WHITE):
                posVec.append(1)
            else:
                posVec.append(0)
        return posVec

    # given a move, get the index of the correspnding move output
    # of the network
    def getNetworkOutputIndex(self, move):
        return self.outputIndex[str(move)]

    def setStartingPosition(self):

        # BLACK BLACK BLACK
        # ##### ##### #####
        # WHITE WHITE WHITE
        self.board = [self.BLACK, self.BLACK, self.BLACK,
                      self.EMPTY, self.EMPTY, self.EMPTY,
                      self.WHITE, self.WHITE, self.WHITE ]

    def applyMove(self, move):
        fromSquare = move[0]
        toSquare = move[1]
        self.board[toSquare] = self.board[fromSquare]
        self.board[fromSquare] = self.EMPTY
        if(self.turn == self.WHITE):
            self.turn = self.BLACK
        else:
            self.turn = self.WHITE
        self.legal_moves = None

    def generateMoves(self):
        if(self.legal_moves == None):
            moves = []
            for i in range(0, 9):
                if(self.board[i] == self.turn):
                    if(self.turn == self.WHITE):
                        # check if we can move one square up
                        toSquare = i - 3
                        if(toSquare >= 0):
                            if(self.board[toSquare] == self.EMPTY):
                                moves.append((i, toSquare))
                        # check if we can capture to the left or right
                        potCaptureSquares = self.WHITE_PAWN_CAPTURES[i]
                        for toSquare in potCaptureSquares:
                            if(self.board[toSquare] == self.BLACK):
                                moves.append((i, toSquare))
                    if (self.turn == self.BLACK):
                        # check if we can move one square down
                        toSquare = i + 3
                        if(toSquare < 9):
                            if (self.board[toSquare] == self.EMPTY):
                                moves.append((i, toSquare))
                        # check if we can capture to the left or right
                        potCaptureSquares = self.BLACK_PAWN_CAPTURES[i]
                        for toSquare in potCaptureSquares:
                            if (self.board[toSquare] == self.WHITE):
                                moves.append((i, toSquare))
            self.legal_moves = moves
        return self.legal_moves



from keras.models import Model
from keras.layers import *
import tensorflow as tf
from tensorflow import keras
import numpy as np
import copy
import numpy as np

import copy

def minimax(board, depth, maximize):
    isTerminal, winner = board.isTerminal()
    if(isTerminal):
        if(winner == board.WHITE):
            return 1000
        if(winner == board.BLACK):
            return -1000
        if(winner == board.DRAW):
            return 0
    moves = board.generateMoves()
    if(maximize):
        bestVal = -999999999999
        for move in moves:
            next = copy.deepcopy(board)
            next.applyMove(move)
            bestVal = max(bestVal, minimax(next, depth - 1, (not maximize)))
        return bestVal
    else:
        bestVal = 9999999999999
        for move in moves:
            next = copy.deepcopy(board)
            next.applyMove(move)
            bestVal = min(bestVal, minimax(next, depth - 1, (not maximize)))
        return bestVal

def getBestMoveRes(board):
    bestMove = None
    bestVal = 1000000000
    if(board.turn == board.WHITE):
        bestVal = -1000000000
    for m in board.generateMoves():
        tmp = copy.deepcopy(board)
        tmp.applyMove(m)
        mVal = minimax(tmp, 30, tmp.turn == board.WHITE)
        if(board.turn == board.WHITE and mVal > bestVal):
            bestVal = mVal
            bestMove = m
        if(board.turn == board.BLACK and mVal < bestVal):
            bestVal = mVal
            bestMove = m
    return bestMove, bestVal

positions = []
moveProbs = []
outcomes = []

terminals = []

def visitNodes(board):
    term, _ = board.isTerminal()
    if(term):
        terminals.append(1)
        return
    else:
        bestMove, bestVal = getBestMoveRes(board)
        positions.append(board.toNetworkInput())
        moveProb = [ 0 for x in range(0,28) ]
        idx = board.getNetworkOutputIndex(bestMove)
        moveProb[idx] = 1
        moveProbs.append(moveProb)
        if(bestVal > 0):
            outcomes.append(1)
        if(bestVal == 0):
            outcomes.append(0)
        if(bestVal < 0):
            outcomes.append(-1)
        for m in board.generateMoves():
            next = copy.deepcopy(board)
            next.applyMove(m)
            visitNodes(next)



inp = Input ((21 ,) )

l1 = Dense (128 , activation ='relu') ( inp )
l2 = Dense (128 , activation ='relu') ( l1 )
l3 = Dense (128 , activation ='relu') ( l2 )
l4 = Dense (128 , activation ='relu') ( l3 )
l5 = Dense (128 , activation ='relu') ( l4 )

policyOut = Dense (28 , name ='policyHead', activation ='softmax') ( l5 )
valueOut = Dense (1 , activation = 'tanh' , name ='valueHead') ( l5 )

bce = tf . keras . losses . CategoricalCrossentropy ( from_logits = False )
model = Model ( inp , [ policyOut , valueOut ])
model.compile(optimizer='SGD',
    loss={
        'valueHead': 'mean_squared_error',
        'policyHead': bce
    })

model . save ('random_model.keras')

board = Board ()
board . setStartingPosition ()
visitNodes (board)
print ("# of reachable distinct positions :")
np . save ("positions", np . array ( positions ))
np . save ("moveprobs", np . array ( moveProbs ))
np . save ("outcomes", np . array ( outcomes ))
model = keras . models . load_model ("random_model.keras")

inputData = np . load ("positions.npy")
policyOutcomes = np . load ("moveprobs.npy")
valueOutcomes = np . load ("outcomes.npy")

print ( policyOutcomes . shape )

model.fit(inputData ,[policyOutcomes, valueOutcomes], epochs =512,
batch_size =16)
model.save('supervised_model.keras')

model = keras.models.load_model("supervised_model.keras")
# model = keras . models . load_model ("../ common / random_model . keras ")

inputData = np . load ("positions.npy")
policyOutcomes = np . load ("moveprobs.npy")
valueOutcomes = np . load ("outcomes.npy")

print ( policyOutcomes . shape )

model.fit(inputData ,[policyOutcomes, valueOutcomes], epochs =512,
batch_size =16, shuffle=True)
model.save('supervised_model.keras')

model = keras.models.load_model("supervised_model.keras")
# model = keras . models . load_model ("../ common / random_model . keras ")

