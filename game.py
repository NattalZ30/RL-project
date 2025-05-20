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
pygame.font.init()
font = pygame.font.SysFont("Univers", 20)
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

class Coin:
    def __init__(self, x, y, width, height, colour=(210,200,10)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour 
        self.collide = False
        self.coin_rect = pygame.Rect(self.x,self.y,self.width,self.height)
        
    def player_collect(self, players, tiles):
        for player in players:
            if self.coin_rect.colliderect(player.player_rect):
                player.score += 1
                self.collide = True
        for tile in tiles:
            if self.coin_rect.colliderect(tile):
                self.collide = True

    
    def draw(self):
        pygame.draw.rect(display,self.colour,self.coin_rect)

class player:
    def __init__(self, x, y, width, height, colour=(0,0,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.score = 0
        self.player_rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.player_movement = [0,0]
        self.moving_left = False
        self.moving_right = False
        self.air_timer = 0
        self.jumping = False
        self.collision_types = {'top':False,'bottom':False,'right':False,'left':False}

    def keys(self, right, left, up):
        if event.type == KEYDOWN:
            if event.key == right:
                self.moving_right = True
            if event.key == left:
                self.moving_left = True
            if event.key == up:
                self.jumping = True
                
        if event.type == KEYUP:
            if event.key == right:
                self.moving_right = False
            if event.key == left:
                self.moving_left = False
            if event.key == up:
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

    def draw(self):
        pygame.draw.rect(display,self.colour,self.player_rect)

# MAIN ------------------------------------------------------------
player_one = player(0,100,21,24)

#player_two = player(580,100,21,24,(100,100,100))

player_list = [player_one]#, player_two]

coin = Coin(300,250,20,23)

floor = pygame.Rect(0,200,100,50)
layer2 = pygame.Rect(0,220,100,30)
layer3 = pygame.Rect(500,220,100,30)
floor2 = pygame.Rect(500,200,100,50)
layer = pygame.Rect(0,300,600,400)
grass = pygame.Rect(0,300,600,30)
#game loop

def draw_score(score):
    text = font.render(f"Score: {score}", True, (0,0,0))
    display.blit(text,(10,10))

while True:
    display.fill((146,244,255))
    
    player_one.draw()
    #player_two.draw()

    ## drawing the tiles
    pygame.draw.rect(display,(135,90,86),layer)
    pygame.draw.rect(display,(105,200,106),grass)
    
    pygame.draw.rect(display,(105,200,106),floor)
    pygame.draw.rect(display,(135,90,86),layer2)
    
    pygame.draw.rect(display,(105,200,106),floor2)
    pygame.draw.rect(display,(135,90,86),layer3)

    coin.draw()
    coin.player_collect(player_list,[grass,floor,floor2,layer,layer2,layer3])
    if coin.collide:
        new_coin = None
        while True:
            new_coin = Coin(random.randint(20, 580), random.randint(100, 277), 20, 23)
            new_coin.player_collect(player_list, [grass, floor, floor2, layer, layer2, layer3])
            if not new_coin.collide:
                break
        coin = new_coin
        coin.draw()

    draw_score(player_one.score)    

    pygame.display.flip()

    for players in player_list:
        players.collisions(players.player_rect, [floor, floor2, layer])
        players.move()
    # player_one.collisions(player_one.player_rect, [floor, floor2, layer])
    # player_one.move()

    # player_two.collisions(player_two.player_rect, [floor, floor2, layer])
    # player_two.move()

    for event in pygame.event.get(): 
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        player_one.keys(K_d,K_a,K_w) 
        #player_two.keys(K_RIGHT,K_LEFT,K_UP)
    
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()

    clock.tick(60)

