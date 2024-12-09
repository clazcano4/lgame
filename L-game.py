import pygame

class GameState:
    def __init__(self, player_positions, dot_positions, current_player):
        # store current positions of players and the dots
        self.player_positions = player_positions
        self.dot_positions = dot_positions
        self.current_player = current_player

    def getNumAgents(self):
        return 2

    def getLegalMoves(self, agentIndex):
        if agentIndex == 0:  # legal moves for player 1
            return ['N', 'S', 'E', 'W']
        elif agentIndex == 1:  # legal moves for player 2
            return ['N', 'S', 'E', 'W']
        return []

    def generateSuccessor(self, agentIndex, move):
        x, y, orientation, neutral_move = move

        # generate positions for L-shaped pieces
        if x is not None:
            new_positions = generate_l_shape(x, y, orientation)
            new_player_positions = dict(self.player_positions)
            new_player_positions["player1" if agentIndex == 0 else "player2"] = new_positions
        else:
            new_player_positions = dict(self.player_positions)

        # if needed, this updates the neutral pieces
        if neutral_move:
            from_pos, to_pos = neutral_move
            new_dot_positions = list(self.dot_positions)
            new_dot_positions.remove(from_pos)
            new_dot_positions.append(to_pos)
        else:
            new_dot_positions = list(self.dot_positions)

        return GameState(new_player_positions, new_dot_positions, "player2" if self.current_player == "player1" else "player1")

    def isWin(self):
        if self.current_player == "player1" and (2, 2) in self.player_positions["player1"]:
            return True
        return False

    def isLose(self):
        legal_moves = self.getLegalMoves(0) if self.current_player == "player1" else self.getLegalMoves(1)
        return len(legal_moves) == 0

    def getCurrentPlayer(self):
        return self.current_player

class MiniMax:
    def __init__(self, depth):
        self.depth = depth

    def getMove(self, gameState):
        value, move = self.getValue(gameState, 0, 0)
        return move

    def getValue(self, gameState, d, agentIndex):
        if d == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), None

        numAgents = gameState.getNumAgents()
        legalMoves = gameState.getLegalMoves(agentIndex)

        bestScore = float('-inf') if agentIndex == 0 else float('inf')
        bestMove = None
        for move in legalMoves:
            successor = gameState.generateSuccessor(agentIndex, (None, None, move, None))  # placeholder for neutral piece
            value, _ = self.getValue(successor, d+1 if (agentIndex+1) % numAgents == 0 else d, (agentIndex+1) % numAgents)
            if (agentIndex == 0 and value > bestScore) or (agentIndex == 1 and value < bestScore):
                bestScore = value
                bestMove = move
        return bestScore, bestMove


class AlphaBetaAgent:
    def __init__(self, depth):
        self.depth = depth

    def evaluationFunction(self, gameState):
        player1_positions = gameState.player_positions["player1"]
        player2_positions = gameState.player_positions["player2"]
        return len(player1_positions) - len(player2_positions)

    def getMove(self, gameState):
        numAgent = gameState.getNumAgents()
        moveScore = []

        def stopRM(list):
            return [x for x in list if x != 'Stop']

        def alphaBeta(successor, counter, alpha, beta):
            if counter >= self.depth * numAgent or successor.isWin() or successor.isLose():
                return self.evaluationFunction(successor)

            if counter % numAgent != 0:  # Min (Player 2's turn)
                result = float('inf')
                for move in stopRM(successor.getLegalMoves(counter % numAgent)):
                    dot = successor.generateSuccessor(counter % numAgent, (None, None, move, None))  # placeholder for neutral move
                    result = min(result, alphaBeta(dot, counter + 1, alpha, beta))
                    beta = min(beta, result)
                    if beta < alpha:
                        break
                return result
            else:  # Max (Player 1's turn)
                result = float('-inf')
                for move in stopRM(successor.getLegalMoves(counter % numAgent)):
                    dot = successor.generateSuccessor(counter % numAgent, (None, None, move, None))  # placeholder for neutral move
                    result = max(result, alphaBeta(dot, counter + 1, alpha, beta))
                    alpha = max(alpha, result)
                    if counter == 0:
                        moveScore.append(result)
                    if beta < alpha:
                        break
                return result

        result = alphaBeta(gameState, 0, float('-inf'), float('inf'))
        # finds move with the maximum score
        best_move = stopRM(gameState.getLegalMoves(0))[moveScore.index(max(moveScore))]
        return best_move

# Initialize Pygame
pygame.init()

# Screen and grid settings
screen_width, screen_height = 400, 500  # Extra space for the input box
grid_size, cell_size = 4, 100
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("L-Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (128, 128, 128)
green = (0, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Initial positions
player_positions = {
    "player1": [(2, 1), (3, 1), (3, 2), (3, 3)],  # Player 1's L-shape
    "player2": [(2, 2), (2, 4), (2, 3), (3, 4)]   # Player 2's L-shape
}
dot_positions = [(1, 1), (4, 4)]  # Neutral pieces

# Input state
input_text = ""

class pastMoves: # class stores stack with all moves made by Agent
    def __init__(self):
        self.stack = []

    def push(self, state):    # pushes user's moves to stack
        self.stack.append(state)

    def pop(self): # Pops user's moves from stack
        if(len(self.stack) != 0):
            return self.stack.pop()
    
    def size(self):
        return len(self.stack)
    
    def goBack(self, amountOfMoves): # allows user to go back to old Moves
        if amountOfMoves <= 0:
            print("Invalid number of moves to go back!")
            return
        if self.size() == 0:
            print("No more moves to undo!")
            return None 
        
        last_valid_state = None 

        for _ in range(amountOfMoves):
            if self.size() > 0:
                last_valid_state = self.pop()
            else:
                print("No more moves to undo!")
                break

        if last_valid_state:
            return last_valid_state
        else:
            print("No more moves available to go back to!")
            return None

# Stack to track moves for undo
past_moves = pastMoves()

# Current player
current_player = "player1"


def generate_l_shape(x, y, orientation):
    positions = []
    if orientation == 'N':  # Vertical arm up
        if x >= 3:  # Flip the piece if it's near the bottom edge
            print("Flipping L-piece facing North near the bottom edge at ({}, {})".format(x, y))
            positions = [(x, y), (x, y - 1), (x - 1, y), (x - 2, y)]  # Flip upward
        else:  # Standard L facing up
            print("Standard L-piece facing North at ({}, {})".format(x, y))
            positions = [(x, y), (x, y - 1), (x + 1, y), (x + 2, y)]

    elif orientation == 'S':  # Vertical arm down
        if x <= 2:  # Flip the piece if it's near the top edge
            print("Flipping L-piece facing South near the top edge at ({}, {})".format(x, y))
            positions = [(x, y), (x, y + 1), (x + 1, y), (x + 2, y)]  # Flip downward
        else:  # Standard L facing down
            print("Standard L-piece facing South at ({}, {})".format(x, y))
            positions = [(x, y), (x, y + 1), (x - 1, y), (x - 2, y)]

    elif orientation == 'E':  # Horizontal arm right
        if y <= 2:  # Flip the piece if it's near the left edge
            print("Flipping L-piece facing East near the left edge at ({}, {})".format(x, y))
            positions = [(x, y), (x + 1, y), (x, y + 1), (x, y + 2)]  # Flip rightward
        else:  # Standard L facing right
            print("Standard L-piece facing East at ({}, {})".format(x, y))
            positions = [(x, y), (x + 1, y), (x, y - 1), (x, y - 2)]

    elif orientation == 'W':  # Horizontal arm left
        if y >= 3:  # Flip the piece if it's near the right edge
            print("Flipping L-piece facing West near the right edge at ({}, {})".format(x, y))
            positions = [(x, y), (x - 1, y), (x, y - 1), (x, y - 2)]  # Flip leftward
        else:  # Standard L facing left
            print("Standard L-piece facing West at ({}, {})".format(x, y))
            positions = [(x, y), (x, y + 1), (x, y + 2), (x - 1, y)]

    else:
        raise ValueError("Invalid orientation: {} at position ({}, {})".format(orientation, x, y))

    # Debug: Print the generated positions
    print("Generated positions for orientation {} at ({}, {}): {}".format(orientation, x, y, positions))
    return positions

def is_space_empty(new_positions, other_positions, neutral_positions):
    #Check if the new positions are empty
    for pos in new_positions:
        if pos in other_positions or pos in neutral_positions:
            print("Space at {} is not empty.".format(pos))  # Debug message
            return False
        if not (1 <= pos[0] <= 4 and 1 <= pos[1] <= 4):  # Ensure within grid
            print("Position {} is out of bounds.".format(pos))  # Debug message
            return False
    return True

def update_game_state(player, move):
    #Updates the game state based on the player's move
    global past_moves, current_player
    x, y, orientation, neutral_move = move

    # Handle neutral piece-only movement
    if x is None and neutral_move:
        from_pos, to_pos = neutral_move
        if from_pos not in dot_positions:
            print("Invalid move: No neutral piece at {}.".format(from_pos))
            return False
        if to_pos in player_positions["player1"] + player_positions["player2"] or to_pos in dot_positions:
            print("Invalid move: Target position {} is occupied.".format(to_pos))
            return False
        if not (1 <= to_pos[0] <= 4 and 1 <= to_pos[1] <= 4):
            print("Invalid move: Target position {} is out of bounds.".format(to_pos))
            return False

        # Save current state for undo
        past_moves.push({
            "player_positions": dict(player_positions),
            "dot_positions": list(dot_positions),
            "current_player": current_player
        })

        # Update the neutral piece position
        dot_positions.remove(from_pos)
        dot_positions.append(to_pos)
        return True

    # Handle L-piece movement
    if x is not None:
        other_player = "player2" if player == "player1" else "player1"
        new_positions = generate_l_shape(x, y, orientation)

        # Validate the L-piece movement
        if not is_space_empty(new_positions, player_positions[other_player], dot_positions):
            print("Invalid move: spaces are not empty.")
            return False

        # Save current state for undo
        past_moves.push({
            "player_positions": dict(player_positions),
            "dot_positions": list(dot_positions),
            "current_player": current_player
        })

        # Update L-piece positions
        player_positions[player] = new_positions

        # Update neutral pieces if moved
        if neutral_move:
            from_pos, to_pos = neutral_move
            if from_pos not in dot_positions or to_pos in player_positions[player] + player_positions[other_player]:
                print("Invalid neutral piece move! Try again.")
                return False
            dot_positions.remove(from_pos)
            dot_positions.append(to_pos)

        return True

    return False

def undo_last_move(amount = 1):
    #Undo the last amount of moves
    global player_positions, dot_positions, current_player, past_moves

    if amount <= 0:
        print("Invalid undo amount!")
        return
    
    if past_moves.size() == 0:
        print("No moves to undo!")
        return 

    saved_state = past_moves.goBack(amount)

    if saved_state:
        player_positions = saved_state["player_positions"]
        dot_positions = saved_state["dot_positions"]
        current_player = saved_state["current_player"]
        print("Undo successful. Restored state from %d move(s)." % amount)

def draw_grid():
    #Draw the grid.
    for row in range(grid_size):
        for col in range(grid_size):
            x, y = col * cell_size, row * cell_size
            pygame.draw.rect(screen, gray, (x, y, cell_size, cell_size), 2)

def draw_player_pieces(positions, color):
    #Draw player pieces based on their positions
    for pos in positions:
        row, col = pos
        x = (row - 1) * cell_size
        y = (col - 1) * cell_size
        pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))

def draw_dot(position, color):
    #Draw a dot at the specified grid position
    row, col = position
    x = (row - 1) * cell_size + cell_size // 2
    y = (col - 1) * cell_size + cell_size // 2
    pygame.draw.circle(screen, color, (x, y), cell_size // 4)

def update_display():
    #Clear the screen and update all elements
    screen.fill(black)  # Clear screen
    draw_grid()  # Draw the grid
    draw_player_pieces(player_positions["player1"], red)
    draw_player_pieces(player_positions["player2"], blue)
    for dot_pos in dot_positions:
        draw_dot(dot_pos, white)

    # Draw the input box
    pygame.draw.rect(screen, gray, (10, 420, 380, 60))  # Input box
    input_surface = font.render(input_text, True, green)
    screen.blit(input_surface, (15, 430))  # Render the input text

    pygame.display.flip()

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

def handle_input(event):
    #Handle input events for typing
    global input_text
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:  # Enter key
            return True
        elif event.key == pygame.K_BACKSPACE:  # Backspace key
            input_text = input_text[:-1]
        else:
            # Capitalize letters before appending
            input_text += event.unicode.upper() if event.unicode.isalpha() else event.unicode
    return False

def initialize_game_state():
    global player_positions, dot_positions

    # Default initial state
    default_state = "3 1 W 1 1 4 4 2 4 E"

    # Prompt the user for the initial state
    user_input = raw_input("Enter initial game state (or press Enter for default): ").strip()  
    if not user_input:
        user_input = default_state

    try:
        # Parse the input
        tokens = user_input.split()
        if len(tokens) != 10:
            raise ValueError("Invalid input format. Must provide exactly 10 values.")

        # Parse Player 1's L-piece
        p1_row, p1_col = int(tokens[0]), int(tokens[1])
        p1_orientation = tokens[2].upper()
        player1_positions = generate_l_shape(p1_row, p1_col, p1_orientation)

        # Parse neutral pieces
        neutral_1 = (int(tokens[3]), int(tokens[4]))
        neutral_2 = (int(tokens[5]), int(tokens[6]))

        # Parse Player 2's L-piece
        p2_row, p2_col = int(tokens[7]), int(tokens[8])
        p2_orientation = tokens[9].upper()
        player2_positions = generate_l_shape(p2_row, p2_col, p2_orientation)

        # Validate positions
        all_positions = set(player1_positions + player2_positions + [neutral_1, neutral_2])
        if len(all_positions) != 10:  # Ensure no overlapping pieces
            raise ValueError("Pieces overlap or are invalid.")

        # Update the game state
        player_positions["player1"] = player1_positions
        player_positions["player2"] = player2_positions
        dot_positions[:] = [neutral_1, neutral_2]  # Update list in place

    except ValueError as e:
        print("Error initializing game state: {}".format(e))
        print("Using default initial state.")
        initialize_game_state()  # Retry with default state

initialize_game_state()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if handle_input(event):  # Process input
            command_parts = input_text.strip().lower().split()
            if command_parts[0] == "undo":
                if len(command_parts) == 2 and command_parts[1].isdigit():
                    amount = int(command_parts[1])
                    undo_last_move(amount)
                else:
                    undo_last_move(1)
                input_text = ""
                continue

            try:
                move = userInput(input_text)  # Parse the input
                if update_game_state(current_player, move):  # Update game state
                    current_player = "player2" if current_player == "player1" else "player1"
                input_text = ""  # Clear the input box after successful move
            except ValueError as e:
                print("Error: %s" % e)
                input_text = ""  # Clear the input box on error

    update_display()

pygame.quit()
