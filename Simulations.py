import re
import io
import sys

simulation_results = []

for i in range(len(ai_players_to_evaluate)):
    for j in range(i, len(ai_players_to_evaluate)):
        player1_class = ai_players_to_evaluate[i]
        player2_class = ai_players_to_evaluate[j]

        print(f"Simulating: {player1_class.__name__} vs {player2_class.__name__}")

        # Capture the output
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output

        run_performance_evaluation(player1_class, player2_class, num_games=100, initial_stones=10)

        # Restore stdout
        sys.stdout = old_stdout

        output_string = redirected_output.getvalue()
        print(output_string) # Print the captured output to the notebook

        # Parse the output
        metrics = {}
        metrics['player1'] = player1_class.__name__
        metrics['player2'] = player2_class.__name__

        win_rate_match = re.search(r'(\w+) Win Rate: ([\d.]+)', output_string)
        if win_rate_match:
            player_name = win_rate_match.group(1)
            win_rate = float(win_rate_match.group(2))
            if player_name == metrics['player1']:
                metrics['player1_win_rate'] = win_rate
            else:
                 metrics['player2_win_rate'] = win_rate

        win_rate_match_2 = re.search(r'(\w+) Win Rate: ([\d.]+)', output_string[win_rate_match.end():])
        if win_rate_match_2:
            player_name = win_rate_match_2.group(1)
            win_rate = float(win_rate_match_2.group(2))
            if player_name == metrics['player1']:
                metrics['player1_win_rate'] = win_rate
            else:
                 metrics['player2_win_rate'] = win_rate

        total_time_match = re.search(r'Total Game Time: ([\d.]+)', output_string)
        if total_time_match:
            metrics['total_game_time'] = float(total_time_match.group(1))

        avg_time_match = re.search(r'Average Game Time: ([\d.]+)', output_string)
        if avg_time_match:
            metrics['average_game_time'] = float(avg_time_match.group(1))

        p1_total_nodes_match = re.search(rf'{player1_class.__name__} Total Nodes Explored: ([\d]+)', output_string)
        if p1_total_nodes_match:
            metrics['player1_total_nodes'] = int(p1_total_nodes_match.group(1))

        p1_avg_nodes_match = re.search(rf'{player1_class.__name__} Average Nodes Explored per Game: ([\d.]+)', output_string)
        if p1_avg_nodes_match:
            metrics['player1_average_nodes'] = float(p1_avg_nodes_match.group(1))

        p2_total_nodes_match = re.search(rf'{player2_class.__name__} Total Nodes Explored: ([\d]+)', output_string)
        if p2_total_nodes_match:
            metrics['player2_total_nodes'] = int(p2_total_nodes_match.group(1))

        p2_avg_nodes_match = re.search(rf'{player2_class.__name__} Average Nodes Explored per Game: ([\d.]+)', output_string)
        if p2_avg_nodes_match:
            metrics['player2_average_nodes'] = float(p2_avg_nodes_match.group(1))


        simulation_results.append(metrics)

print("\nSimulation Results:")
print(simulation_results)
