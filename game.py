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

#collision checker
def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

# CLASSES -------------------------------------------------------
class player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.player_movement = [0,0]
        self.moving_left = False
        self.moving_right = False
        self.air_timer = 0
        self.vertical_momentum = 0
        self.jumping = False
        self.collision_types = {'top':False,'bottom':False,'right':False,'left':False}

    def keys(self):
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                self.moving_right = True
            if event.key == K_LEFT:
                self.moving_left = True
            if event.key == K_UP or event.key == K_SPACE:
                self.jumping = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                self.moving_right = False
            if event.key == K_LEFT:
                self.moving_left = False
            if event.key == K_UP or event.key == K_SPACE:
                self.jumping = False

    def move(self):
        if self.moving_right == True and self.collision_types.right == False:
            self.player_movement[0] += 2
        if self.moving_left == True and self.collision_types.left == False:
            self.player_movement[0] -= 2
        if self.collision_types['bottom'] == True:
            self.air_timer = 0
            self.vertical_momentum = 0
        else:
            self.air_timer += 1
    
    def collisions(self,rect,tiles):
        rect.x += self.player_movement[0]
        hit_list = collision_test(rect,tiles)
        for tile in hit_list:
            if self.player_movement[0] > 0:
                rect.right = tile.left
                self.collision_types['right'] = True
            elif self.player_movement[0] < 0:
                rect.left = tile.right
                self.collision_types['left'] = True
        rect.y += self.player_movement[1]
        hit_list = collision_test(rect,tiles)
        for tile in hit_list:
            if self.player_movement[1] > 0:
                rect.bottom = tile.top
                self.collision_types['bottom'] = True
            elif self.player_movement[1] < 0:
                rect.top = tile.bottom
                self.collision_types['top'] = True
        return rect, self.collision_types

    def draw(self):
        self.player_rect = pygame.Rect(self.x,self.y,self.width,self.height)

# MAIN ------------------------------------------------------------
#game loop
while True: 
    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get(): 
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    

