# -----------------
# Field: Creates platforms and enemy blocks
# -----------------

import pygame
import random

class Field(): 
    def __init__(self,world_width, world_height, tile):
        self.world_width = world_width
        self.world_height = world_height
        self.TILE = tile
        
        self.world_begin = 0                    #flyttade world begin och end in i klassen eftersom de ska bli beroende av game
        self.world_end = world_width // self.TILE

        self.platforms = []
        self.enemies = []
        self.build_world()


    # -----------------
    # RESET
    # -----------------
    def reset_world(self):
        self.platforms.clear()
        self.enemies.clear()
        self.build_world()

    # -----------------
    # BUILD 
    # -----------------
    def build_world(self):
        # -----------------
        # Build world block by block, organize block from left to right
        # -----------------

  
        heights = [450, 400, 350, 300]  
        current_y = heights[0]

        min_chance = 0.1
        max_chance = 0.2  
        hole_persistence = 0.7

        max_hole_tiles = 2
        safe_blocks_left = 0
        hole_tiles_in_row = 0

        middle_block = self.world_end // 2

        # -----------------
        # RANDOMIZATION LOGIC
        # ----------------- 
        for block in range(self.world_begin+1, self.world_end-1):
            distance_factor = abs(block - middle_block) / middle_block
            current_hole_chance = min_chance + (distance_factor * (max_chance - min_chance))
            
            if safe_blocks_left > 0:
                is_forced_solid = True
                safe_blocks_left -= 1
            else:
                is_forced_solid = False

            if block == middle_block:
                possible_heights = [h for h in heights if abs(h - current_y) <= 100]
                current_y = random.choice(possible_heights)
                draw_y = current_y
                hole_tiles_in_row = 0
                safe_blocks_left = 2
            
            is_already_in_hole = (hole_tiles_in_row > 0 and hole_tiles_in_row < max_hole_tiles)
            chance_to_be_hole = hole_persistence if is_already_in_hole else current_hole_chance
            
            if not is_forced_solid and random.random() < chance_to_be_hole and block != middle_block:
                draw_y = 600
                hole_tiles_in_row += 1

                if hole_tiles_in_row >= max_hole_tiles:
                    safe_blocks_left = 2

            else:
                possible_heights = [h for h in heights if abs(h - current_y) <= 100]
                current_y = random.choice(possible_heights)
                draw_y = current_y
                hole_tiles_in_row = 0
                    
            self.add_platform(block, block + 1, draw_y, self.world_height - draw_y)
        

        # Fall
        self.add_enemy(self.world_begin * self.TILE, 550, self.world_end * self.TILE, 650)

        # Goal platforms
        self.add_platform(self.world_begin, 2, 400,100)
        self.add_platform(self.world_end - 2, self.world_end, 400,100)

        """
        # Enemies
        self.add_enemy_on_platform(random.randint(4, 12))
        """


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
            self.platforms.append(pygame.Rect(x*self.TILE, y, self.TILE, h))

    def add_enemy_on_platform(self, block, w = 35, h = 35):
        x = block * self.TILE + (self.TILE - w) // 2
        
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