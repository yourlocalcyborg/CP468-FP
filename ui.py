import pygame as pg

def runUI():
   pg.init()
   screen = pg.display.set_mode((1280, 720))
   clock = pg.time.Clock()
   running = True

   while running:
       screen.fill("purple")

       for event in pg.event.get():
           if event.type == pg.QUIT:
               running = False

       pg.display.flip()
       clock.tick(60)
    pg.quit()
