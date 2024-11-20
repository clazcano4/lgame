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

    def is_valid(self, x, y, direction):
        #Check if within grid boundaries
        if x < 1 or x > self.grid_size or y < 1 or y > self.grid_size:
            return False

        #Check if position is occupied by Player 1's L-piece
        if (x, y, direction) in self.get_Piece_Position(self.player_one):
            return False

        #Check if position is occupied by Player 2's L-piece
        if (x, y, direction) in self.get_Piece_Position(self.player_two):
            return False

        #Check if position is occupied by any neutral piece
        if (x, y) == self.neutral_piece_one or (x, y) == self.neutral_piece_two:
            return False

        #If all checks pass, the position is valid
        return True
    

    def free_postion(self, x, y):
        occupied_postion = ()

    
    def get_Piece_Position(self, player):
        corner, orientation = player
        x, y = corner

        postions = [(x,y)]
        if orientation == "North":
            postions += [(x, y - 1), (x, y - 2), (x + 1, y - 2), (x + 2, y - 2)]
        elif orientation == "South":
            util.raiseNotDefined()
        elif orientation == "East":
            util.raiseNotDefined()
        elif orientation == "West":
            util.raiseNotDefined()

        return util.raiseNotDefined()

        

    def getLegalMoves(self, player):
        legal_moves = []


            

    #def apply_move():
        #update the L piece postion

    #def getDirection(self):
        # returns agent's current direction 
        #return self.direction

    #def eval():
        #get legal moves for both players
        #calculate the difference in the number of moves between the max and min players
        #return the difference as the heuristic score
    
    #def miniMax(gamestate, depth, alpha, beta, max__min_player):
        #recurisve minimax function with alpha-beta pruning
        #gamestate: the current state of the game
        #depth: max search depth for minimax algo
        #alpha, beta: values for alpha-beta pruning
        #max__min_player: boolean telling wheterh we are max or min
        #return best score

    #def keyboard_input():
        #choose inputting format on keyboard for user input
    
    #def main():
        #for displaying main menu like how we did in wordle or similar projects
