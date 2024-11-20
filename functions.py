from main import * 
from L_game import *
from keyboard import *
from util import *
import sys
import math
import random
import string
import time
import types
import Tkinter

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

    class KeyboardAgent(Agent):
        WEST = 'w'
        EAST = 'e'
        NORTH = 'n'
        SOUTH = 's'

        def __init__(self, index = 0):
            self.lastMove = Directions.STOP
            self.index = index
            self.keys = []

        def getAction(self, state):
            from keyboard import keys_waiting
            CoordsAndDirections.running = True


class pastMoves: # class stores stack with all moves made by Agent
    def __init__(self):
        self.stack = []

    def push(self, x, y, direction, *neutralCoords):    # pushes user's moves to stack
        if (neutralCoords):
            self.stack.append((x, y, direction, *neutralCoords))
        else:
            self.stack.append((x, y, direction))

    def pop(self): # Pops user's moves from stack
        if(len(self.stack) != 0):
            return self.stack.pop()
    
    def size(self):
        return len(self.stack)
    
    def goBack(self, amountOfMoves): # allows user to go back to old Moves
        while (amountOfMoves != 0 and self.stack.size() != 0):
            self.stack.pop()
            amountOfMoves = amountOfMoves - 1 
        oldMove = self.stack.pop() # pops old move from stack
        self.stack.push(oldMove) # old move now becomes new move than can be re-acessed in future from stack
        return oldMove  # returns old move's coordinates

        

