import random
import time
import re
import io
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import google.generativeai as genai
import os


from nim import Nim
from players import MinimaxAI, ExpectiminimaxAI, AlphaBetaAI, RandomAI, GeminiAI, HumanPlayer

# --- Performance Evaluation Function ---
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
        # Re-initialize players for each game to reset node counts
        player1 = player1_class(name=player1_class.__name__)
        player2 = player2_class(name=player2_class.__name__)


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
    player1_average_nodes = player1_total_nodes / num_games if num_games > 0 else 0
    player2_average_nodes = player2_total_nodes / num_games if num_games > 0 else 0


    print(f"\n--- Performance Metrics ({player1_class.__name__} vs {player2_class.__name__}) ---")
    print(f"{player1_class.__name__} Win Rate: {player1_win_rate:.2f}")
    print(f"{player2_class.__name__} Win Rate: {player2_win_rate:.2f}")
    print(f"Total Game Time: {total_game_time:.2f} seconds")
    print(f"Average Game Time: {average_game_time:.4f} seconds") # More precision for average time
    print(f"{player1_class.__name__} Total Nodes Explored: {player1_total_nodes}")
    print(f"{player1_class.__name__} Average Nodes Explored per Game: {player1_average_nodes:.2f}")
    print(f"{player2_class.__name__} Total Nodes Explored: {player2_total_nodes}")
    print(f"{player2_class.__name__} Average Nodes Explored per Game: {player2_average_nodes:.2f}")

    return {
        'player1': player1_class.__name__,
        'player2': player2_class.__name__,
        'player1_win_rate': player1_win_rate,
        'player2_win_rate': player2_win_rate,
        'total_game_time': total_game_time,
        'average_game_time': average_game_time,
        'player1_total_nodes': player1_total_nodes,
        'player1_average_nodes': player1_average_nodes,
        'player2_total_nodes': player2_total_nodes,
        'player2_average_nodes': player2_average_nodes,
    }


# --- Identify AI players ---
ai_options = {
    "1": MinimaxAI,
    "2": ExpectiminimaxAI,
    "3": AlphaBetaAI,
    "4": RandomAI,
    # Exclude GeminiAI for this evaluation
    # "5": GeminiAI
}

ai_players_to_evaluate = [ai_options["1"], ai_options["2"], ai_options["3"], ai_options["4"]]

# --- Run simulations ---
simulation_results = []

for i in range(len(ai_players_to_evaluate)):
    for j in range(i, len(ai_players_to_evaluate)):
        player1_class = ai_players_to_evaluate[i]
        player2_class = ai_players_to_evaluate[j]

        # Capture the output of run_performance_evaluation
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output

        metrics = run_performance_evaluation(player1_class, player2_class, num_games=100, initial_stones=10)

        # Restore stdout
        sys.stdout = old_stdout

        output_string = redirected_output.getvalue()
        print(output_string) # Print the captured output to the console/notebook

        simulation_results.append(metrics)

print("\nSimulation Results:")
print(simulation_results)


# --- Organize results into DataFrame ---
df_results = pd.DataFrame(simulation_results)

# --- Display summary table ---
print("\n--- Summary Table ---")
print(df_results.to_string()) # Use to_string() to display the entire DataFrame without truncation

# --- Generate charts ---
# Create a bar chart visualizing the win rates for each player when they are designated as 'player1'
plt.figure(figsize=(10, 6))
sns.barplot(x='player1', y='player1_win_rate', data=df_results)
plt.xlabel('Player 1 AI')
plt.ylabel('Win Rate')
plt.title('Win Rates for Player 1 AI')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Create a bar chart visualizing the win rates for each player when they are designated as 'player2'
plt.figure(figsize=(10, 6))
sns.barplot(x='player2', y='player2_win_rate', data=df_results)
plt.xlabel('Player 2 AI')
plt.ylabel('Win Rate')
plt.title('Win Rates for Player 2 AI')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Create a bar chart visualizing the average game time for each simulation pair
plt.figure(figsize=(12, 6))
df_results['player_pair'] = df_results['player1'] + ' vs ' + df_results['player2']
sns.barplot(x='player_pair', y='average_game_time', data=df_results)
plt.xlabel('Player Pair')
plt.ylabel('Average Game Time (seconds)')
plt.title('Average Game Time for AI Player Pairs')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Create a bar chart visualizing the average nodes explored for player1
plt.figure(figsize=(10, 6))
sns.barplot(x='player1', y='player1_average_nodes', data=df_results)
plt.xlabel('Player 1 AI')
plt.ylabel('Average Nodes Explored')
plt.title('Average Nodes Explored by Player 1 AI')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Create a bar chart visualizing the average nodes explored for player2
plt.figure(figsize=(10, 6))
sns.barplot(x='player2', y='player2_average_nodes', data=df_results)
plt.xlabel('Player 2 AI')
plt.ylabel('Average Nodes Explored')
plt.title('Average Nodes Explored by Player 2 AI')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
