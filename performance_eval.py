import time
from nim import Nim
from players import MinimaxAI, ExpectiminimaxAI, AlphaBetaAI, RandomAI

def run_performance_evaluation(player1_class, player2_class, num_games=100, initial_stones=10):
    """
    Runs multiple games between two AI players and tracks performance metrics.

    Args:
        player1_class: The class for player 1 (e.g., MinimaxAI).
        player2_class: The class for player 2 (e.g., ExpectiminimaxAI).
        num_games (int): The number of games to simulate.
        initial_stones (int): The initial number of stones in the Nim game.
    """
    player1_wins = 0
    player2_wins = 0
    total_game_time = 0.0
    player1_total_nodes = 0
    player2_total_nodes = 0

    print(f"Running {num_games} games with initial stones = {initial_stones}...")

    for i in range(num_games):
        game_start_time = time.time()

        game = Nim(initial_stones)
        player1 = player1_class(name="Player 1") # Use generic names for the function
        player2 = player2_class(name="Player 2")

        is_player1_turn = True

        while not game.is_game_over():
            if is_player1_turn:
                move = player1.pick_move(game)
            else:
                move = player2.pick_move(game)

            game.apply_move(move)
            is_player1_turn = not is_player1_turn

        game_end_time = time.time()
        game_duration = game_end_time - game_start_time
        total_game_time += game_duration

        # Assuming AI classes have a node_count attribute
        if hasattr(player1, 'node_count'):
             player1_total_nodes += player1.node_count
        if hasattr(player2, 'node_count'):
             player2_total_nodes += player2.node_count


        if is_player1_turn:  # If it's player 1's turn after the game is over, player 2 won
            player2_wins += 1
        else:
            player1_wins += 1

        # Optional: Print progress
        if (i + 1) % 10 == 0:
            print(f"Completed {i + 1} games...")


    # --- Report Performance ---
    player1_win_rate = player1_wins / num_games
    player2_win_rate = player2_wins / num_games
    average_game_time = total_game_time / num_games
    player1_average_nodes = player1_total_nodes / num_games
    player2_average_nodes = player2_total_nodes / num_games

    print(f"\n--- Performance Metrics ({player1.__class__.__name__} vs {player2.__class__.__name__}) ---")
    print(f"{player1.__class__.__name__} Win Rate: {player1_win_rate:.2f}")
    print(f"{player2.__class__.__name__} Win Rate: {player2_win_rate:.2f}")
    print(f"Total Game Time: {total_game_time:.2f} seconds")
    print(f"Average Game Time: {average_game_time:.4f} seconds") # More precision for average time
    print(f"{player1.__class__.__name__} Total Nodes Explored: {player1_total_nodes}")
    print(f"{player1.__class__.__name__} Average Nodes Explored per Game: {player1_average_nodes:.2f}")
    print(f"{player2.__class__.__name__} Total Nodes Explored: {player2_total_nodes}")
    print(f"{player2.__class__.__name__} Average Nodes Explored per Game: {player2_average_nodes:.2f}")
