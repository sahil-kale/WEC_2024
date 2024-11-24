import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((400, 300))
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_w:
                print("W pressed")
            elif event.key == K_a:
                print("A pressed")
            elif event.key == K_s:
                print("S pressed")
            elif event.key == K_d:
                print("D pressed")

pygame.quit()
