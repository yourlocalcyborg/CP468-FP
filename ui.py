import pygame as pg
from nim import Nim
from players import HumanPlayer, RandomAI, MinimaxAI, AlphaBetaAI, ExpectiminimaxAI, GeminiAI
import random

def runUI():
   pg.init()
   screen = pg.display.set_mode((1280, 720))
   pg.display.set_caption("Nim Game UI")
   clock = pg.time.Clock()
   FONT = pg.font.SysFont(None, 36)
   button_rects = {}

   # Setup games and players
   game = Nim(10)
   player1 = HumanPlayer()
   player2 = random.choice([RandomAI(), MinimaxAI(), AlphaBetaAI(), ExpectiminimaxAI(), GeminiAI()])
   players = [player1, player2]

   ai_pending_move = False
   ai_timer_start = 0

   running = True
   # Continue looping though turns until game is over
   while running:
       current_player = players[game.current_player]

       # Draw screen 
       screen.fill("purple")
       draw(game, screen, FONT, button_rects, current_player)

       if current_player == player2 and not game.is_game_over():
           pg.time.wait(500)
           move = current_player.pick_move(game)
           game.apply_move(move)
           game.switch_player()
        
       for event in pg.event.get():
           if event.type == pg.QUIT:
               running = False
            # Check if player has clicked the mouse
           elif event.type == pg.MOUSEBUTTONDOWN and not game.is_game_over():
               # Loop through the buttons 
               for move, rect in button_rects.items():
                   # Check if the button was clicked and if so, apply the associated move
                   if rect.collidepoint(event.pos):
                       if game.apply_move(move):
                           game.switch_player()
                           break
           # Once game is over, display the winner
           if game.is_game_over():
               screen.fill("purple")
               winner = current_player.name
               text = FONT.render(f"Player {winner} wins!", True, "black")
               screen.blit(text, (1280 // 2 - 100, 720 // 2))
               pg.display.flip()
               pg.time.wait(3000)
               running = False
       pg.display.flip()
       clock.tick(60)
   pg.quit()

def draw(game, screen, font, buttons, current_player):
    # Draw current stones
    for i in range(game.stones):
        pg.draw.circle(screen, (0, 0, 0), (75 + i * 125, 100), 25)
    # Display current player's turn
    turn_text = font.render(f"Player {current_player.name}'s turn", True, (0, 0, 0))
    screen.blit(turn_text, (50, 200))
    # Draw buttons for all possible moves
    for move in game.moves:
        rect1 = pg.Rect(9 + move * 270, 390, 225, 125)
        rect2 = pg.Rect(20 + move * 270, 400, 200, 100)
        buttons[move] = rect2
        pg.draw.rect(screen, (0, 0, 0), rect1)
        pg.draw.rect(screen, (255, 255, 255), rect2)
        label = font.render(str(move), True, (0, 0, 0))
        screen.blit(label, (rect2.x + 90, rect2.y + 40))
    