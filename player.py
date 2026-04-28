import pygame
import spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        ss_walk = spritesheet.spritesheet("images/walk.png") 
        ss_idle = spritesheet.spritesheet("images/idle.png")
        ss_jump = spritesheet.spritesheet("images/jump.png")
        ss_run  = spritesheet.spritesheet("images/run.png")

        self.animations = {
            "walk": ss_walk.load_strip((0, 0, 128, 128), 8),
            "idle": ss_idle.load_strip((0, 0, 128, 128), 8),
            "jump": ss_jump.load_strip((0, 0, 128, 128), 13),
            "run":  ss_run.load_strip((0, 0, 128, 128), 7),
        }
    
        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect()
        
        self.vx
        self.vy
        self.speed
        self.jump_strength
        self.gravity
        self.on_ground
        self.state = "idle"
        self.frame = 0
        self.animation_speed = 0.15

    def update(self, keys, delta):
        self.handle_input(keys)
        self.gravity(delta)
        self.move(delta)
        self.set_state()
        self.animate()
        
        
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        self.vx = 0
        
        if keys[pygame.K_LEFT]: # kan ändra till K_a
            self.vx = -self.speed

        if keys[pygame.K_RIGHT]: # kan ändra till K_d
            self.vx = self.speed
            
        if keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]:
            self.vx = 0
            
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vy = -self.jump_strength
            self.on_ground = false
            

        def move(self, delta):
            
           
        def set_state(self):
            
        
        def gravity(self, delta):
            
                
            
        def animate(self):
            self.frame += self.animation_speed

            if self.frame >= len(self.animations[self.state]):
                self.frame = 0

            self.image = self.animations[self.state][int(self.frame)]
            
     
        