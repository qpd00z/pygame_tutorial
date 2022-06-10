import pygame
import sys

pygame.init()
bg = pygame.image.load("img/bg.png")
screen = pygame.display.set_mode([1200, 595])  # open program window
clock = pygame.time.Clock()  # clock
pygame.display.set_caption("MakerKids Pygame Tutorial")


def draw():
    screen.blit(bg, (0, 0))  # show background image
    pygame.draw.rect(screen, (0, 0, 255), (int(x), int(y), width, height))
    pygame.display.update()


x = 400  # position pointer x
y = 440  # position pointer y
speed = 5  # pixels per move
width = 40
height = 80

leftWall = pygame.draw.rect(screen, (0, 0, 0), (-2, 0, 2, 600), 0)
rightWall = pygame.draw.rect(screen, (0, 0, 0), (1201, 0, 2, 600), 0)

active = True  # set game active
jumpvar = -16

# main program
while active:
    for event in pygame.event.get():  # read events
        if event.type == pygame.QUIT:
            sys.exit()  # exit program

    playerRect = pygame.Rect(int(x), int(y), 40, 80)

    # evaluate keyboard inputs
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP] and jumpvar == -16:
        jumpvar = 15
    if pressed[pygame.K_RIGHT] and not playerRect.colliderect(rightWall):
        x += speed
    if pressed[pygame.K_LEFT] and not playerRect.colliderect(leftWall):
        x -= speed

    if jumpvar >= -15:
        n = 1
        if jumpvar < 0:
            n = -1

        y -= (jumpvar**2) * 0.17 * n
        jumpvar -= 1

    draw()
    clock.tick(60)  # adjust screen frequency
