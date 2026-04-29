#
# field
#

import pygame
pygame.init()


class Field(): 
    def __init__(self):
        self.WIDTH = 20
        self.blocks = [[] for _ in range(self.WIDTH)]
        self.platforms = []
        self.build_world()

    def build_world(self):
        self.add_platform(0,self.WIDTH,400,500)
        self.add_platform(2,3,350,400)

    def add_platform(self, x_start, x_end, y_start, y_end):
        for x in range(x_start, x_end):
            self.platforms.append(pygame.Rect(x*50, y_start, 50, y_end)
            )
            self.blocks[x].append((y_start,y_end))

    def is_solid(self, rect):
        return any(rect.colliderect(p) for p in self.platforms)
    

    def is_solid2(self, x, y):
        x = int(x // 50)
        y = int(y // 50)

        if x < 0 or x >= self.WIDTH:
            return False
        
        for y1, y2 in self.blocks[x]:
            if y1 // 50 <= y <= y2 // 50:
                return True

        return False