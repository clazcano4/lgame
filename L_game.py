'''
At a minimum, your program should do the following:

-Implement minimax and heuristic alpha-beta pruning 
    (up to a user-provided depth d, possibly infinite).
-Implement a heuristic evaluation function.
-Define a representation for the states, legal actions and the result of applying a 
    egal action to a state.
-Plot the board and pieces as the game progresses.
-Take as input from the keyboard a human move.

Note: you must represent this as in the following example: 1 2 E 4 3 1 1 
where (1,2) are the (x,y) coordinates of the corner of the L (where (1,1) is 
the top left grid position) and E is the orientation of the foot of 
the L (out of North, South, East, West); and a neutral piece is moved 
from (4,3) to (1,1). If not moving a neutral piece, omit the part 4 3 1 1.
Implement three versions: human vs human, human vs computer, computer vs computer.
Your implementation should be efficient, in particular regarding the use of appropriate 
data structures. Runtime will be a part of the assignment grade.
You are encouraged to go beyond these minimum requirements and the grade will reflect your 
effort. For example, you could improve the user interface to get a suggested move from the 
computer if the human asks for it; to replay the last n moves; to undo the 
last n moves; to switch to computer-vs-computer play; to rotate or flip the 
board (to aid visualization for the human); to save the game; etc. The plot of 
the board could be as simple as ASCII text symbols, or as fancy as you like.
'''
import sys
import main
from functions import *
from somepackage import util

class Player:   # class where each player's moves and evaluation functions will be stored

    def getMove(self, gameState):
        legalMoves = gameState.getLegalMoves() # returns legal moves of gameState
    
    def getPastMoves(self, currentGameState):
        return self.stack # returns list of past moves made by player

    def evaluationFunction(self, currentGameState, move):
        util.raiseNotDefined()

    def scoreEvaluationFunction(currentGameState):
        util.raiseNotDefined()

#L piece orientation
class GameState:
    def __init__(self, playerOne, playerTwo, neutralPieceOne, neutralPieceTwo):
        self.grid_size = 4  
        self.player_one = playerOne  #Position and orientation for Player 1's L-piece
        self.player_two = playerTwo  #Position and orientation for Player 2's L-piece
        self.neutral_piece_one = neutralPieceOne  #Position of first neutral piece
        self.neutral_piece_two = neutralPieceTwo  #Position of second neutral piece
    
    # def generateSuccessor(self)

    # def getValue(self)

    # def getNumAgents(self)

    # def evaluationFunction(self)

    


            
