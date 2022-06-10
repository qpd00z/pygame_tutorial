import pygame
import sys

pygame.init()

bg = pygame.image.load("img/bg.png")
screen = pygame.display.set_mode([1200, 595])  # open program window
clock = pygame.time.Clock()  # clock
pygame.display.set_caption("MakerKids Pygame Tutorial")

# load still images for several body positions
attackleft = pygame.image.load("img/attackleft.png")
attackright = pygame.image.load("img/attackright.png")
jump = pygame.image.load("img/jump.png")

# load image sequence for left walk animation
moveleft = [pygame.image.load("img/left1.png"),
            pygame.image.load("img/left2.png"),
            pygame.image.load("img/left3.png"),
            pygame.image.load("img/left4.png"),
            pygame.image.load("img/left5.png"),
            pygame.image.load("img/left6.png"),
            pygame.image.load("img/left7.png"),
            pygame.image.load("img/left8.png")]

# load image sequence for right walk animation
moveright = [pygame.image.load("img/right1.png"),
             pygame.image.load("img/right2.png"),
             pygame.image.load("img/right3.png"),
             pygame.image.load("img/right4.png"),
             pygame.image.load("img/right5.png"),
             pygame.image.load("img/right6.png"),
             pygame.image.load("img/right7.png"),
             pygame.image.load("img/right8.png")]

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
        self.last = [1, 0]
        self.ok = True

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
            self.last = [1, 0]

        if self.direction[1]:
            screen.blit(moveright[self.stepsright // 8], (int(self.x), int(self.y)))
            self.last = [0, 1]

        if self.direction[2]:
            if self.last[0]:
                screen.blit(attackleft, (int(self.x), int(self.y)))
            else:
                screen.blit(attackright, (int(self.x), int(self.y)))

        if self.direction[3]:
            screen.blit(jump, (int(self.x), int(self.y)))


class Ball:
    def __init__(self, playerx, playery, balldirection, radius, color, speed):
        self.x = int(playerx)
        self.y = int(playery)
        if balldirection[0]:
            self.x += 5
            self.speed = -1 * speed
        elif balldirection[1]:
            self.x += 92
            self.speed = speed
        self.y += 84
        self.radius = radius
        self.color = color

    def move(self):
        self.x += self.speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius), 0)


class Zombie:
    def __init__(self, x, y, speed, width, height, direction, xmin, xmax):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.direction = direction
        self.stepsleft = 0
        self.stepsright = 0
        self.xmin = xmin
        self.xmax = xmax
        self.lifes = 6
        # load image sequence for left walk animation
        self.moveleft = [pygame.image.load("img/l1.png"),
                         pygame.image.load("img/l2.png"),
                         pygame.image.load("img/l3.png"),
                         pygame.image.load("img/l4.png"),
                         pygame.image.load("img/l5.png"),
                         pygame.image.load("img/l6.png"),
                         pygame.image.load("img/l7.png"),
                         pygame.image.load("img/l8.png")]
        # load image sequence for right walk animation
        self.moveright = [pygame.image.load("img/r1.png"),
                          pygame.image.load("img/r2.png"),
                          pygame.image.load("img/r3.png"),
                          pygame.image.load("img/r4.png"),
                          pygame.image.load("img/r5.png"),
                          pygame.image.load("img/r6.png"),
                          pygame.image.load("img/r7.png"),
                          pygame.image.load("img/r8.png")]
        # load images for life monitor
        self.empty = pygame.image.load("img/empty.png")
        self.half = pygame.image.load("img/half.png")
        self.full = pygame.image.load("img/full.png")

    def hearts(self):
        # full hearts
        if self.lifes >= 2:
            screen.blit(self.full, (507, 15))
        if self.lifes >= 4:
            screen.blit(self.full, (569, 15))
        if self.lifes == 6:
            screen.blit(self.full, (631, 15))

        # half hearts
        if self.lifes == 1:
            screen.blit(self.half, (507, 15))
        elif self.lifes == 3:
            screen.blit(self.half, (569, 15))
        elif self.lifes == 5:
            screen.blit(self.half, (631, 15))

        # empty hearts
        if self.lifes <= 0:
            screen.blit(self.empty, (507, 15))
        if self.lifes <= 2:
            screen.blit(self.empty, (569, 15))
        if self.lifes <= 4:
            screen.blit(self.empty, (631, 15))

    def drawzombie(self):
        if self.stepsleft == 63:
            self.stepsleft = 0
        if self.stepsright == 63:
            self.stepsright = 0

        if self.direction[0]:
            screen.blit(self.moveleft[self.stepsleft//8], (int(self.x), int(self.y)))
        if self.direction[1]:
            screen.blit(self.moveright[self.stepsright//8], (int(self.x), int(self.y)))

    def move(self):
        self.x += int(self.speed)
        # move left
        if self.speed < 0:
            self.direction = [1, 0]
            self.stepsleft += 1
        # move right
        if self.speed > 0:
            self.direction = [0, 1]
            self.stepsright += 1

    def changedirection(self):
        if self.x > self.xmax:
            self.speed *= -1
        elif self.x < self.xmin:
            self.speed *= -1
        self.move()


def draw():
    screen.blit(bg, (0, 0))  # show background image
    for b in balls:
        b.draw()
    player1.drawplayer()
    zombie1.drawzombie()
    zombie1.hearts()
    pygame.display.update()


def ballhandler():
    global balls
    for b in balls:
        if 0 <= b.x <= 1200:  # if b.x >= 0 and b.x <= 1200:
            b.move()
        else:
            balls.remove(b)


def collision():
    global balls
    zombierect = pygame.Rect(int(zombie1.x) + 18, int(zombie1.y) + 24, zombie1.width - 36, zombie1.height - 24)

    for b in balls:
        ballrect = pygame.Rect(int(b.x) - b.radius, int(b.y) - b.radius, b.radius * 2, b.radius * 2)
        if zombierect.colliderect(ballrect):
            balls.remove(b)
            zombie1.lifes -= 1


wallleft = pygame.draw.rect(screen, (0, 0, 0), (-2, 0, 2, 600), 0)
wallright = pygame.draw.rect(screen, (0, 0, 0), (1201, 0, 2, 600), 0)

player1 = Player(300, 393, 5, 96, 128, -16, [0, 0, 1, 0], 0, 0)
zombie1 = Zombie(600, 393, 4, 96, 128, [0, 0], 40, 1090)

balls = []
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

    if pressed[pygame.K_SPACE]:
        if len(balls) <= 4 and player1.ok:
            balls.append(Ball(int(player1.x), int(player1.y), player1.last, 8, (0, 0, 0), 7))
        player1.ok = False

    if not pressed[pygame.K_SPACE]:
        player1.ok = True

    ballhandler()
    zombie1.changedirection()

    collision()
    draw()
    clock.tick(60)  # adjust screen frequency
