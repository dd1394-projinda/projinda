# -----------------
# Field: Creates platforms and enemy blocks
# -----------------

import pygame
import random

TILE = 100
CORNER = 5

class Field(): 
    def __init__(self,world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height
        
        self.world_begin = 0                    #flyttade world begin och end in i klassen eftersom de ska bli beroende av game
        self.world_end = world_width // TILE

        self.platforms = []
        self.enemies = []
        self.build_world()


    # -----------------
    # BUILD 
    # -----------------
    def build_world(self):
        # -----------------
        # Build world block by block, organize block from left to right
        # -----------------
        
        # Ground
        """"a = 4
        self.add_platform(self.world_begin,  a,              400,    100)
        self.add_platform(a+2,            self.world_end,    400,    100)""" #jag bara testar lite grejer
        
        
        heights = [400, 350, 300, 250]  
        hole_chance = 0.08      

        previous_y = 400
        max_hole_tiles = 2
        hole_tiles_in_row = 0
        for block in range(self.world_begin, self.world_end):
            if hole_tiles_in_row < max_hole_tiles and random.random() < hole_chance:
                y = 500
                hole_tiles_in_row += 1
            else:
                y = random.choice(heights)
                hole_tiles_in_row = 0
                    
            self.add_platform(block, block + 1, y, self.world_height - y)
            #self.platforms.append(pygame.Rect(block * TILE, y, TILE, self.world_height - y)) ##needs some work
        

        # Fall
        self.add_enemy((self.world_begin - CORNER) * TILE, 500, (self.world_end + CORNER) * TILE, 500)
        # World borders
        self.add_platform(self.world_begin - CORNER,     self.world_begin,        50,   500)
        self.add_platform(self.world_end,                self.world_end + CORNER,    50,   500)
        
        # Goal platforms
        self.add_platform(self.world_begin, 2, 400,100)
        self.add_platform(self.world_end - 2, self.world_end, 400,100)

        
        # Platforms
        self.add_platform(0,    2,      350,    50)
        self.add_platform(0,    1,      300,    50)
        
        # Enemies
        self.add_enemy_on_platform(random.randint(4, 12))


    # ----------------- 
    # ENEMY BLOCK
    # -----------------
    def add_enemy(self, x, y, w, h):
        # -----------------
        # x,y top left, w how much right, h how much down
        # -----------------
        self.enemies.append(pygame.Rect(x, y, w, h))


    # -----------------
    # PLATFORM
    # -----------------
    def add_platform(self, x_start, x_end, y, h):
        # -----------------
        # Block wise, so each block is 50x50
        # -----------------
        for x in range(x_start, x_end):
            self.platforms.append(pygame.Rect(x*TILE, y, TILE, h))

    def add_enemy_on_platform(self, block, w = 35, h = 35):
         x = block * TILE + (TILE - w) // 2
         
         for p in self.platforms:
             if p.left <= x < p.right:
                y = p.top - h
                enemy = pygame.Rect(x, y, w, h)

                if not self.is_solid(enemy):
                    self.enemies.append(enemy)
                return
            

    # -----------------
    # BLOCK CONTACT
    # -----------------
    def is_solid(self, rect):
        return any(rect.colliderect(p) for p in self.platforms)
    
    def is_enemy(self,rect):
        return any(rect.colliderect(e) for e in self.enemies)