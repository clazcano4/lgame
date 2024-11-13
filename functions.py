from main import * 
from L_game import *
from keyboard import *
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

        

