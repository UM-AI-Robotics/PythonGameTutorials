# 1 - Import library
import pygame as pg
import pygame.locals as pgl

# 2 - Initialize the game
pg.init()
width, height = 640, 480
screen = pg.display.set_mode((width, height))
keys = [False, False, False, False]
playerpos = [100, 100]

# 3 - Load images
player = pg.image.load("resources/images/dude.png")
grass = pg.image.load("resources/images/grass.png")
castle = pg.image.load("resources/images/castle.png")

# 4 - Main loop
while True:
    # 5 - Clear old screen (fill with black)
    screen.fill(0)
    # 6 - Draw new screen elements
    # 6.0 - Scenery
    # 6.01 - Tile grass (nx by ny)
    grass_nx = width/grass.get_width() + 1
    grass_ny = width/grass.get_height() + 1
    for x in range(grass_nx):
        for y in range(grass_ny):
            screen.blit(grass, (x * 100, y * 100))
    # 6.02 - Place castles
    screen.blit(castle, (0, 30))
    screen.blit(castle, (0, 135))
    screen.blit(castle, (0, 240))
    screen.blit(castle, (0, 345))
    screen.blit(player, playerpos)

    # 7 - Update screen
    pg.display.flip()
    # 8 - Event loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)

        if event.type == pg.KEYDOWN:
            if event.key == pgl.K_w:
                keys[0] = True
            elif event.key == pgl.K_a:
                keys[1] = True
            elif event.key == pgl.K_s:
                keys[2] = True
            elif event.key == pgl.K_d:
                keys[3] = True

        if event.type == pg.KEYUP:
            if event.key == pgl.K_w:
                keys[0] = False
            elif event.key == pgl.K_a:
                keys[1] = False
            elif event.key == pgl.K_s:
                keys[2] = False
            elif event.key == pgl.K_d:
                keys[3] = False

    if keys[0]:
        playerpos[1] -= 5
    elif keys[2]:
        playerpos[1] += 5
    elif keys[1]:
        playerpos[0] -= 5
    elif keys[3]:
        playerpos[0] += 5
