import pygame, random, sys, os, time
from pygame.locals import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 8
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 8
PLAYERMOVERATE = 5
WALLSPEED = 8
count = 3
topScore=0

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # escape quits
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('car race')
pygame.mouse.set_visible(False)

playerImage = pygame.image.load('car1.png')
car3 = pygame.image.load('car3.png')
car4 = pygame.image.load('car4.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('car2.png')
sample = [car3, car4, baddieImage]

wallLeft = pygame.image.load("left.png")
wallLeft_size = wallLeft.get_rect().size
wallLeft_width = wallLeft_size[0]
wallLeft_height = wallLeft_size[1]
wallLeft_x_pos = 0
wallLeft_y_pos = 0

wallLeft2 = pygame.image.load("left.png")
wallLeft2_size = wallLeft2.get_rect().size
wallLeft2_width = wallLeft2_size[0]
wallLeft2_height = wallLeft2_size[1]
wallLeft2_x_pos = 0
wallLeft2_y_pos = -WINDOWHEIGHT

wallRight = pygame.image.load("right.png")
wallRight_size = wallRight.get_rect().size
wallRight_width = wallRight_size[0]
wallRight_height = wallRight_size[1]
wallRight_x_pos = 0
wallRight_y_pos = 0

wallRight2 = pygame.image.load("right.png")
wallRight2_size = wallRight2.get_rect().size
wallRight2_width = wallRight2_size[0]
wallRight2_height = wallRight2_size[1]
wallRight2_x_pos = 0
wallRight2_y_pos = -WINDOWHEIGHT

font = pygame.font.SysFont(None, 42)
drawText('PRESS ANY KEY TO START THE GAME!', font, windowSurface, (WINDOWWIDTH / 3) - 137, (WINDOWHEIGHT / 3)+80)
pygame.display.update()
waitForPlayerToPressKey()
zero = 0

while (count > 0):
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0

    while True:
        score += 1

        for event in pygame.event.get():

            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    # score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    # score = 0
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False


        if not reverseCheat and not slowCheat:
            WALLSPEED = 8
        if reverseCheat:
            WALLSPEED = -3
        if slowCheat:
            WALLSPEED = 1
            
        wallLeft_y_pos += WALLSPEED
        if wallLeft_y_pos > WINDOWHEIGHT:
            wallLeft_y_pos = 0
            wallLeft_x_pos = 0

        wallRight_y_pos += WALLSPEED
        if wallRight_y_pos > WINDOWHEIGHT:
            wallRight_y_pos = 0
            wallRight_x_pos = WINDOWWIDTH - wallRight_width
       
        wallLeft2_y_pos += WALLSPEED
        if wallLeft2_y_pos > 0:
            wallLeft2_y_pos = -WINDOWHEIGHT
            wallLeft2_x_pos = 0

        wallRight2_y_pos += WALLSPEED
        if wallRight2_y_pos > 0:
            wallRight2_y_pos = -WINDOWHEIGHT
            wallRight2_x_pos = WINDOWWIDTH - wallRight2_width

        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = 30
            newBaddie = {'rect': pygame.Rect(random.randint(140, 485), 0 - baddieSize, 23, 47),
                         'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                         'surface': pygame.transform.scale(random.choice(sample), (23, 47)),
                         }
            baddies.append(newBaddie)

            # sideLeft = {'rect': pygame.Rect(0, 0, 126, 600),
            #             'speed': 1,
            #             'surface': pygame.transform.scale(wallLeft, (126, 599)),
            #             }
            # walls.append(sideLeft)
            # sideRight = {'rect': pygame.Rect(497, 0, 303, 600),
            #              'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
            #              'surface': pygame.transform.scale(wallRight, (303, 599)),
            #              }
            # baddies.append(sideRight)

        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)
                


        font = pygame.font.SysFont(None, 38)
        windowSurface.fill(BACKGROUNDCOLOR)
        drawText('Score: %s' % (score), font, windowSurface, 128, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 128, 21)
        drawText('Rest Life: %s' % (count), font, windowSurface, 128, 41)

        windowSurface.blit(playerImage, playerRect)

        windowSurface.blit(wallLeft, (wallLeft_x_pos, wallLeft_y_pos))
        windowSurface.blit(wallRight, ((WINDOWWIDTH - wallRight_width), wallRight_y_pos) )
        windowSurface.blit(wallLeft2, (wallLeft2_x_pos, wallLeft2_y_pos))
        windowSurface.blit(wallRight2, ((WINDOWWIDTH - wallRight2_width), wallRight2_y_pos) )

        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score
            break

        wallLeft_rect = wallLeft.get_rect()
        wallLeft_rect.left = wallLeft_x_pos
        wallLeft_rect.top = wallLeft_y_pos
        wallLeft2_rect = wallLeft2.get_rect()
        wallLeft2_rect.left = wallLeft2_x_pos
        wallLeft2_rect.top = wallLeft2_y_pos
        wallRight_rect = wallRight.get_rect()
        wallRight_rect.left = wallRight_x_pos
        wallRight_rect.top = wallRight_y_pos
        wallRight2_rect = wallRight2.get_rect()
        wallRight2_rect.left = wallRight2_x_pos
        wallRight2_rect.top = wallRight2_y_pos


        if playerRect.colliderect(wallLeft_rect):
            if score > topScore:
                topScore = score
            break
        if playerRect.colliderect(wallLeft2_rect):
            if score > topScore:
                topScore = score
            break
        if playerRect.colliderect(wallRight_rect):
            if score > topScore:
                topScore = score
            break
        if playerRect.colliderect(wallRight2_rect):
            if score > topScore:
                topScore = score
            break



        mainClock.tick(FPS)

    count = count - 1
    time.sleep(1)
    font = pygame.font.SysFont(None, 52)
    if (count == 0):

        drawText('Game Over', font, windowSurface, (WINDOWWIDTH / 3)+40, (WINDOWHEIGHT / 3)+70)
        drawText('Press any key to play again.', font, windowSurface, (WINDOWWIDTH /3) - 110, (WINDOWHEIGHT / 3) + 95)
        pygame.display.update()
        time.sleep(2)
        waitForPlayerToPressKey()
        count = 3


