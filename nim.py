class Nim:

    def __init__(self, total_stones):
        self.stones = total_stones
        self.current_player = 0
        self.moves = [1, 2, 3]
        
    def switch_player(self):
        self.current_player = 1 - self.current_player
        
    def is_game_over(self):
        return self.stones <= 0
    
    def is_valid_move(self):
        return self.moves 
    
    def apply_move(self, move):
        if move in self.is_valid_move():
            self.stones -= move
            return True
        else:
            return False
        
    def display(self):
        # Display stones in a 1D grid
        if self.stones > 0:
            grid = ["O"] * self.stones
            print(' '.join(grid))
        print(f"Stones remaining: {self.stones}")