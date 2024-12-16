import pygame
import random
import sys


class GameState:
    def __init__(self, player_positions, dot_positions, current_player):
        self.player_positions = player_positions
        self.dot_positions = dot_positions
        self.current_player = current_player

    def getNumAgents(self):
        return 2

    

    def generateSuccessor(self, agentIndex, move):
        x, y, orientation = move
        player = "player1" if agentIndex == 0 else "player2"
        
        new_positions = generate_l_shape(x, y, orientation)
        new_player_positions = dict(self.player_positions)
        new_player_positions[player] = new_positions
        
        return GameState(new_player_positions, self.dot_positions, 
                        "player2" if self.current_player == "player1" else "player1")

    def isWin(self):
        opponent = "player2" if self.current_player == "player1" else "player1"
        opponent_index = 1 if opponent == "player2" else 0
        l_piece_moves = self.getLegalMoves(opponent_index)
        return len(l_piece_moves) == 0

    def isLose(self):
        current_index = 0 if self.current_player == "player1" else 1
        l_piece_moves = self.getLegalMoves(current_index)
        return len(l_piece_moves) == 0

    def getLegalMoves(self, agentIndex):
        player = "player1" if agentIndex == 0 else "player2"
        other_player = "player2" if player == "player1" else "player1"
        
        legal_moves = []
        current_positions = set(self.player_positions[player])
        
        for x in range(1, 5):
            for y in range(1, 5):
                for orientation in ['N', 'S', 'E', 'W']:
                    try:
                        new_positions = generate_l_shape(x, y, orientation)
                        new_positions_set = set(new_positions)
                        
                        if new_positions_set == current_positions:
                            continue
                            
                        if not all(1 <= pos[0] <= 4 and 1 <= pos[1] <= 4 for pos in new_positions):
                            continue
                            
                        valid = True
                        occupied_positions = (set(self.player_positions[other_player]) | 
                                        set(self.dot_positions))
                        
                        for pos in new_positions:
                            if pos in occupied_positions:
                                valid = False
                                break
                                
                        if valid:
                            legal_moves.append((x, y, orientation))
                            
                    except ValueError:
                        continue
        
        return legal_moves
    
    
    
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
                    if successor:  # Only process if the move was valid
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
                    if successor:  # Only process if the move was valid
                        new_score, _ = alphabeta(successor, depth - 1, alpha, beta, True, moves_made + 1)
                        if new_score < value:
                            value = new_score
                            best_move = combined_move
                        beta = min(beta, value)
                        if beta <= alpha:
                            break
                        
            self.cache[state_key] = (value, best_move)
            return value, best_move

        valid_moves = self.getLegalMovesWithNeutral(gameState)
        if not valid_moves:
            return None
            
        _, action = alphabeta(gameState, self.depth, float('-inf'), float('inf'), True)
        print(f"Nodes expanded: {self.nodes_expanded}")
        
        if action:
            return action
            
        # Fallback to any valid move if alphabeta fails
        l_move, neutral_move = valid_moves[0]
        return (l_move[0], l_move[1], l_move[2], neutral_move)
    

    def getSuccessor(self, state, move):
        """
        Gets the successor state after applying a combined move
        """
        x, y, orientation, neutral_move = move
        if neutral_move is None:
            return None
            
        # Verify L piece move
        new_l_positions = generate_l_shape(x, y, orientation)
        other_player = "player2" if state.current_player == "player1" else "player1"
        
        # Check for collisions
        other_pieces = set(state.player_positions[other_player])
        dots = set(state.dot_positions)
        
        # Validate L piece positions
        for pos in new_l_positions:
            if not (1 <= pos[0] <= 4 and 1 <= pos[1] <= 4):
                return None
            if pos in other_pieces or pos in dots:
                return None
                
        # Validate neutral piece movement
        old_pos, new_pos = neutral_move
        if old_pos not in state.dot_positions:
            return None
            
        if not (1 <= new_pos[0] <= 4 and 1 <= new_pos[1] <= 4):
            return None
            
        if (new_pos in new_l_positions or 
            new_pos in state.player_positions[other_player] or 
            new_pos in state.dot_positions):
            return None
        
        # All validations passed, create new state
        new_player_positions = dict(state.player_positions)
        new_player_positions[state.current_player] = new_l_positions
        new_dot_positions = list(state.dot_positions)
        
        # Apply neutral piece movement
        new_dot_positions.remove(old_pos)
        new_dot_positions.append(new_pos)
            
        return GameState(new_player_positions, new_dot_positions, 
                        "player2" if state.current_player == "player1" else "player1")

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
        combined_moves = []
        current_player = state.current_player
        other_player = "player2" if current_player == "player1" else "player1"
        
        # Get all pieces' current positions as sets for efficient collision checking
        current_l_positions = set(state.player_positions[current_player])
        other_pieces = set(state.player_positions[other_player])
        dot_positions = set(state.dot_positions)
        
        # Try all possible L-piece positions
        for x in range(1, 5):
            for y in range(1, 5):
                for orientation in ['N', 'S', 'E', 'W']:
                    try:
                        # Generate new L-piece positions
                        new_l_positions = generate_l_shape(x, y, orientation)
                        new_positions_set = set(new_l_positions)
                        
                        # Skip if no new squares are covered
                        if not bool(new_positions_set - current_l_positions):
                            continue
                            
                        # Check if all positions are within bounds
                        if not all(1 <= pos[0] <= 4 and 1 <= pos[1] <= 4 for pos in new_l_positions):
                            continue
                            
                        # Check for collisions with other pieces
                        if (new_positions_set & other_pieces) or (new_positions_set & dot_positions):
                            continue
                        
                        # For valid L-piece positions, try all possible neutral piece movements
                        for dot_pos in state.dot_positions:
                            for new_x in range(1, 5):
                                for new_y in range(1, 5):
                                    new_dot_pos = (new_x, new_y)
                                    
                                    # Skip if neutral piece doesn't actually move
                                    if new_dot_pos == dot_pos:
                                        continue
                                    
                                    # Skip if new position is out of bounds
                                    if not (1 <= new_x <= 4 and 1 <= new_y <= 4):
                                        continue
                                    
                                    # Skip if new position overlaps with any piece
                                    if (new_dot_pos in new_positions_set or
                                        new_dot_pos in other_pieces or
                                        new_dot_pos in (set(state.dot_positions) - {dot_pos})):
                                        continue
                                    
                                    # Move is valid - add it to the list
                                    l_move = (x, y, orientation)
                                    neutral_move = (dot_pos, new_dot_pos)
                                    combined_moves.append((l_move, neutral_move))
                                    
                    except ValueError:
                        continue
        
        # Shuffle moves for variety
        random.shuffle(combined_moves)
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
        self.screen_width = 800
        self.screen_height = 900
        self.grid_size = 4
        self.cell_size = 150
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("L-Game")

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.gray = (128, 128, 128)
        self.green = (0, 255, 0)
        self.yellow = (255, 255, 0)

        self.font = pygame.font.Font(None, 48)
        self.reset_game()

    def initialize_game_state(self):
        default_state = "3 1 W 1 1 4 4 2 4 E"
        input_text = ""
        
        while True:
            self.screen.fill(self.black)
            
            # Display instructions
            title = self.font.render("Enter Initial Game State", True, self.white)
            title_rect = title.get_rect(center=(self.screen_width // 2, 100))
            self.screen.blit(title, title_rect)
            
            # Display format instructions
            format_text = "Format: P1(x y D) n1x n1y n2x n2y P2(x y D)"
            format_surface = self.font.render(format_text, True, self.gray)
            format_rect = format_surface.get_rect(center=(self.screen_width // 2, 150))
            self.screen.blit(format_surface, format_rect)
            
            # Display example
            example = "Example: 3 1 W 1 1 4 4 2 4 E"
            example_surface = self.font.render(example, True, self.gray)
            example_rect = example_surface.get_rect(center=(self.screen_width // 2, 180))
            self.screen.blit(example_surface, example_rect)
            
            # Display enter instruction
            enter_text = "Press ENTER for default state"
            enter_surface = self.font.render(enter_text, True, self.green)
            enter_rect = enter_surface.get_rect(center=(self.screen_width // 2, 220))
            self.screen.blit(enter_surface, enter_rect)

            # Display current input
            input_prompt = self.font.render("Your input:", True, self.white)
            input_prompt_rect = input_prompt.get_rect(center=(self.screen_width // 2, 320))
            self.screen.blit(input_prompt, input_prompt_rect)

            input_surface = self.font.render(input_text, True, self.green)
            input_rect = input_surface.get_rect(center=(self.screen_width // 2, 350))
            self.screen.blit(input_surface, input_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        try:
                            # Use default state if input is empty
                            state_to_use = input_text.strip() if input_text.strip() else default_state
                            tokens = state_to_use.split()
                            
                            if len(tokens) != 10:
                                raise ValueError("Invalid input format. Must provide exactly 10 values.")

                            p1_row, p1_col = int(tokens[0]), int(tokens[1])
                            p1_orientation = tokens[2].upper()
                            player1_positions = generate_l_shape(p1_row, p1_col, p1_orientation)

                            neutral_1 = (int(tokens[3]), int(tokens[4]))
                            neutral_2 = (int(tokens[5]), int(tokens[6]))

                            p2_row, p2_col = int(tokens[7]), int(tokens[8])
                            p2_orientation = tokens[9].upper()
                            player2_positions = generate_l_shape(p2_row, p2_col, p2_orientation)

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
                            return
                            
                        except (ValueError, IndexError) as e:
                            # Display error message
                            error_text = f"Error: {str(e)}"
                            error_surface = self.font.render(error_text, True, self.red)
                            error_rect = error_surface.get_rect(center=(self.screen_width // 2, 400))
                            self.screen.blit(error_surface, error_rect)
                            pygame.display.flip()
                            pygame.time.wait(2000)  # Show error for 2 seconds
                            input_text = ""  # Clear input after error
                            continue
                            
                    elif event.unicode.isprintable():
                        input_text += event.unicode
            
            
    def reset_game(self):
        """Reset all game variables to their initial state"""
        self.input_text = ""
        self.game_mode = None
        self.ai_agent = MinimaxAgent(depth=3)
        self.past_moves = pastMoves()
        self.game_over = False
        self.winner_message = ""
        self.initialize_game_state()
        
    def display_play_again(self):
        """Display play again options and handle input through Pygame"""
        input_text = ""
        while True:
            # Clear screen and display messages
            self.screen.fill(self.black)
            
            # Display winner message
            winner_surface = self.font.render(self.winner_message, True, self.yellow)
            winner_rect = winner_surface.get_rect(center=(self.screen_width // 2, 180))
            self.screen.blit(winner_surface, winner_rect)
            
            # Display play again prompt
            play_again = self.font.render("Play Again? (Y/N)", True, self.white)
            play_rect = play_again.get_rect(center=(self.screen_width // 2, 250))
            self.screen.blit(play_again, play_rect)
            
            # Display current input
            input_surface = self.font.render(input_text, True, self.green)
            input_rect = input_surface.get_rect(center=(self.screen_width // 2, 300))
            self.screen.blit(input_surface, input_rect)
            
            pygame.display.flip()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                    
                if event.type == pygame.KEYDOWN:
                    # Handle backspace
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                        
                    # Handle return/enter
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if input_text.upper() == 'Y':
                            self.reset_game()
                            return True
                        elif input_text.upper() == 'N':
                            return False
                            
                    # Handle character input
                    elif event.unicode.upper() in ['Y', 'N']:
                        input_text = event.unicode.upper()

       
    
        

    def select_game_mode(self):
        while self.game_mode is None:
            self.screen.fill(self.black)
            
            # Create text surfaces
            title = self.font.render("Select Game Mode:", True, self.white)
            option1 = self.font.render("1. Human vs Human", True, self.white)
            option2 = self.font.render("2. Human vs AI", True, self.white)
            option3 = self.font.render("3. AI vs AI", True, self.white)
            
            # Get rectangles for centering
            title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height // 3))
            option1_rect = option1.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            option2_rect = option2.get_rect(center=(self.screen_width // 2, (self.screen_height // 2) + 80))
            option3_rect = option3.get_rect(center=(self.screen_width // 2, (self.screen_height // 2) + 160))
            
            # Draw centered text
            self.screen.blit(title, title_rect)
            self.screen.blit(option1, option1_rect)
            self.screen.blit(option2, option2_rect)
            self.screen.blit(option3, option3_rect)
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.game_mode = "human"
                        if not self.select_first_player("HUMAN VS HUMAN"):
                            return False
                        return True
                    elif event.key == pygame.K_2:
                        self.game_mode = "ai"
                        if not self.select_first_player("HUMAN VS AI"):
                            return False
                        return True
                    elif event.key == pygame.K_3:
                        self.game_mode = "ai_vs_ai"
                        # Create two different AI agents with different depths for variety
                        self.ai_agent1 = MinimaxAgent(depth=3)  # AI player 1
                        self.ai_agent2 = MinimaxAgent(depth=2)  # AI player 2
                        return True
        return True
    
    
    def select_first_player(self, mode_title):
        """Handle first player selection for human modes"""
        while True:
            self.screen.fill(self.black)
            
            # Display mode title
            title = self.font.render(mode_title, True, self.white)
            title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height // 3))
            self.screen.blit(title, title_rect)
            
            # Display selection prompt
            prompt = self.font.render("Who goes first?", True, self.white)
            prompt_rect = prompt.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(prompt, prompt_rect)
            
            # Display options
            if self.game_mode == "human":
                option1 = self.font.render("1. Player 1", True, self.white)
                option2 = self.font.render("2. Player 2", True, self.white)
            else:  # human vs AI
                option1 = self.font.render("1. Human", True, self.white)
                option2 = self.font.render("2. AI", True, self.white)
                
            option1_rect = option1.get_rect(center=(self.screen_width // 2, (self.screen_height // 2) + 80))
            option2_rect = option2.get_rect(center=(self.screen_width // 2, (self.screen_height // 2) + 160))
            
            self.screen.blit(option1, option1_rect)
            self.screen.blit(option2, option2_rect)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.current_player = "player1"
                        return True
                    elif event.key == pygame.K_2:
                        self.current_player = "player2"
                        if self.game_mode == "ai":
                            self.ai_agent = MinimaxAgent(depth=3)  # Create AI agent here if AI goes first
                        return True



    def run(self):
        running = True
        while running:
            # Select game mode if not selected
            if not self.select_game_mode():
                running = False
                continue

            # Main game loop
            game_running = True
            while game_running and running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        game_running = False
                    
                    if not self.game_over and self.game_mode != "ai_vs_ai" and self.handle_input(event):
                        command_parts = self.input_text.strip().lower().split()
                        
                        # Handle undo command
                        if command_parts[0] == "undo":
                            if len(command_parts) == 2 and command_parts[1].isdigit():
                                self.undo_last_move(int(command_parts[1]))
                            else:
                                self.undo_last_move(1)
                            self.input_text = ""
                            continue

                        # Handle regular moves
                        try:
                            move = self.parse_input(self.input_text)
                            if self.update_game_state(self.current_player, move):
                                new_state = GameState(self.player_positions, self.dot_positions, self.current_player)
                                opponent_index = 1 if self.current_player == "player1" else 0
                                legal_moves = new_state.getLegalMoves(opponent_index)
                                
                                if len(legal_moves) <= 1:
                                    winner = "Player 1" if self.current_player == "player1" else "Player 2"
                                    if self.game_mode == "ai" and winner == "Player 2":
                                        self.winner_message = f"AI WINS!"
                                    else:
                                        self.winner_message = f"{winner} WINS!"
                                    self.game_over = True
                                
                                if not self.game_over:
                                    self.current_player = "player2" if self.current_player == "player1" else "player1"
                                    
                            self.input_text = ""
                        except ValueError as e:
                            self.input_text = ""

                # Handle AI moves
                if not self.game_over:
                    if self.game_mode == "ai_vs_ai":
                        # Add delay between AI moves for visibility
                        pygame.time.wait(1000)  
                        
                        game_state = GameState(self.player_positions, self.dot_positions, self.current_player)
                        
                        # Determine which AI agent to use
                        current_agent = self.ai_agent1 if self.current_player == "player1" else self.ai_agent2
                        ai_move = current_agent.getAction(game_state)
                        
                        if ai_move:
                            print(f"AI {self.current_player} attempting move:", ai_move)
                            success = self.update_game_state(self.current_player, ai_move)
                            if success:
                                print(f"AI {self.current_player} move successful")
                                new_state = GameState(self.player_positions, self.dot_positions, self.current_player)
                                opponent_index = 1 if self.current_player == "player1" else 0
                                legal_moves = new_state.getLegalMoves(opponent_index)
                                
                                if len(legal_moves) <= 1:
                                    winner = "AI 1" if self.current_player == "player1" else "AI 2"
                                    self.winner_message = f"{winner} WINS!"
                                    print(f"\n!!! GAME OVER - {self.winner_message}")
                                    self.game_over = True
                                else:
                                    self.current_player = "player2" if self.current_player == "player1" else "player1"
                            else:
                                print(f"AI {self.current_player} move failed")
                                
                    elif self.game_mode == "ai" and self.current_player == "player2":
                        game_state = GameState(self.player_positions, self.dot_positions, self.current_player)
                        ai_move = self.ai_agent.getAction(game_state)
                        
                        if ai_move:
                            print("AI attempting move:", ai_move)
                            success = self.update_game_state("player2", ai_move)
                            if success:
                                print("AI move successful")
                                new_state = GameState(self.player_positions, self.dot_positions, "player2")
                                legal_moves = new_state.getLegalMoves(0)  # Check player1's moves
                                if len(legal_moves) <= 1:
                                    self.winner_message = "AI WINS!"
                                    print(f"\n!!! GAME OVER - {self.winner_message}")
                                    self.game_over = True
                                else:
                                    self.current_player = "player1"
                            else:
                                print("AI move failed")

                # Update the display
                self.update_display()

                # If game is over, show play again option
                if self.game_over:
                    if self.display_play_again():
                        game_running = False  # Exit current game loop to start new game
                    else:
                        running = False  # Exit main loop to quit game
                        game_running = False

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
                return bool(self.input_text.strip())
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
        
        if self.game_over:
            return False
        
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
        
        # Calculate grid position to center it
        grid_width = self.grid_size * self.cell_size
        grid_height = self.grid_size * self.cell_size
        grid_x = (self.screen_width - grid_width) // 2
        grid_y = 50  # Offset from top
        
        # Draw grid with offset
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x = grid_x + col * self.cell_size
                y = grid_y + row * self.cell_size
                pygame.draw.rect(self.screen, self.gray, 
                            (x, y, self.cell_size, self.cell_size), 2)

        # Draw player pieces with offset
        for pos in self.player_positions["player1"]:
            row, col = pos
            x = grid_x + (row - 1) * self.cell_size
            y = grid_y + (col - 1) * self.cell_size
            pygame.draw.rect(self.screen, self.red, 
                            (x, y, self.cell_size, self.cell_size))

        for pos in self.player_positions["player2"]:
            row, col = pos
            x = grid_x + (row - 1) * self.cell_size
            y = grid_y + (col - 1) * self.cell_size
            pygame.draw.rect(self.screen, self.blue, 
                            (x, y, self.cell_size, self.cell_size))

        # Draw dots with offset
        for position in self.dot_positions:
            row, col = position
            x = grid_x + (row - 1) * self.cell_size + self.cell_size // 2
            y = grid_y + (col - 1) * self.cell_size + self.cell_size // 2
            pygame.draw.circle(self.screen, self.white, (x, y), self.cell_size // 4)

        # Draw input box at bottom
        input_box_height = 80
        pygame.draw.rect(self.screen, self.gray, 
                        (20, self.screen_height - input_box_height - 20, 
                        self.screen_width - 40, input_box_height))
        input_surface = self.font.render(self.input_text, True, self.green)
        self.screen.blit(input_surface, (30, self.screen_height - input_box_height - 10))

        # Draw current player or game over message
        if not self.game_over:
            if self.game_mode == "ai_vs_ai":
                player_text = f"Current Player: AI {1 if self.current_player == 'player1' else 2}"
            else:
                player_text = f"Current Player: {'Human' if self.current_player == 'player1' else ('AI' if self.game_mode == 'ai' else 'Human 2')}"
            player_surface = self.font.render(player_text, True, self.white)
            self.screen.blit(player_surface, (20, self.screen_height - input_box_height - 80))
        else:
            winner_surface = self.font.render(self.winner_message, True, self.yellow)
            winner_rect = winner_surface.get_rect(center=(self.screen_width // 2, 
                                                        self.screen_height - input_box_height - 80))
            self.screen.blit(winner_surface, winner_rect)

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
            positions = [(x, y), (x, y - 1), (x - 1, y), (x - 2, y)]  # Flip upward
        else: 
            #print("Standard L-piece facing North at ({}, {})".format(x, y))
            positions = [(x, y), (x, y - 1), (x + 1, y), (x + 2, y)]

    elif orientation == 'S':  # Vertical arm down
        if x <= 2:  # Flip the piece if it's near the top edge
            #print("Flipping L-piece facing South near the top edge at ({}, {})".format(x, y))
            positions = [(x, y), (x, y + 1), (x + 1, y), (x + 2, y)]  # Flip downward
        else: 
            #("Standard L-piece facing South at ({}, {})".format(x, y))
            positions = [(x, y), (x, y + 1), (x - 1, y), (x - 2, y)]

    elif orientation == 'E':  # Horizontal arm right
        if y <= 2:  # Flip the piece if it's near the left edge
            #print("Flipping L-piece facing East near the left edge at ({}, {})".format(x, y))
            positions = [(x, y), (x + 1, y), (x, y + 1), (x, y + 2)]  # Flip rightward
        else: 
            #print("Standard L-piece facing East at ({}, {})".format(x, y))
            positions = [(x, y), (x + 1, y), (x, y - 1), (x, y - 2)]

    elif orientation == 'W':  # Horizontal arm left
        if y >= 3:  # Flip the piece if it's near the right edge
            #print("Flipping L-piece facing West near the right edge at ({}, {})".format(x, y))
            positions = [(x, y), (x - 1, y), (x, y - 1), (x, y - 2)]  # Flip leftward
        else:  
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