"""
Player: handle tanget input, player data, player movement, player animation
"""

import pygame
import spritesheet
import os


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        BASE_DIR = os.path.dirname(__file__)
        ss_walk = spritesheet.spritesheet(os.path.join(BASE_DIR, "images", "walk.png"))
        ss_idle = spritesheet.spritesheet(os.path.join(BASE_DIR, "images", "idle.png"))
        ss_jump = spritesheet.spritesheet(os.path.join(BASE_DIR, "images", "jump.png"))
        ss_run = spritesheet.spritesheet(os.path.join(BASE_DIR, "images", "run.png"))

        self.animations = {
            "walk": ss_walk.load_strip((0, 0, 128, 128), 8),
            "idle": ss_idle.load_strip((0, 0, 128, 128), 8),
            "jump": ss_jump.load_strip((0, 0, 128, 128), 13),
            "run":  ss_run.load_strip((0, 0, 128, 128), 7),
        }
        
        self.state              = "idle"
        self.frame              = 0
        self.animation_speed    = 0.15
        self.image              = self.animations[self.state][0]
               

        """
            ### TEMPORARY ###
        self.image = pygame.Surface((50,50))
        self.image.fill((200, 170, 230))
            ### TEMPORARY ###
        """

        self.rect   = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 475

        self.x = float(self.rect.x) #prevents choppy movement
        self.y = float(self.rect.y) #prevents choppy movement
        
        self.vx = 0
        self.vy = 0
        
        self.speed          = 200
        self.jump_strength  = 700
        self.gravity        = 2000
        self.on_ground      = True
   

    def update(self, keys, delta, ground): ##kanske lägg typ "levels", "ground", "platforms". alltså ett sätt för spelaren att se om den är på marken eller inte
        self.handle_input(keys)
        self.apply_gravity(delta)
        self.move(delta, ground)

        
        self.set_state()
        self.animate()
        
        
        
    def handle_input(self, keys):
        self.vx = 0

        if keys[pygame.K_a]: self.vx = -self.speed
        if keys[pygame.K_d]: self.vx = self.speed 
        if keys[pygame.K_a] and keys[pygame.K_d]: self.vx = 0 
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vy = -self.jump_strength
            self.on_ground = False
            

    def move(self, delta, ground):
       self.x += self.vx * delta
       self.rect.x = int(self.x)
       self.y += self.vy * delta
       self.rect.y = int(self.y)
       
       if self.rect.bottom >= ground: 
           self.rect.bottom = ground
           self.y = self.rect.y
           self.vy = 0
           self.on_ground = True
       else:
           self.on_ground = False

    def apply_gravity(self, delta):
        self.vy += self.gravity * delta



    def set_state(self):
        if not self.on_ground:
            new_state = "jump"
        elif self.vx == 0:
            new_state= "idle"
        else: 
            new_state = "walk"
            
            ##potentiellt lägg till dash action här
            
        if new_state != self.state:
            self.state = new_state
            self.frame = 0
            

    def animate(self):
        self.frame += self.animation_speed

        if self.frame >= len(self.animations[self.state]):
            self.frame = 0

        self.image = self.animations[self.state][int(self.frame)]
        
    
        