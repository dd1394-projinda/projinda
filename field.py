# -----------------
# Field: Creates platforms and enemy blocks
# -----------------

import pygame
pygame.init()


class Field(): 
    def __init__(self):
        self.WIDTH = 20
        self.platforms = []
        self.enemies = []
        self.build_world()


    # -----------------
    # BUILD 
    # -----------------
    def build_world(self):
        self.add_platform(0,self.WIDTH,400,500)
        self.add_platform(2,3,350,400)
        self.add_enemy(300,365,35,35)


    # ----------------- 
    # ENEMY BLOCK
    # -----------------
    def add_enemy(self, x, y, w, h):
        self.enemies.append(pygame.Rect(x, y, w, h))


    # -----------------
    # PLATFORM
    # -----------------
    def add_platform(self, x_start, x_end, y, h):
        for x in range(x_start, x_end):
            self.platforms.append(pygame.Rect(x*50, y, 50, h))


    # -----------------
    # BLOCK CONTACT
    # -----------------
    def is_solid(self, rect):
        return any(rect.colliderect(p) for p in self.platforms)
    
    def is_enemy(self,rect):
        return any(rect.colliderect(e) for e in self.enemies)