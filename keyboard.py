import pygame

def userInput(move_input):
    #Parses the move input and returns the parsed data.
    move = move_input.strip().split()

    if len(move) < 3 or len(move) > 7:
        raise ValueError("Invalid input format. Enter a valid move (e.g., '1 2 E' or '1 2 E 4 3 1 1').")

    try:
        x = int(move[0])
        y = int(move[1])
        orientation = move[2]

        if len(move) == 3:
            return x, y, orientation, None

        elif len(move) == 7:
            oldNeutralX = int(move[3])
            oldNeutralY = int(move[4])
            newNeutralX = int(move[5])
            newNeutralY = int(move[6])
            neutral_move = ((oldNeutralX, oldNeutralY), (newNeutralX, newNeutralY))
            return x, y, orientation, neutral_move

        else:
            raise ValueError("Invalid input format.")
    except ValueError:
        raise ValueError("Invalid input. Make sure to enter integers for coordinates and a valid direction.")


