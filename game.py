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
display = pygame.Surface((W, H))
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
        if self.moving_right and not self.collision_types["right"]:
            self.player_movement[0] = min(self.player_movement[0] + 2, 2)
        elif self.moving_left and not self.collision_types["left"]:
            self.player_movement[0] = max(self.player_movement[0] - 2, -2)
        else:
            self.player_movement[0] = 0
        
        self.air_timer += 1
        if self.air_timer != 0 or not self.collision_types["bottom"] :
            self.player_movement[1] += 0.2
            if self.player_movement[1] > 5:
                self.player_movement[1] = 5  
        
        if self.collision_types['bottom'] and not self.jumping:
            self.air_timer = 0
            self.player_movement[1] = 0
        elif self.jumping and self.collision_types['bottom']:
            self.player_movement[1] = -8
            self.collision_types["bottom"] = False
            
    def collisions(self,rect,tiles):
        self.collision_types = {'top':False,'bottom':False,'right':False,'left':False}
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
        return rect

    def draw(self):
        self.player_rect = pygame.Rect(self.x,self.y,self.width,self.height)
        return self.player_rect

# MAIN ------------------------------------------------------------
player_one = player(0,100,21,24)
player_rect = player_one.draw()
floor = pygame.Rect(0,200,100,50)
floor2 = pygame.Rect(500,200,100,50)
layer = pygame.Rect(0,300,600,400)
#game loop
while True:
    display.fill((146,244,255))
    
    pygame.draw.rect(display,(0,0,0),player_rect)
    pygame.draw.rect(display,(105,200,106),floor)
    pygame.draw.rect(display,(105,200,106),floor2)
    pygame.draw.rect(display,(135,90,86),layer)
    pygame.display.flip()

    player_rect = player_one.collisions(player_rect, [floor, floor2, layer])
    player_one.move()

    for event in pygame.event.get(): 
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        player_one.keys()
    
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()

    clock.tick(60)

