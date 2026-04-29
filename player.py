"""
Player: handle tanget input, player data, player movement, player animation
"""

import pygame
import spritesheet
import os
import random


class Player(pygame.sprite.Sprite): 
    
    """
    Representerar spelaren.

    Klassen hanterar spelarens rörelse, gravitation, hopp,
    markkollision och animationer baserat på spelarens state.
    """
    def __init__(self):
        
        """ 
        Initierar spelaren och laddar in animationer för olika states.
        
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
        self.animation_speed    = 12
        self.image              = self.animations[self.state][0]
        """
            
            ### TEMPORARY
        self.image = pygame.Surface((50,50))
        self.image.fill((200,170,230))


        self.rect               = self.image.get_rect()
        self.rect.x             = 450
        self.rect.bottom        = 400 

        self.x      = float(self.rect.x) #prevents choppy movement
        self.y      = float(self.rect.y) #prevents choppy movement
        
        self.vx     = 0
        self.vy     = 0
        
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

    
    # --------------
    # Reset methods
    # --------------

    def reset_after_death(self):
        self.x = 475
        self.reset()

    def reset_after_win(self):
        self.x = random.randint(250,500)
        self.reset()
    
    def reset(self):
        self.y = 350
        self.vx = 0
        self.vy = 0
        self.on_ground = True
        #self.state = "idle"
        #self.frame = 0

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    # ----------------
    # Main update Loop
    # ----------------

    def update(self, keys, delta, field): ##kanske lägg typ "levels", "ground", "platforms". alltså ett sätt för spelaren att se om den är på marken eller inte
        self.on_ground = self.is_on_ground(field)
        self.handle_input(keys, field)
        self.apply_gravity(delta)
        self.move(delta, field)
        #self.set_state()
        #self.animate(delta)
        
        """
        Tolkar key input och uppdaterar spelarens horisontella
        hastighet samt initierar hopp.
        
        parametrar:
        keys (Sequence[bool]): Tangentstatus från pygame.
        """
        
    # --------------
    # Input
    # --------------
        
    def handle_input(self, keys, field):
        self.vx = 0

        if keys[pygame.K_a] and not keys[pygame.K_d]: 
            self.vx = -self.speed

        if keys[pygame.K_d] and not keys[pygame.K_a]: 
            self.vx = self.speed 
    
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vy = -self.jump_strength
            self.on_ground = False

    def is_on_ground(self, field):
        self.rect.y += 1
        grounded = field.is_solid(self.rect)
        self.rect.y -= 1
        return grounded


    # -----------
    # Movement
    # -----------

    """
    Flyttar spelaren baserat på hastighet och tid, samt hanterar
    kollision med marknivån.
    
    paratemetrar:
        delta (float): Tid sedan föregående frame.
        ground (int | float): Y-position för marknivå. BEHÖVER LÄGGAS TILL I GAME.PY
     """   
    def move(self, delta, field):
        # Horizontal movement
        self.x += self.vx * delta
        self.rect.x = int(self.x)

        for p in field.platforms:
            if self.rect.colliderect(p):
                if self.vx > 0:
                    self.rect.right = p.left
                elif self.vx < 0:
                    self.rect.left = p.right
                self.x = self.rect.x

        # Vertical movement
        #old_bottom = self.rect.bottom

        self.y += self.vy * delta
        self.rect.y = int(self.y)
        
        self.on_ground = False

        for p in field.platforms:
            if self.rect.colliderect(p):
                if self.vy > 0:
                    self.rect.bottom = p.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = p.bottom
                    self.vy = 0
                self.y = self.rect.y
        
    # --------
    # Gravity
    # --------

    """
    Sätter gravitation på spelarens vertikala hastighet
   
    parameter:
    delta (float): Tid sedan föregående frame.
    """
    def apply_gravity(self, delta):
       if not self.on_ground:
           self.vy += self.gravity * delta
        ##behöver input från game.py så spelare kan interagera med marken.
            
    
    # ----------
    # Animation
    # ----------

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
    Updaterar animation baserat på spelarens state och animationshastighet
    
    parameter:
    delta (float): Tid sedan föregående frame.
    """
    def animate(self, delta):
        self.frame += self.animation_speed * delta

        if self.frame >= len(self.animations[self.state]):
            self.frame = 0

        self.image = self.animations[self.state][int(self.frame)]
        
    
        