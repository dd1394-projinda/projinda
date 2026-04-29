# -----------------
# Field: Creates platforms and enemy blocks
# -----------------

import pygame
pygame.init()


WORLD_END = 200     # 10_000 pixel world
WORLD_BEGIN = 0
TILE = 50
CORNER = 10

class Field(): 
    def __init__(self):
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
        a = 4
        self.add_platform(WORLD_BEGIN,  a,              400,    100)
        self.add_platform(a+2,            WORLD_END,    400,    100)

        # Fall
        self.add_enemy((WORLD_BEGIN - CORNER) * TILE,     500,   (WORLD_END + CORNER) * TILE,    500)

        # World borders
        self.add_platform(WORLD_BEGIN - CORNER,     WORLD_BEGIN,        50,   500)
        self.add_platform(WORLD_END,                WORLD_END + CORNER,    50,   500)
        
        # Platforms
        self.add_platform(0,    2,      350,    50)
        self.add_platform(0,    1,      300,    50)
        
        # Enemies
        self.add_enemy(400,     365,    35,     35)


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
            self.platforms.append(pygame.Rect(x*50, y, 50, h))


    # -----------------
    # BLOCK CONTACT
    # -----------------
    def is_solid(self, rect):
        return any(rect.colliderect(p) for p in self.platforms)
    
    def is_enemy(self,rect):
        return any(rect.colliderect(e) for e in self.enemies)