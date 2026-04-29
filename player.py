"""
Player: handle tanget input, player data, player movement, player animation
"""

import pygame
import spritesheet
import os


class Player(pygame.sprite.Sprite): 
    
    """
    Representerar spelaren.

    Klassen hanterar spelarens rörelse, gravitation, hopp,
    markkollision och animationer baserat på spelarens state.
    """
    def __init__(self):
        
        """ 
        Initierar spelaren och laddar in animationer för olika states.
        """
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
        ##lol hur kom det dit ?? där uppe. skrev du frances?

        self.rect   = self.image.get_rect()
        self.rect.x = 450
        self.rect.bottom = 400 #inte ramla genom golvet

        self.x = float(self.rect.x) #prevents choppy movement
        self.y = float(self.rect.y) #prevents choppy movement
        
        self.vx = 0
        self.vy = 0
        
        self.speed          = 200
        self.jump_strength  = 700
        self.gravity        = 2000
        self.on_ground      = True
   
        """
         Uppdaterar spelarens rörelse och gravitation. animerar spelaren.
         
         Parametrar:
        keys (Sequence[bool]): Tangentstatus från pygame.
        delta (float): Tid sedan föregående frame.
        ground (int | float): Y-position för marknivå.
        """
   
    def update(self, keys, delta, ground): ##kanske lägg typ "levels", "ground", "platforms". alltså ett sätt för spelaren att se om den är på marken eller inte
        self.handle_input(keys)
        self.apply_gravity(delta)
        self.move(delta, ground)
        self.set_state()
        self.animate(delta)
        
        """
        Tolkar key input och uppdaterar spelarens horisontella
        hastighet samt initierar hopp.
        
        parametrar:
        keys (Sequence[bool]): Tangentstatus från pygame.
        """
        
        
    def handle_input(self, keys):
        self.vx = 0

        if keys[pygame.K_a]: self.vx = -self.speed
        if keys[pygame.K_d]: self.vx = self.speed 
        if keys[pygame.K_a] and keys[pygame.K_d]: self.vx = 0 
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vy = -self.jump_strength
            self.on_ground = False
            

    """
    Flyttar spelaren baserat på hastighet och tid, samt hanterar
    kollision med marknivån.
    
    paratemetrar:
        delta (float): Tid sedan föregående frame.
        ground (int | float): Y-position för marknivå. BEHÖVER LÄGGAS TILL I GAME.PY
     """   
    def move(self, delta, ground):
       self.x += self.vx * delta
       self.rect.x = int(self.x)
       self.y += self.vy * delta
       self.rect.y = int(self.y)
       
       if self.rect.bottom >= ground: 
           self.rect.bottom = ground
           self.y = float(self.rect.y)
           self.vy = 0
           self.on_ground = True
       else:
           self.on_ground = False
        
    """
    Bestämmer spelarens nuvarande state (idle, walk, jump)
    baserat på rörelse och om spelaren är på marken.
    """
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
    
    """
    Sätter gravitation på spelarens vertikala hastighet
   
    parameter:
    delta (float): Tid sedan föregående frame.
    """
    def apply_gravity(self, delta):
        self.vy += self.gravity * delta
        ##behöver input från game.py så spelare kan interagera med marken.
            
    """
    Updaterar animation baserat på spelarens state och animationshastighet
    
    parameter:
    delta (float): Tid sedan föregående frame.
    """
    def animate(self, delta):
        self.frame += self.animation_speed * delta

        if self.frame >= len(self.animations[self.state]):
            self.frame = 0

        self.image = self.animations[self.state][int(self.frame)]
        
    
        