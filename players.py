import random
from nim import Nim

class HumanPlayer():
    def __init__(self, name="Human"):
        self.name = name
        
    def pick_move(self, game):
        while True:
            move = int(input("Select number of stones to take (1-3): "))
            if move in game.is_valid_move():
                return move
            else:
                print("Invalid selection")
            
class RandomAI():
    def __init__(self, name="Random"):
        self.name = name
    def pick_move(self, game):
        return random.choice(game.is_valid_move())
        

class MinimaxAI():
    def __init__(self, name="Minimax"):
        self.name = name

    def pick_move(self, game):
        _, move = self.minimax(game, True)
        return move

    def minimax(self, game, is_maximizing):
        if game.is_game_over():
            return (-1 if is_maximizing else 1), None  # Losing state

        best_val = float('-inf') if is_maximizing else float('inf')
        best_move = None

        for move in game.is_valid_move():
            clone = Nim(game.stones - move)
            val, _ = self.minimax(clone, not is_maximizing)
            if is_maximizing:
                if val > best_val:
                    best_val, best_move = val, move
            else:
                if val < best_val:
                    best_val, best_move = val, move

        return best_val, best_move

class AlphaBetaAI():
    def __init__(self, name="AlphaBeta"):
        self.name = name

    def pick_move(self, game):
        _, move = self.alphabeta(game, True, float('-inf'), float('inf'))
        return move

    def alphabeta(self, game, is_maximizing, alpha, beta):
        if game.is_game_over():
            return (-1 if is_maximizing else 1), None

        best_move = None

        if is_maximizing:
            max_eval = float('-inf')
            for move in game.is_valid_move():
                if game.stones - move < 0:
                    continue
                next_state = Nim(game.stones - move)
                eval, _ = self.alphabeta(next_state, False, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move

        else:
            min_eval = float('inf')
            for move in game.is_valid_move():
                if game.stones - move < 0:
                    continue
                next_state = Nim(game.stones - move)
                eval, _ = self.alphabeta(next_state, True, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

class ExpectiminimaxAI():
    def __init__(self, name="Expectiminimax"):
        self.name = name

    def pick_move(self, game):
        _, move = self.expectiminimax(game, True)
        return move

    def expectiminimax(self, game, is_maximizing):
        if game.is_game_over():
            return (-1 if is_maximizing else 1), None

        if is_maximizing:
            max_val = float('-inf')
            best_move = None
            for move in game.is_valid_move():
                if game.stones - move < 0:
                    continue
                next_state = Nim(game.stones - move)
                val = self.chance_node(next_state, False)
                if val > max_val:
                    max_val = val
                    best_move = move
            return max_val, best_move
        else:
            min_val = float('inf')
            best_move = None
            for move in game.is_valid_move():
                if game.stones - move < 0:
                    continue
                next_state = Nim(game.stones - move)
                val = self.chance_node(next_state, True)
                if val < min_val:
                    min_val = val
                    best_move = move
            return min_val, best_move

    def chance_node(self, game, is_maximizing):
        """
        Simulate chance: 50% chance that an extra stone is removed randomly (1-2).
        Expected value = average of all outcomes.
        """
        outcomes = []

        # No random effect
        outcomes.append(self.expectiminimax(game, is_maximizing)[0])

        # Simulated randomness (e.g., penalty)
        for penalty in [1, 2]:
            if game.stones - penalty >= 0:
                next_state = Nim(game.stones - penalty)
                val, _ = self.expectiminimax(next_state, is_maximizing)
                outcomes.append(val)

        return sum(outcomes) / len(outcomes)

