#1 - Import library
import math
import random
import pygame as pg
import pygame.locals as pgl

# 2 - Initialize the game
pg.init()
width, height = 640, 480
screen = pg.display.set_mode((width, height))
keys = [False, False, False, False]
playerpos = [100, 100]
acc = [0, 0]
arrows = []
badtimer = 100
badtimer1 = 0
badguys = [[640, 100]]
healthvalue = 194
# 3 - Load images
player = pg.image.load("resources/images/dude.png")
grass = pg.image.load("resources/images/grass.png")
castle = pg.image.load("resources/images/castle.png")
arrow = pg.image.load("resources/images/bullet.png")
badguyimg1 = pg.image.load("resources/images/badguy.png")
badguyimg = badguyimg1
# 4 - Main loop
while True:
    badtimer -= 1
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
    # 6.1 - Set player position and rotation
    position = pg.mouse.get_pos()
    delta_y = position[1] - playerpos[1] - 32
    delta_x = position[0] - playerpos[0] - 26
    angle = 360 - 57.29 * math.atan2(delta_y, delta_x)
    playerrot = pg.transform.rotate(player, angle)
    playerpos1 = (playerpos[0] - playerrot.get_rect().width/2, 
                    playerpos[1] - playerrot.get_rect().height/2)
    screen.blit(playerrot, playerpos1)
    # 6.2 - Draw arrows
    for bullet in arrows:
        index = 0
        velx = math.cos(bullet[0]) * 10
        vely = math.sin(bullet[0]) * 10
        bullet[1] += velx
        bullet[2] += vely
        if bullet[1] < -64 or bullet[1] > 640 or \
        bullet[2] < -64 or bullet[2] > 480:
            arrows.pop(index)
        index += 1
        for projectile in arrows:
            angle = 360 - projectile[0] * 57.29
            arrow1 = pg.transform.rotate(arrow, angle)
            screen.blit(arrow1, (projectile[1], projectile[2]))
    # 6.3 - Draw badgers
    if badtimer == 0:
        badguys.append([640, random.randint(50, 430)])
        badtimer = 100 - (badtimer1 * 2)
        if badtimer1 >= 35:
            badtimer1 = 35
        else:
            badtimer += 5
    index = 0
    for badguy in badguys:
        if badguy[0] < -64:
            badguys.pop(index)
        badguy[0] -= 7
        badrect = pg.Rect(badguyimg.get_rect())
        badrect.top = badguy[1]
        badrect.left = badguy[0]
        if badrect.left < 64:
            healthvalue -= random.randint(5, 20)
            badguys.pop(index)
        index += 1
    for badguy in badguys:
        screen.blit(badguyimg, badguy)

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

        if event.type == pg.MOUSEBUTTONDOWN:
            position = pg.mouse.get_pos()
            acc[1] += 1
            delta_y = position[1] - playerpos1[1] - 32
            delta_x = position[0] - playerpos1[0] - 26
            angle = math.atan2(delta_y, delta_x)
            arrows.append([angle,
                            playerpos1[0] + 32, 
                            playerpos1[1] + 32])
            
    if keys[0]:
        playerpos[1] -= 5
    elif keys[2]:
        playerpos[1] += 5
    elif keys[1]:
        playerpos[0] -= 5
    elif keys[3]:
        playerpos[0] += 5
