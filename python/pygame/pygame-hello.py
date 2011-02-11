import pygame
from pygame.locals import *
from sys import exit

pygame.init()

SCR_SIZE = (200, 200)

screen = pygame.display.set_mode(SCR_SIZE, 0, 32)

pygame.display.set_caption('Hola Mundo!')

font = pygame.font.SysFont('Arial', 22, bold=True)

font_height = font.get_linesize()

while True:
    for event in pygame.event.get():
        screen.fill((0, 0, 0))
        y = SCR_SIZE[1]/2
        x = SCR_SIZE[0]/2-50
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_h:
                screen.blit(font.render('Hola mundo!', False, (0, 255, 0)), (x, y))

    pygame.display.update()

