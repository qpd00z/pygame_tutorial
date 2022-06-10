import pygame
import sys

pygame.init()
screen = pygame.display.set_mode([800, 600])  # open program window
clock = pygame.time.Clock()  # clock

x = 400  # position pointer x
y = 300  # position pointer y
speed = 3  # pixels per move
width = 40
height = 80

active = True  # set game active
# main program
while active:
    for event in pygame.event.get():  # read events
        if event.type == pygame.QUIT:
            sys.exit()  # exit program

    # evaluate keyboard inputs
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        y -= speed
    if pressed[pygame.K_RIGHT]:
        x += speed
    if pressed[pygame.K_DOWN]:
        y += speed
    if pressed[pygame.K_LEFT]:
        x -= speed

    screen.fill((0, 0, 0))  # clear screen (uncomment for painting on screen)
    pygame.draw.rect(screen, (255, 255, 0), (x, y, width, height))
    pygame.display.update()
    clock.tick(60)  # adjust screen frequency
