import pygame
import sys

pygame.init()
bg = pygame.image.load("img/bg.png")
screen = pygame.display.set_mode([1200, 595])  # open program window
clock = pygame.time.Clock()  # clock
pygame.display.set_caption("MakerKids Pygame Tutorial")

# load still images for several body positions
stand = pygame.image.load("img/stand.png")
jump = pygame.image.load("img/jump.png")

# load image sequence for right walk animation
moveright = [pygame.image.load("img/right1.png"),
             pygame.image.load("img/right2.png"),
             pygame.image.load("img/right3.png"),
             pygame.image.load("img/right4.png"),
             pygame.image.load("img/right5.png"),
             pygame.image.load("img/right6.png"),
             pygame.image.load("img/right7.png"),
             pygame.image.load("img/right8.png")]
# load image sequence for left walk animation
moveleft = [pygame.image.load("img/left1.png"),
            pygame.image.load("img/left2.png"),
            pygame.image.load("img/left3.png"),
            pygame.image.load("img/left4.png"),
            pygame.image.load("img/left5.png"),
            pygame.image.load("img/left6.png"),
            pygame.image.load("img/left7.png"),
            pygame.image.load("img/left8.png")]

jumpsound = pygame.mixer.Sound("snd/jump.wav")


def draw(dlist):
    global stepsleft, stepsright
    screen.blit(bg, (0, 0))  # show background image

    if stepsleft == 63:
        stepsleft = 0
    if stepsright == 63:
        stepsright = 0

    if dlist[0]:
        screen.blit(moveleft[stepsleft // 8], (int(x), int(y)))

    if dlist[1]:
        screen.blit(moveright[stepsright // 8], (int(x), int(y)))

    if dlist[2]:
        screen.blit(stand, (int(x), int(y)))

    if dlist[3]:
        screen.blit(jump, (int(x), int(y)))

    pygame.display.update()


x = 400  # position pointer x
y = 393  # position pointer y
speed = 5  # pixels per move
width = 40
height = 80

wallleft = pygame.draw.rect(screen, (0, 0, 0), (-2, 0, 2, 600), 0)
wallright = pygame.draw.rect(screen, (0, 0, 0), (1201, 0, 2, 600), 0)

active = True  # set game active
jumpvar = -16

# params: [left, right, stand, jump]
direction = [0, 0, 0, 0]
stepsleft = 0  # step counter left direction
stepsright = 0  # step counter right direction

# main program
while active:
    for event in pygame.event.get():  # read events
        if event.type == pygame.QUIT:
            sys.exit()  # exit program

    playerrect = pygame.Rect(int(x), int(y), 96, 128)

    # evaluate keyboard inputs
    pressed = pygame.key.get_pressed()

    direction = [0, 0, 1, 0]

    # jump
    if pressed[pygame.K_UP] and jumpvar == -16:
        jumpvar = 15

    # move left
    if pressed[pygame.K_LEFT] and not playerrect.colliderect(wallleft):
        x -= speed
        direction = [1, 0, 0, 0]
        stepsleft += 1

    # move right
    if pressed[pygame.K_RIGHT] and not playerrect.colliderect(wallright):
        x += speed
        direction = [0, 1, 0, 0]
        stepsright += 1

    if jumpvar == 15:
        pygame.mixer.Sound.play(jumpsound)

    if jumpvar >= -15:
        direction = [0, 0, 0, 1]
        n = 1
        if jumpvar < 0:
            n = -1

        y -= (jumpvar**2) * 0.17 * n
        jumpvar -= 1

    if direction[2] or direction[3]:
        stepsleft = 0
        stepsright = 0

    draw(direction)
    clock.tick(60)  # adjust screen frequency
