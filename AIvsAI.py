#AI vs AI selection
from nim import Nim
from players import MinimaxAI, ExpectiminimaxAI, AlphaBetaAI, RandomAI, GeminiAI

# Dictionary to map user input to AI classes
ai_options = {
    "1": MinimaxAI,
    "2": ExpectiminimaxAI,
    "3": AlphaBetaAI,
    "4": RandomAI,
    "5": GeminiAI
}

print("Select AI for Player 1:")
print("1: MinimaxAI")
print("2: ExpectiminimaxAI")
print("3: AlphaBetaAI")
print("4: RandomAI")
print("5: GeminiAI")

player1_choice = input("Enter the number for Player 1's AI: ")
player1_class = ai_options.get(player1_choice)

if player1_class is None:
    print("Invalid choice for Player 1. Using RandomAI.")
    player1_class = RandomAI

print("\nSelect AI for Player 2:")
print("1: MinimaxAI")
print("2: ExpectiminimaxAI")
print("3: AlphaBetaAI")
print("4: RandomAI")
print("5: GeminiAI")


player2_choice = input("Enter the number for Player 2's AI: ")
player2_class = ai_options.get(player2_choice)

if player2_class is None:
    print("Invalid choice for Player 2. Using RandomAI.")
    player2_class = RandomAI

# Initialize game with 10 stones (or any desired initial number)
initial_stones = 10
game = Nim(initial_stones)

# Initialize players with selected AI classes
player1 = player1_class(name="Player 1")
player2 = player2_class(name="Player 2")

is_player1_turn = True

print(f"\nStarting a game with {initial_stones} stones: {player1.name} vs {player2.name}")

# Game loop for a single game
while not game.is_game_over():
    game.display()

    if is_player1_turn:
        move = player1.pick_move(game)
        print(f"{player1.name} chooses: {move}")
    else:
        move = player2.pick_move(game)
        print(f"{player2.name} chooses: {move}")

    game.apply_move(move)
    is_player1_turn = not is_player1_turn

# Game over
print("\nGame Over!")
if is_player1_turn:  # If it's player 1's turn after the game is over, player 2 won
    print(f"{player2.name} wins!")
else:
    print(f"{player1.name} wins!")
