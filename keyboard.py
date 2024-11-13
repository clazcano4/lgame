from functions import *

class pastMoves: # class stores stack with all moves made by Agent
    def __init__(self):
        self.stack = []
    def push(self, x, y, direction, *neutralCoords):
        if (neutralCoords):
            self.stack.append((x, y, direction, *neutralCoords))
        else:
            self.stack.append((x, y, direction))


def userInput(): # Prompts user to input coordinates for their next move 
    running = True
    playerOneMoves = pastMoves()
    playerTwoMoves = pastMoves()

    currentPlayer = 1

    while (running):
        coordsAndDirection = input("Enter your move (e.g, '1 2 E 4 3 1 1'): ")
        move = coordsAndDirection.split()

        if (len(move) < 3 or len(move) > 7):
            print("Invalid input. Please enter a valid move")
            continue

        try:
            x = int(move[0])
            y = int(move[1])
            direction = str(move[2])

            if (len(move) == 3):
                if currentPlayer == 1:
                    playerOneMoves.push(x, y, direction)
                else:
                    playerTwoMoves.push(x, y, direction)

            elif (len(move) == 7):
                oldNeutralX = int(move[3])
                oldNeutralY = int(move[4])
                newNeutralX = int(move[5])
                newNeutralY = int(move[6])

                if currentPlayer == 1:
                    playerOneMoves.push(x, y, direction, oldNeutralX, oldNeutralY, newNeutralX, newNeutralY)
                else:
                    playerTwoMoves.push(x, y, direction, oldNeutralX, oldNeutralY, newNeutralX, newNeutralY)
            
            currentPlayer = 2 if currentPlayer == 1 else 1

        except ValueError: 
            print("Invalid input.")
            continue



            