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


class Player:

    def __init__(self, x, y, speed, width, height, jumpvar, direction, stepsleft, stepsright):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.jumpvar = jumpvar
        self.direction = direction
        self.stepsleft = stepsleft
        self.stepsright = stepsright
        self.jump = False

    def move(self, dlist):
        # move left
        if dlist[0]:
            self.x -= self.speed
            self.direction = [1, 0, 0, 0]  # params: [left, right, stand, jump]
            self.stepsleft += 1
        # move right
        if dlist[1]:
            self.x += self.speed
            self.direction = [0, 1, 0, 0]  # params: [left, right, stand, jump]
            self.stepsright += 1

    def resetsteps(self):
        self.stepsleft = 0
        self.stepsright = 0

    def stand(self):
        self.direction = [0, 0, 1, 0]
        self.resetsteps()

    def setjump(self):
        if self.jumpvar == -16:
            self.jump = True
            self.jumpvar = 15
            pygame.mixer.Sound.play(jumpsound)

    def dojump(self):
        if self.jump:
            self.direction = [0, 0, 0, 1]
            if self.jumpvar >= -15:
                n = 1
                if self.jumpvar < 0:
                    n = -1
                self.y -= (self.jumpvar ** 2) * 0.17 * n
                self.jumpvar -= 1
            else:
                self.jump = False

    def drawplayer(self):
        if self.stepsleft == 63:
            self.stepsleft = 0
        if self.stepsright == 63:
            self.stepsright = 0

        if self.direction[0]:
            screen.blit(moveleft[self.stepsleft // 8], (int(self.x), int(self.y)))

        if self.direction[1]:
            screen.blit(moveright[self.stepsright // 8], (int(self.x), int(self.y)))

        if self.direction[2]:
            screen.blit(stand, (int(self.x), int(self.y)))

        if self.direction[3]:
            screen.blit(jump, (int(self.x), int(self.y)))


def draw():
    screen.blit(bg, (0, 0))  # show background image
    player1.drawplayer()
    pygame.display.update()


wallleft = pygame.draw.rect(screen, (0, 0, 0), (-2, 0, 2, 600), 0)
wallright = pygame.draw.rect(screen, (0, 0, 0), (1201, 0, 2, 600), 0)

player1 = Player(300, 393, 5, 96, 128, -16, [0, 0, 1, 0], 0, 0)

active = True  # set game active


# main program
while active:
    for event in pygame.event.get():  # read events
        if event.type == pygame.QUIT:
            sys.exit()  # exit program

    playerrect = pygame.Rect(int(player1.x), int(player1.y), 96, 128)

    # evaluate keyboard inputs
    pressed = pygame.key.get_pressed()

    # move left
    if pressed[pygame.K_LEFT] and not playerrect.colliderect(wallleft):
        player1.move([1, 0])
    # move right
    elif pressed[pygame.K_RIGHT] and not playerrect.colliderect(wallright):
        player1.move([0, 1])
    else:
        player1.stand()

    # jump
    if pressed[pygame.K_UP]:
        player1.setjump()
    player1.dojump()

    draw()
    clock.tick(60)  # adjust screen frequency
