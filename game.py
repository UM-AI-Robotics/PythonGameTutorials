#1 - Import libraries
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
pg.mixer.init()

# 3 - Load images
player = pg.image.load("resources/images/dude.png")
grass = pg.image.load("resources/images/grass.png")
castle = pg.image.load("resources/images/castle.png")
arrow = pg.image.load("resources/images/bullet.png")
badguyimg1 = pg.image.load("resources/images/badguy.png")
badguyimg = badguyimg1
healthbar = pg.image.load("resources/images/healthbar.png")
health = pg.image.load("resources/images/health.png")
gameover = pg.image.load("resources/images/gameover.png")
youwin = pg.image.load("resources/images/youwin.png")
# 3.1 - Load audio
hit = pg.mixer.Sound("resources/audio/explode.wav")
enemy = pg.mixer.Sound("resources/audio/enemy.wav")
shoot = pg.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pg.mixer.music.load("resources/audio/moonlight.wav")
pg.mixer.music.play(-1, 0.0)
pg.mixer.music.set_volume(0.25)

# 4 - Main loop
running = 1
exitcode = 0
while running:
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
        # 6.3.1 - Attack castle
        badrect = pg.Rect(badguyimg.get_rect())
        badrect.top = badguy[1]
        badrect.left = badguy[0]
        if badrect.left < 64:
            hit.play()
            healthvalue -= random.randint(5, 20)
            badguys.pop(index)
        # 6.3.2 - Check for collisions
        index1 = 0
        for bullet in arrows:
            bullrect = pg.Rect(arrow.get_rect())
            bullrect.left = bullet[1]
            bullrect.top = bullet[2]
            if badrect.colliderect(bullrect):
                enemy.play()
                acc[0] += 1
                badguys.pop(index)
                arrows.pop(index1)
            index1 += 1
        # 6.3.3 - Next bad guy
        index += 1
    for badguy in badguys:
        screen.blit(badguyimg, badguy)
    # 6.4 - Draw clock
    mins = (90000 - pg.time.get_ticks()) / 60000
    secs  = (90000 - pg.time.get_ticks()) / 1000 % 60
    clock_str = str(mins) + ':' + str(secs).zfill(2)
    font = pg.font.Font(None, 24)
    survivedtext = font.render(clock_str, True, (0, 0, 0))
    textRect = survivedtext.get_rect()
    textRect.topright = [635, 5]
    screen.blit(survivedtext, textRect)
    # 6.5 - Draw health bar
    screen.blit(healthbar, (5, 5))
    for health1 in range(healthvalue):
        screen.blit(health, (health1 + 8, 8))

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
            shoot.play()
            position = pg.mouse.get_pos()
            acc[1] += 1
            delta_y = position[1] - playerpos1[1] - 32
            delta_x = position[0] - playerpos1[0] - 26
            angle = math.atan2(delta_y, delta_x)
            arrows.append([angle,
                            playerpos1[0] + 32, 
                            playerpos1[1] + 32])
            
    # 9 - Move player
    if keys[0]:
        playerpos[1] -= 5
    elif keys[2]:
        playerpos[1] += 5
    elif keys[1]:
        playerpos[0] -= 5
    elif keys[3]:
        playerpos[0] += 5

    #10 - Win/Lose check
    if pg.time.get_ticks() >= 90000:
        running = 0
        exitcode = 1
    if healthvalue <= 0:
        running = 0
        exitcode = 0
    if acc[1] != 0:
        accuracy = acc[0] * 1.0/acc[1] * 100
    else:
        accuracy = 0

#11 = Win/lose display
if exitcode == 0:
    pg.font.init()
    font = pg.font.Font(None, 24)
    acc_str = "Accuracy: " + str(accuracy) + "%"
    text = font.render(acc_str, True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(gameover, (0,0))
    screen.blit(text, textRect)
else:
    pg.font.init()
    font = pg.font.Font(None, 24)
    acc_str = "Accuracy: " + str(accuracy) + "%"
    text = font.render(acc_str, True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(youwin, (0,0))
    screen.blit(text, textRect)
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)
    pg.display.flip()
