import nim
import players
def play_nim(player1, player2, total_stones=10):
    
    game = nim.Nim(total_stones)
    player_list = [player1, player2]
    
    while not game.is_game_over():
        # Display remaining stones
        game.display()
        # Get current player
        current = player_list[game.current_player]
        print(f"\nPlayer {current.name}'s turn")
        # Select move based on player algorithm
        move = current.pick_move(game)
        # Apply move to the game
        game.apply_move(move)
        # Display the number of stones removed
        print(f"Stones removed: {move}")
        # Once game is over, display the losing player
        if game.is_game_over():
            game.display()
            print(f"Player {current.name} wins!")
        # Switch current player
        game.switch_player()

def pick_ai():
    choice = input("(1) Random\n(2) Minimax\n(3) Alpha Beta\n(4) Expectiminimax\n> ")
    if not choice.isdigit():
        # Show input menu if incorrect input given
        print("Please enter a given integer")
        return pick_ai()
    else:
        if int(choice) == 1:
            return players.RandomAI()
        if int(choice) == 2:
            return players.MinimaxAI()
        if int(choice) == 3:
            return players.AlphaBetaAI()
        if int(choice) == 4:
            return players.ExpectiminimaxAI()
        else:
            print("Please enter a given integer")
            return pick_ai()

def compare_ai():
    print("TODO\n")
        
def get_players():
    gamemode = input("Choose a game mode:\n(1) Player vs AI\n(2) AI vs AI\n(3) Compare AIs\n> ")
    if not gamemode.isdigit():
        print("Please enter a given integer")
        return get_players()
    else:
        # Player vs AI
        if int(gamemode) == 1:
            p1 = players.HumanPlayer()
            print("Please choose an AI for player 2")
            p2 = pick_ai()
        # AI vs AI
        elif int(gamemode) == 2:
            print("Please choose an AI for player 1")
            p1 = pick_ai()
            print("Please choose an AI for player 2")
            p2 = pick_ai()
        # Compare AI
        elif int(gamemode) == 3:
            compare_ai()
            p1, p2 = None, None
        else:
            print("Please enter a given integer")
            return get_players()
        return p1, p2
        
p1, p2 = get_players()
if not (p1 == None or p2 == None):
    play_nim(p1, p2)
