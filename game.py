# imports
import math, random, sys, os
import pygame
from pygame.locals import *

#event loop
def events():
    for event in pygame.event.get(): 
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

#define display surface
W, H = 600, 400
HW, HH = W/2, H/2
WINDOW_SIZE = (W, H)

#display initiation
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_SIZE) 
##display = pygame.Surface((HW, HH))
pygame.display.set_caption('RL Pygame Platform Game')

#game loop
while True: 
    pygame.display.update()
    clock.tick(60)

    events()
    

