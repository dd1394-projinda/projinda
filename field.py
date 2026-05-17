# -----------------
# Field: Creates platforms and enemy blocks
# -----------------

import pygame
import random

class Field(): 
    def __init__(self,world_width, world_height, tile):
        self.world_width    = world_width
        self.world_height   = world_height
        self.TILE           = tile
        
        self.ENEMY_SIZE     = 40
        self.GROUND         = 500
        self.FALL_GROUND    = self.GROUND + 100
        self.world_begin    = 0                    #flyttade world begin och end in i klassen eftersom de ska bli beroende av game
        self.world_end      = world_width // self.TILE
        self.middle_block   = self.world_end // 2

        self.platforms      = []
        self.enemies        = []
        
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


        # Left goal platform
        self.add_platform(self.world_begin, self.world_begin + 1, 400,100)

        # Possible heights
        heights     = [450, 400, 350, 300]  
        current_y   = heights[0]            # Initilize y

        # Probability factors
        min_chance          = 0.1
        max_chance          = 0.2  
        hole_persistence    = 0.7

        # Hole factors
        max_hole_tiles      = 2         # At most 2 in a row, 3 makes an impossible jump
        safe_blocks_left    = 0         
        hole_tiles_in_row   = 0
    

        # -----------------
        # RANDOMIZATION LOGIC
        # ----------------- 
        for block in range(self.world_begin+1, self.world_end-1):
            distance_factor = abs(block - self.middle_block) / self.middle_block        # Distance from middle position
            hole_chance = min_chance + (distance_factor * (max_chance - min_chance))    # Hole chance depedant on distance from middle, increases as the edges get closer
            
            is_middle = (block == self.middle_block)    # Check if block is the middle block

            if is_middle or safe_blocks_left > 0:       # If middle or if there are "must be" blocks left, aka blocks after a hole
                safe_blocks_left = max(0, safe_blocks_left - 1)     # Safe blocks is decreased unless already 0
                if is_middle:
                    hole_tiles_in_row = 0   # Reset hole counter
                    safe_blocks_left = 2    # Garantee solid ground
                is_hole = False             # Force solid
            else:
                chance = hole_persistence if hole_tiles_in_row > 0 else hole_chance     # Use persistence chance if already in a hole, else distance based chance
                is_hole = random.random() < chance          # Random for chance, true = hole

            if is_hole:
                hole_tiles_in_row += 1      # Track consecutive holes
                if hole_tiles_in_row >= max_hole_tiles:
                    safe_blocks_left = 2    # Max hole size reached, start safe zone
                self.add_platform(block, block + 1, self.FALL_GROUND + 50, 10)      # Add ghost block, for 1:1 enemy spawn logic
            else:
                hole_tiles_in_row = 0       # Reset hole counter on solid block
                possible_heights = [h for h in heights if abs(h - current_y) <= 100]        # Random between these possible heights, only allow 100 pixel change
                current_y = random.choice(possible_heights)
                self.add_platform(block, block + 1, current_y, self.world_height - current_y)
            

        # Right goal platform
        self.add_platform(self.world_end - 1, self.world_end, 400,100)      # Needs to be added last, for 1:1 enemy spawn logic


        # -----------------
        # RANDOMIZE ENEMIES
        # -----------------
        probability         = 0.5
        min_enemy_spacing   = 3         # Min distance between enemies
        enemy_cooldown      = 0

        for i in range(1, len(self.platforms) - 3):
            p_left  = self.platforms[i].top         # Look at three consecutive tiles
            p       = self.platforms[i+1].top
            p_right = self.platforms[i+2].top

            if enemy_cooldown > 0:
                enemy_cooldown -= 1
                continue

            in_middle = (self.middle_block - 1 <= i + 1 <= self.middle_block + 2)   # Checks if current enemy block is within a small range to the middle block (char spawn position)

            if max(p_left, p, p_right) < self.GROUND and not in_middle:             # If there is ground and current is not the middle
                if random.random() < probability:               # Random for chance
                    enemy_x = (i+1)*self.TILE + ((self.TILE - self.ENEMY_SIZE) // 2)    # Enemy, top-left x position
                    enemy_y = p - self.ENEMY_SIZE                                       # y-position
                    self.add_enemy(enemy_x, enemy_y, self.ENEMY_SIZE, self.ENEMY_SIZE)  # Add enemy

                    enemy_cooldown = min_enemy_spacing      # When enemy added, create cooldown until next

        # Fall
        self.add_enemy(self.world_begin * self.TILE, self.FALL_GROUND, self.world_end * self.TILE, 100)     # So char dies when falling


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
      

    # -----------------
    # BLOCK CONTACT
    # -----------------
    def is_solid(self, rect):
        return any(rect.colliderect(p) for p in self.platforms)
    
    def is_enemy(self,rect):
        return any(rect.colliderect(e) for e in self.enemies)