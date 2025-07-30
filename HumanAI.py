#Human vs AI
from nim import Nim
from players import MinimaxAI, ExpectiminimaxAI, AlphaBetaAI, RandomAI, GeminiAI, HumanPlayer

# Dictionary to map user input to AI classes
ai_options = {
    "1": MinimaxAI,
    "2": ExpectiminimaxAI,
    "3": AlphaBetaAI,
    "4": RandomAI,
    "5": GeminiAI
}

print("Select your opponent (AI):")
print("1: MinimaxAI")
print("2: ExpectiminimaxAI")
print("3: AlphaBetaAI")
print("4: RandomAI")
print("5: GeminiAI")

opponent_choice = input("Enter the number for your AI opponent: ")
opponent_class = ai_options.get(opponent_choice)

if opponent_class is None:
    print("Invalid choice for AI opponent. Using RandomAI.")
    opponent_class = RandomAI

# Initialize game with 10 stones (or any desired initial number)
initial_stones = 10
game = Nim(initial_stones)

# Initialize players: HumanPlayer and the chosen AI
player1 = HumanPlayer(name="Human")
player2 = opponent_class(name=opponent_class.__name__)

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
