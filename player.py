# -----------------
# Player: handle tanget input, player data, player movement, player animation
# -----------------


import pygame
import spritesheet
import os
import random


class Player(pygame.sprite.Sprite): 

    # -----------------
    # Representerar spelaren
    #
    # Klassen hanterar spelarens rörelse, gravitation, hopp,
    # markkollision och animationer baserat på spelarens state.
    # -----------------

    def __init__(self):
        
        # -----------------
        # Uppdaterar spelarens rörelse och gravitation. animerar spelaren.
         
        # Parametrar:
        # keys (Sequence[bool]): Tangentstatus från pygame.
        # delta (float): Tid sedan föregående frame.
        #ground (int | float): Y-position för marknivå.
        # -----------------

        """ 
        BASE_DIR = os.path.dirname(__file__)                    # Initierar spelaren och laddar in animationer för olika states
        ss_walk = spritesheet.spritesheet(os.path.join(BASE_DIR, "images", "walk.png"))
        ss_idle = spritesheet.spritesheet(os.path.join(BASE_DIR, "images", "idle.png"))
        ss_jump = spritesheet.spritesheet(os.path.join(BASE_DIR, "images", "jump.png"))
        ss_run = spritesheet.spritesheet(os.path.join(BASE_DIR, "images", "run.png"))
        
        #kan lägga till död, skadad, spring, attack, etc. många idleanimationer. bilder finns! finns även en röd slime som kan vara fiende?


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

        self.x      = float(self.rect.x)    # Prevents choppy movement
        self.y      = float(self.rect.y)    # Prevents choppy movement
        
        self.vx     = 0
        self.vy     = 0
        
        self.speed          = 200
        self.jump_strength  = 800
        self.gravity        = 2000
        self.on_ground      = True

        self.spawn          = None
    

    # -----------------
    # SPAWN METHODS
    # -----------------
    """ CAN'T GET RANDOM SPAWN TO WORK PROPERLY """
    def get_spawn(self, field):
        attempts = 50
        for _ in range(attempts):
            x = random.randint(200, 800)        # Horizontal range
            y = 100                             # Fixed spawn height

            # Create a rect where the player would spawn
            test_rect = pygame.Rect(x, y, self.rect.width, self.rect.height)

            # 1️ Check if the spawn itself is empty
            if field.is_solid(test_rect):
                continue

            # 2 Check if spawn collides with enemy block
            if any(test_rect.colliderect(e) for e in field.enemies):
                continue

            # 3 Check if there is a platform below at y >= 400
            platform_below = None
            for p in field.platforms:
                if x + self.rect.width > p.left and x < p.right:
                    platform_below = p
                    break

            if not platform_below:
                continue  # try another x
            
            # set spawn y to be on top of the platform
            y = platform_below.top - self.rect.height
            return x, y

        return 500, 500     # fallback if no safe spot found

    def set_initial_spawn(self, field):
        if self.spawn is None:
            self.spawn = self.get_spawn(field)
        self.x, self.y = self.spawn
        self.reset()


    # -----------------
    # RESET METHODS
    # -----------------
    def reset(self):
        self.vx = 0
        self.vy = 0
        self.on_ground = True
        
        """
        self.state = "idle"
        self.frame = 0
        """

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def reset_after_death(self):
        """
        if self.spawn is None:
            self.spawn = 600,350    # Fallback, shouldn't happen
        self.x, self.y = self.spawn
        """

        self.x, self.y = 600,350
        self.reset()

    def reset_after_win(self, field):
        """
        safe_spawn = self.get_spawn(field)
        self.spawn = safe_spawn
        self.x, self.y = self.spawn
        """

        self.x, self.y = random.randint(300,800), 350
        self.reset()

        
    # -----------------
    # MAIN UPDATE LOOP
    # -----------------
    def update(self, keys, delta, field): ##kanske lägg typ "levels", "ground", "platforms". alltså ett sätt för spelaren att se om den är på marken eller inte
        # -----------------
        # Tolkar key input och uppdaterar spelarens horisontella
        # hastighet samt initierar hopp.
        #
        # parametrar:
        # keys (Sequence[bool]): Tangentstatus från pygame.
        # -----------------

        self.on_ground = self.is_on_ground(field)
        self.handle_input(keys, field)
        self.apply_gravity(delta)
        self.move(delta, field)
        
        """
        self.set_state()
        #self.animate(delta)
        """
   
        
    # --------------
    # Input
    # --------------
    def handle_input(self, keys, field):
        self.vx = 0

        if keys[pygame.K_a] and not keys[pygame.K_d]: self.vx = -self.speed
        if keys[pygame.K_d] and not keys[pygame.K_a]: self.vx = self.speed 
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vy = -self.jump_strength
            self.on_ground = False


    # -----------------
    # CHECK GROUND
    # -----------------
    def is_on_ground(self, field):
        self.rect.y += 1
        grounded = field.is_solid(self.rect)
        self.rect.y -= 1
        return grounded


    # -----------------
    # Movement
    # -----------------
    def move(self, delta, field):       # Flyttar spelaren baserat på hastighet och tid, samt hanterar kollision med mark och sida.
        # delta (float): Tid sedan föregående frame
        # field information om världen från field.py
        
        # Horizontal movement
        self.x += self.vx * delta       # Move x-coordinate, based on speed to create a smooth animation
        self.rect.x = int(self.x)

        for p in field.platforms:               # For every platform
            if self.rect.colliderect(p):        # If player is about to collide, player won't move in that direction
                if self.vx > 0:
                    self.rect.right = p.left
                elif self.vx < 0:
                    self.rect.left = p.right
                self.x = self.rect.x            # Both cases handle -> no platform -> move x-coordinate

        # Vertical movement
        self.y += self.vy * delta
        self.rect.y = int(self.y)
        
        self.on_ground = False          # To prevent jumping through platforms

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


    # -----------------
    # Gravity
    # -----------------
    def apply_gravity(self, delta):
        # -----------------
        # Sätter gravitation på spelarens vertikala hastighet
        #
        # parameter:
        # delta (float): Tid sedan föregående frame
        # -----------------
        if not self.on_ground:
           self.vy += self.gravity * delta
            
    
    # -----------------
    # Animation
    # -----------------
    def set_state(self):
        # -----------------
        # Bestämmer spelarens nuvarande state (idle, walk, jump)
        # baserat på rörelse och om spelaren är på marken.
        # -----------------
        if not self.on_ground:
            new_state = "jump"
        elif self.vx == 0:
            new_state= "idle"
        else: 
            new_state = "walk"
            
            # Potentiellt lägg till dash och spring action här
            
        if new_state != self.state:
            self.state = new_state
            self.frame = 0
    
    def animate(self, delta):
        # -----------------
        # Updaterar animation baserat på spelarens state och animationshastighet
        #
        # parameter:
        # delta (float): Tid sedan föregående frame
        # -----------------
        self.frame += self.animation_speed * delta

        if self.frame >= len(self.animations[self.state]):
            self.frame = 0

        self.image = self.animations[self.state][int(self.frame)]
        