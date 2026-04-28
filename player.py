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
        
        self.state = "idle"
        self.frame = 0
        self.animation_speed = 0.15
    
        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect()
        
        self.x = float(self.rect.x) #prevents choppy movement
        self.y = float(self.rect.y) #prevents choppy movement
        self.vx = 0
        self.vy = 0
        self.speed = 200
        self.jump_strength = 500
        self.gravity = 1000
        self.on_ground = True
   

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
            self.on_ground = False
            

    def move(self, delta):
       self.rect.x += self.vx * delta
       self.rect.x = int(self.x)
        
    def set_state(self):
        if not self.on_ground:
            self.state = jump
        elif self.vx == 0:
            self.state= idle
        else: 
            self.state = walk
            
            ##potentiellt lägg till dash action här
        
    
    def apply_gravity(self, delta):
        pass
            
    def animate(self):
        self.frame += self.animation_speed

        if self.frame >= len(self.animations[self.state]):
            self.frame = 0

        self.image = self.animations[self.state][int(self.frame)]
        
    
        