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
        print(f"Player {current.name}'s turn")
        # Select move based on player algorithm
        move = current.pick_move(game)
        # Apply move to the game
        game.apply_move(move)
        # Display the number of stones removed
        print(f"Stones removed: {move}")
        # Once game is over, display the losing player
        if game.is_game_over():
            game.display()
            print(f"Player {current.name} loses")
        # Switch current player
        game.switch_player()

p1 = players.HumanPlayer()
p2 = players.RandomAI()
play_nim(p1, p2)