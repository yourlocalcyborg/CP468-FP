import random
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