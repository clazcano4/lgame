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
from somepackage import util

#Grid size
GRID_SIZE = 4

class Grid:
    def __init__(self , width, height, initValue = False, bitRep = None):
        util.raiseNotDefined()

class Agent:
    def __init__(self, index = 0):
        self.index = index
    
    def getAction(self, state):
        util.raiseNotDefined()

class Directions: 
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'

    LEFT = {NORTH: WEST, SOUTH:EAST, EAST: NORTH, WEST: SOUTH, STOP: STOP}

    RIGHT = {v: k for k, v in LEFT.items()}

    REVERSE = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST, STOP: STOP}

#L piece orientation
class GameState:
    def init(self, player_1, player_2, neutral_piece):
        #initalize tje game state with  the startiong postions for the L pieces and neutral 
        #player 1 and player 2 represent the corner position and orientation of each L-PIece
        #neutral piece is the 2 1x1 ciricle piece
    
    def is_valid():
        #check if a given (x,y) position is within the grid boundries
        #return true if within bound, if not return false
    
    def get_Piece_Position():
        #caclucate the (x,y) positions based on corner and oritentation
        #return a list of all (x,y) postions that the L piece occupies
    
    def is_position_free():
        #check if positon is free within the bound, and not occupied by other player
        #no overlapping with neurtal piece

    def apply_move():
        #update the L piece postion

    def getDirection(self):
        # returns agent's current direction 
        return self.direction

    def get_legal_move():
        #get all possible legal moves for the given player's L-Piece
        #get current L-Piece position and oreientation

    def eval():
        #get legal moves for both players
        #calculate the difference in the number of moves between the max and min players
        #return the difference as the heuristic score
    
    def miniMax(gamestate, depth, alpha, beta, max__min_player):
        #recurisve minimax function with alpha-beta pruning
        #gamestate: the current state of the game
        #depth: max search depth for minimax algo
        #alpha, beta: values for alpha-beta pruning
        #max__min_player: boolean telling wheterh we are max or min
        #return best score

    def keyboard_input():
        #choose inputting format on keyboard for user input
    
    def main():
        #for displaying main menu like how we did in wordle or similar projects
