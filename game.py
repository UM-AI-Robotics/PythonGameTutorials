# 1 - Import library
import pygame as pg
import pygame.locals as pgl

# 2 - Initialize the game
pg.init()
width, height = 640, 480
screen = pg.display.set_mode((width, height))

# 3 - Load images
player = pg.image.load("resources/images/dude.png")

# 4 - Main loop
while True:
    # 5 - Clear old screen (fill with black)
    screen.fill(0)
    # 6 - Draw new screen elements
    screen.blit(player, (100, 100))
    # 7 - Update screen
    pg.display.flip()
    # 8 - Event loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)
