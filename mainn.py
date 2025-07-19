import time
import nim
import players

def select_agent(player_num):
    print(f"\nSelect agent for Player {player_num}:")
    print("1. HumanPlayer")
    print("2. RandomAI")
    print("3. MinimaxAI")
    print("4. AlphaBetaAI")
    print("5. ExpectiminimaxAI")
    choice = input("Enter choice (1-5): ")

    if choice == "1":
        return players.HumanPlayer(f"P{player_num}-Human")
    elif choice == "2":
        return players.RandomAI(f"P{player_num}-Random")
    elif choice == "3":
        return players.MinimaxAI(f"P{player_num}-Minimax")
    elif choice == "4":
        return players.AlphaBetaAI(f"P{player_num}-AlphaBeta")
    elif choice == "5":
        return players.ExpectiminimaxAI(f"P{player_num}-Expectiminimax")
    else:
        print("Invalid choice. Defaulting to RandomAI.")
        return players.RandomAI(f"P{player_num}-Random")

def play_nim(player1, player2, total_stones=10, show_timing=True):
    game = nim.Nim(total_stones)
    player_list = [player1, player2]

    while not game.is_game_over():
        game.display()
        current = player_list[game.current_player]
        print(f"{current.name}'s turn")

        start = time.time()
        move = current.pick_move(game)
        elapsed = time.time() - start

        game.apply_move(move)
        print(f"Stones removed: {move} (Move time: {elapsed:.4f} seconds)")

        if game.is_game_over():
            game.display()
            print(f"{current.name} loses")

        game.switch_player()

    # Print node counts after game if available
    for p in [player1, player2]:
        if hasattr(p, "node_count"):
            print(f"{p.name} evaluated {p.node_count} nodes.")

def benchmark(agent_class_1, agent_class_2, stones_list=[10, 15, 20, 25]):
    print("\n--- Benchmarking Mode ---")
    for stones in stones_list:
        p1_wins = 0
        total_time = 0

        for _ in range(10):  # 10 games per size
            p1 = agent_class_1("Benchmark-P1")
            p2 = agent_class_2("Benchmark-P2")
            p1.node_count = 0
            p2.node_count = 0

            game = nim.Nim(stones)
            players_list = [p1, p2]
            game.current_player = 0

            start = time.time()
            while not game.is_game_over():
                current = players_list[game.current_player]
                move = current.pick_move(game)
                game.apply_move(move)
                if game.is_game_over() and game.current_player == 1:
                    p1_wins += 1
                game.switch_player()
            total_time += time.time() - start

        avg_time = total_time / 10
        print(f"\nStones: {stones}")
        print(f"  {agent_class_1.__name__} win rate: {p1_wins * 10}%")
        print(f"  Avg game time: {avg_time:.4f} s")
        print(f"  Avg nodes (P1): {p1.node_count}")
        print(f"  Avg nodes (P2): {p2.node_count}")

# MAIN MENU
print("Choose Mode:")
print("1. Play a game")
print("2. Run benchmark (AI vs Random)")
mode = input("Enter mode (1 or 2): ")

if mode == "1":
    p1 = select_agent(1)
    p2 = select_agent(2)
    stones = int(input("Enter total number of stones: "))
    play_nim(p1, p2, total_stones=stones)

elif mode == "2":
    print("\nBenchmark: Minimax vs Random")
    benchmark(players.MinimaxAI, players.RandomAI)

    print("\nBenchmark: AlphaBeta vs Random")
    benchmark(players.AlphaBetaAI, players.RandomAI)

    print("\nBenchmark: Expectiminimax vs Random")
    benchmark(players.ExpectiminimaxAI, players.RandomAI)

else:
    print("Invalid mode.")
