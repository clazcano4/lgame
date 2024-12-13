import pygame
import random

class GameState:
    def __init__(self, player_positions, dot_positions, current_player):
        self.player_positions = player_positions
        self.dot_positions = dot_positions
        self.current_player = current_player

    def getNumAgents(self):
        return 2

    def getLegalMoves(self, agentIndex):
        legal_moves = []
        player = "player1" if agentIndex == 0 else "player2"
        other_player = "player2" if player == "player1" else "player1"
        
        # Try all possible positions and orientations
        for x in range(1, 5):
            for y in range(1, 5):
                for orientation in ['N', 'S', 'E', 'W']:
                    try:
                        new_positions = generate_l_shape(x, y, orientation)
                        # Verify the move is valid
                        valid = True
                        for pos in new_positions:
                            if (pos in self.player_positions[other_player] or 
                                pos in self.dot_positions or 
                                not (1 <= pos[0] <= 4 and 1 <= pos[1] <= 4)):
                                valid = False
                                break
                        if valid:
                            legal_moves.append((x, y, orientation))
                    except ValueError:
                        continue
        return legal_moves

    def generateSuccessor(self, agentIndex, move):
        x, y, orientation = move
        player = "player1" if agentIndex == 0 else "player2"
        
        new_positions = generate_l_shape(x, y, orientation)
        new_player_positions = dict(self.player_positions)
        new_player_positions[player] = new_positions
        
        return GameState(new_player_positions, self.dot_positions, 
                        "player2" if self.current_player == "player1" else "player1")

    def isWin(self):
        return False  # Simplified win condition

    def isLose(self):
        return len(self.getLegalMoves(0 if self.current_player == "player1" else 1)) == 0

class MinimaxAgent:
    def __init__(self, depth='inf'):
        self.depth = float('inf') if depth == 'inf' else int(depth)
        self.nodes_expanded = 0
        self.cache = {}

    def getAction(self, gameState):
        """
        Returns the minimax action using alpha-beta pruning
        """
        self.nodes_expanded = 0
        
        def alphabeta(state, depth, alpha, beta, maximizingPlayer, moves_made=0):
            state_key = (
                str(state.player_positions),
                str(state.dot_positions),
                depth,
                maximizingPlayer
            )
            
            if state_key in self.cache:
                return self.cache[state_key]
            
            self.nodes_expanded += 1
            
            if depth == 0 or state.isWin() or state.isLose() or moves_made >= 50:
                score = self.evaluationFunction(state)
                self.cache[state_key] = (score, None)
                return score, None
            
            valid_moves = self.getLegalMovesWithNeutral(state)
            if not valid_moves:
                score = self.evaluationFunction(state)
                self.cache[state_key] = (score, None)
                return score, None
            
            best_move = None
            if maximizingPlayer:
                value = float('-inf')
                for l_move, neutral_move in valid_moves:
                    combined_move = (l_move[0], l_move[1], l_move[2], neutral_move)
                    successor = self.getSuccessor(state, combined_move)
                    new_score, _ = alphabeta(successor, depth - 1, alpha, beta, False, moves_made + 1)
                    if new_score > value:
                        value = new_score
                        best_move = combined_move
                    alpha = max(alpha, value)
                    if beta <= alpha:
                        break
            else:
                value = float('inf')
                for l_move, neutral_move in valid_moves:
                    combined_move = (l_move[0], l_move[1], l_move[2], neutral_move)
                    successor = self.getSuccessor(state, combined_move)
                    new_score, _ = alphabeta(successor, depth - 1, alpha, beta, True, moves_made + 1)
                    if new_score < value:
                        value = new_score
                        best_move = combined_move
                    beta = min(beta, value)
                    if beta <= alpha:
                        break
                    
            self.cache[state_key] = (value, best_move)
            return value, best_move

        _, action = alphabeta(gameState, self.depth, float('-inf'), float('inf'), True)
        print(f"Nodes expanded: {self.nodes_expanded}")
        return action

    def coversNewSquare(self, old_positions, new_positions):
        """
        Check if the new L-piece position covers at least one square
        that wasn't covered by the old position
        """
        old_set = set(old_positions)
        new_set = set(new_positions)
        return bool(new_set - old_set)  # Returns True if there are any new squares

    def getLegalMovesWithNeutral(self, state):
        """
        Gets all legal moves with mandatory neutral piece movement and new square coverage
        """
        basic_moves = state.getLegalMoves(1)
        combined_moves = []
        current_l_positions = state.player_positions["player2"]
        
        for move in basic_moves:
            # Generate new L-piece positions
            new_l_positions = generate_l_shape(move[0], move[1], move[2])
            
            # Check if the L-piece covers at least one new square
            if not self.coversNewSquare(current_l_positions, new_l_positions):
                continue
                
            # For valid L-piece moves, try all possible neutral piece movements
            for dot_idx, dot_pos in enumerate(state.dot_positions):
                for x in range(1, 5):
                    for y in range(1, 5):
                        new_pos = (x, y)
                        # Check if neutral move is valid with this L-piece move
                        if self.isValidNeutralMove(state, dot_pos, new_pos, new_l_positions):
                            combined_moves.append((move, (dot_pos, new_pos)))
        
        return combined_moves

    def isValidNeutralMove(self, state, old_pos, new_pos, new_l_positions):
        """
        Checks if a neutral piece movement is valid with the given L-piece positions
        """
        # Must be within bounds
        if not (1 <= new_pos[0] <= 4 and 1 <= new_pos[1] <= 4):
            return False
            
        # Can't overlap with other pieces
        if (new_pos in new_l_positions or 
            new_pos in state.player_positions["player1"] or 
            new_pos in state.dot_positions or 
            new_pos == old_pos):
            return False
            
        return True

    def getSuccessor(self, state, move):
        """
        Gets the successor state after applying a combined move
        """
        x, y, orientation, neutral_move = move
        if neutral_move is None:
            return state  # Invalid move - must include neutral piece movement
            
        # Create new state
        new_player_positions = dict(state.player_positions)
        new_player_positions["player2"] = generate_l_shape(x, y, orientation)
        new_dot_positions = list(state.dot_positions)
        
        # Apply neutral piece movement
        old_pos, new_pos = neutral_move
        new_dot_positions.remove(old_pos)
        new_dot_positions.append(new_pos)
            
        return GameState(new_player_positions, new_dot_positions, "player1")

    def evaluationFunction(self, state):
        """
        Heuristic evaluation function
        """
        if state.isWin():
            return float('inf')
        if state.isLose():
            return float('-inf')
            
        score = 0
        
        # Mobility score
        player2_moves = len(self.getLegalMovesWithNeutral(state))
        # Approximate player1's moves since we don't need exact neutral moves calculation
        player1_moves = len(state.getLegalMoves(0)) 
        mobility_score = player2_moves - player1_moves
        score += mobility_score * 10
        
        # Territory control for L-piece
        player2_positions = set(state.player_positions["player2"])
        for pos in player2_positions:
            x, y = pos
            if 2 <= x <= 3 and 2 <= y <= 3:  # Center positions
                score += 2
            else:  # Edge positions
                score += 1
        
        # Neutral piece positioning
        for dot_pos in state.dot_positions:
            x, y = dot_pos
            if 2 <= x <= 3 and 2 <= y <= 3:  # Center positions
                score += 1
            # Bonus for blocking opponent's potential moves
            adj_squares = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
            for adj_x, adj_y in adj_squares:
                if (1 <= adj_x <= 4 and 1 <= adj_y <= 4 and 
                    (adj_x, adj_y) in state.player_positions["player1"]):
                    score += 2
        
        return score
    
    
class LGame:
    def __init__(self):
        pygame.init()
        self.screen_width = 400
        self.screen_height = 500
        self.grid_size = 4
        self.cell_size = 100
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("L-Game")

        # Colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.gray = (128, 128, 128)
        self.green = (0, 255, 0)

        self.font = pygame.font.Font(None, 36)
        self.input_text = ""
        self.game_mode = None
        self.ai_agent = MinimaxAgent(depth=3)
        self.past_moves = pastMoves()
        self.initialize_game_state()

    def initialize_game_state(self):
        print("Initializing game state...")
        default_state = "3 1 W 1 1 4 4 2 4 E"
        
        try:
            user_input = input("Enter initial game state (or press Enter for default): ").strip()
            if not user_input:
                user_input = default_state

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
            if len(all_positions) != 10:
                raise ValueError("Pieces overlap or are invalid.")

            self.player_positions = {
                "player1": player1_positions,
                "player2": player2_positions
            }
            self.dot_positions = [neutral_1, neutral_2]
            self.current_player = "player1"
            self.past_moves = pastMoves()

        except (ValueError, IndexError) as e:
            print(f"Error initializing game state: {e}")
            print("Using default initial state...")
            self.initialize_game_state()

    def select_game_mode(self):
        while self.game_mode is None:
            self.screen.fill(self.black)
            title = self.font.render("Select Game Mode:", True, self.white)
            option1 = self.font.render("1. Human vs Human", True, self.white)
            option2 = self.font.render("2. Human vs AI", True, self.white)
            
            self.screen.blit(title, (100, 150))
            self.screen.blit(option1, (100, 200))
            self.screen.blit(option2, (100, 250))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.game_mode = "human"
                        return True
                    elif event.key == pygame.K_2:
                        self.game_mode = "ai"
                        return True
        return True

    def run(self):
        if not self.select_game_mode():
            return

        running = True
        while running:
            if self.game_mode == "ai" and self.current_player == "player2":
                # AI's turn
                game_state = GameState(self.player_positions, self.dot_positions, self.current_player)
                ai_move = self.ai_agent.getAction(game_state)  # Changed from getMove to getAction
                
                if ai_move:
                    print("AI attempting move:", ai_move)
                    success = self.update_game_state("player2", ai_move)  # No need to unpack the move
                    if success:
                        print("AI move successful")
                        self.current_player = "player1"
                    else:
                        print("AI move failed")
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.handle_input(event):
                    command_parts = self.input_text.strip().lower().split()
                    if command_parts[0] == "undo":
                        if len(command_parts) == 2 and command_parts[1].isdigit():
                            self.undo_last_move(int(command_parts[1]))
                        else:
                            self.undo_last_move(1)
                        self.input_text = ""
                        continue

                    try:
                        move = self.parse_input(self.input_text)
                        if self.update_game_state(self.current_player, move):
                            self.current_player = "player2" if self.current_player == "player1" else "player1"
                        self.input_text = ""
                    except ValueError as e:
                        print(f"Error: {e}")
                        self.input_text = ""

            self.update_display()

        pygame.quit()
    
    def undo_last_move(self, amount=1):
        if amount <= 0:
            print("Invalid undo amount!")
            return
        if self.past_moves.size() == 0:
            print("No moves to undo!")
            return

        saved_state = self.past_moves.goBack(amount)
        if saved_state:
            self.player_positions = saved_state["player_positions"]
            self.dot_positions = saved_state["dot_positions"]
            self.current_player = saved_state["current_player"]
            print("Undo successful. Restored state from %d move(s)." % amount)
        else:
            print("No more moves available to go back to!")

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                self.input_text += event.unicode.upper() if event.unicode.isalpha() else event.unicode
        return False

    def parse_input(self, move_input):
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
                oldNeutralX, oldNeutralY = int(move[3]), int(move[4])
                newNeutralX, newNeutralY = int(move[5]), int(move[6])
                return x, y, orientation, ((oldNeutralX, oldNeutralY), (newNeutralX, newNeutralY))
            else:
                raise ValueError("Invalid input format.")
        except ValueError:
            raise ValueError("Invalid input. Make sure to enter integers for coordinates and a valid direction.")

    def update_game_state(self, player, move):
        x, y, orientation, neutral_move = move
        other_player = "player2" if player == "player1" else "player1"
        
        try:
            # Generate new positions
            new_positions = generate_l_shape(x, y, orientation)
            
            # Convert current positions to sets for collision detection
            other_pieces = set(self.player_positions[other_player])
            dots = set(self.dot_positions)
            
            # Check if any new L-piece position is invalid
            for pos in new_positions:
                if not (1 <= pos[0] <= 4 and 1 <= pos[1] <= 4):
                    print("Position {} is out of bounds".format(pos))
                    return False
                if pos in other_pieces:
                    print("Position {} overlaps with other player".format(pos))
                    return False
                if pos in dots:
                    print("Position {} overlaps with dot".format(pos))
                    return False
            
            # If neutral move is specified, validate it before making any changes
            if neutral_move:
                from_pos, to_pos = neutral_move
                
                # Check if the source position is valid
                if from_pos not in self.dot_positions:
                    print("Invalid neutral piece source")
                    return False
                
                # Check if destination is in bounds
                if not (1 <= to_pos[0] <= 4 and 1 <= to_pos[1] <= 4):
                    print("Neutral piece destination is out of bounds")
                    return False
                
                # Check if destination overlaps with L pieces (both current and new positions)
                if to_pos in new_positions or to_pos in self.player_positions[other_player]:
                    print("Invalid neutral piece destination - overlaps with L piece")
                    return False
                    
                # Check if destination overlaps with other neutral piece
                other_dot = [pos for pos in self.dot_positions if pos != from_pos][0]
                if to_pos == other_dot:
                    print("Invalid neutral piece destination - overlaps with other neutral piece")
                    return False
            
            # At this point, both moves are valid, so save current state and apply changes
            self.past_moves.push({
                "player_positions": dict(self.player_positions),
                "dot_positions": list(self.dot_positions),
                "current_player": self.current_player
            })
            
            # Update the L-piece position
            self.player_positions[player] = new_positions
            
            # Update neutral piece position if specified
            if neutral_move:
                from_pos, to_pos = neutral_move
                self.dot_positions.remove(from_pos)
                self.dot_positions.append(to_pos)
                
            return True
            
        except ValueError as e:
            print("Invalid move: {}".format(e))
            return False
        
        
        
    def update_display(self):
        self.screen.fill(self.black)
        self.draw_grid()
        self.draw_player_pieces(self.player_positions["player1"], self.red)
        self.draw_player_pieces(self.player_positions["player2"], self.blue)
        for dot_pos in self.dot_positions:
            self.draw_dot(dot_pos, self.white)

        pygame.draw.rect(self.screen, self.gray, (10, 420, 380, 60))
        input_surface = self.font.render(self.input_text, True, self.green)
        self.screen.blit(input_surface, (15, 430))

        # Display current player and game mode
        player_text = f"Current Player: {'Human' if self.current_player == 'player1' else ('AI' if self.game_mode == 'ai' else 'Human 2')}"
        player_surface = self.font.render(player_text, True, self.white)
        self.screen.blit(player_surface, (10, 380))

        pygame.display.flip()

    def draw_grid(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x, y = col * self.cell_size, row * self.cell_size
                pygame.draw.rect(self.screen, self.gray, (x, y, self.cell_size, self.cell_size), 2)

    def draw_player_pieces(self, positions, color):
        for pos in positions:
            row, col = pos
            x = (row - 1) * self.cell_size
            y = (col - 1) * self.cell_size
            pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))

    def draw_dot(self, position, color):
        row, col = position
        x = (row - 1) * self.cell_size + self.cell_size // 2
        y = (col - 1) * self.cell_size + self.cell_size // 2
        pygame.draw.circle(self.screen, color, (x, y), self.cell_size // 4)

def generate_l_shape(x, y, orientation):
    positions = []
    if orientation == 'N':  # Vertical arm up
        if x >= 3:  # Flip the piece if it's near the bottom edge
            #("Flipping L-piece facing North near the bottom edge at ({}, {})".format(x, y))
            positions = [(x, y), (x, y - 1), (x - 1, y), (x - 2, y)]  # Flip upward
        else:  # Standard L facing up
            #print("Standard L-piece facing North at ({}, {})".format(x, y))
            positions = [(x, y), (x, y - 1), (x + 1, y), (x + 2, y)]

    elif orientation == 'S':  # Vertical arm down
        if x <= 2:  # Flip the piece if it's near the top edge
            #print("Flipping L-piece facing South near the top edge at ({}, {})".format(x, y))
            positions = [(x, y), (x, y + 1), (x + 1, y), (x + 2, y)]  # Flip downward
        else:  # Standard L facing down
            #("Standard L-piece facing South at ({}, {})".format(x, y))
            positions = [(x, y), (x, y + 1), (x - 1, y), (x - 2, y)]

    elif orientation == 'E':  # Horizontal arm right
        if y <= 2:  # Flip the piece if it's near the left edge
            #print("Flipping L-piece facing East near the left edge at ({}, {})".format(x, y))
            positions = [(x, y), (x + 1, y), (x, y + 1), (x, y + 2)]  # Flip rightward
        else:  # Standard L facing right
            #print("Standard L-piece facing East at ({}, {})".format(x, y))
            positions = [(x, y), (x + 1, y), (x, y - 1), (x, y - 2)]

    elif orientation == 'W':  # Horizontal arm left
        if y >= 3:  # Flip the piece if it's near the right edge
            #print("Flipping L-piece facing West near the right edge at ({}, {})".format(x, y))
            positions = [(x, y), (x - 1, y), (x, y - 1), (x, y - 2)]  # Flip leftward
        else:  # Standard L facing left
            #print("Standard L-piece facing West at ({}, {})".format(x, y))
            positions = [(x, y), (x, y + 1), (x, y + 2), (x - 1, y)]

    else:
        raise ValueError(f"Invalid orientation: {orientation}")
    # Debug: Print the generated positions
    #print("Generated positions for orientation {} at ({}, {}): {}".format(orientation, x, y, positions))
    return positions

def is_space_empty(new_positions, other_positions, neutral_positions):
    new_pos_set = set(new_positions)
    other_pos_set = set(other_positions)
    neutral_pos_set = set(neutral_positions)
    
    # Check bounds first
    if not all(1 <= pos[0] <= 4 and 1 <= pos[1] <= 4 for pos in new_pos_set):
        return False
    
    # Use set operations for faster checking
    return not (new_pos_set.intersection(other_pos_set) or 
               new_pos_set.intersection(neutral_pos_set))

class pastMoves:
    def __init__(self):
        self.stack = []

    def push(self, state):
        self.stack.append(state)

    def pop(self):
        if len(self.stack) != 0:
            return self.stack.pop()
    
    def size(self):
        return len(self.stack)
    
    def goBack(self, amountOfMoves):
        if amountOfMoves <= 0:
            print("Invalid number of moves to go back!")
            return None
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

def main():
    game = LGame()
    game.run()

if __name__ == "__main__":
    main()