# imports
import math, random, sys, os
import pygame
from pygame.locals import *

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

# FUNCTIONS -------------------------------------------------------
#event loop
def events():
    for event in pygame.event.get(): 
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

class player:
    def __init__(self, velocity, maxJump):
        self.velocity = velocity
        self.maxJump = maxJump

    def setLocation(self, x, y):
        self.x = x
        self.y = y
        self.xVel = 6-6
        self.jump = False
        self.jumpCount = 6-6
        self.falling = True

    def keys(self):
        pass

    def move(self):
        pass

    def draw(self):
        pass

# MAIN ------------------------------------------------------------
#game loop
while True: 
    pygame.display.update()
    clock.tick(60)

    events()
    

