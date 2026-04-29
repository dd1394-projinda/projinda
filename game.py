# 
# Game: open window, game loop, get tangent input, win/lose
# 


import pygame
import random
import time
import os

# -----------------
# Window properties
# -----------------
(width, height)     = (1000, 500)           # Size of window
caption             = "Platform game"       # Window name
background_colour   = (224, 247, 250)       # Amount of red, green, blue (255 is max, 0 is no color)
platform_colour     = (0, 0, 0)       
#dirt_colour        = (205, 175, 140)
#cloud_colour       = (255, 205, 225)


""" Goal """
def create_goal():
    goal_x              = random.randint(700, 980)
    return pygame.Rect(goal_x, 0, 20, 400) 
goal_rect = create_goal()

""" Object properties """
enemy_rect          = pygame.Rect(300, 365, 35, 35)


""" Create window """
pygame.init()                                           # Initialize pygame
screen = pygame.display.set_mode((width, height))       # Create window / screen
pygame.display.set_caption(caption)                     # Add caption to window


"""
BASE_DIR = os.path.dirname(__file__)
background_image = pygame.image.load(os.path.join(BASE_DIR, "images", "bg.png")).convert()
background_image = pygame.transform.smoothscale(background_image, (width, height))
bg_width = background_image.get_width()
bg_height = background_image.get_height()

goal_image = pygame.image.load(os.path.join(BASE_DIR, "images", "goal.png")).convert_alpha()
goal_image = pygame.transform.scale(goal_image, (50, 150))
goal_rect = goal_image.get_rect(topleft=(goal_x, 400 - 150))
"""

font = pygame.font.SysFont(None, 72)
TEXT_COLOR = (255, 255, 255)

# Extend player class, create object / player, camera
from player import Player
player = Player()

"""
from camera import Camera
camera = Camera(1000, 500)
"""

""" Base frame """
def base_frame():
        # horizontal scroll based on camera
    #offset_x = camera.camera.x % bg_width

    pygame.draw.rect(screen, platform_colour, (0, 400, 1000, 100))              # draw block (x,y,width,height), x,y is top left corner (0,0) increases to bottom right corner
    pygame.draw.rect(screen, (255,0,0), enemy_rect)
    pygame.draw.rect(screen, (0, 255, 0), goal_rect)                            # målet, där spelaren går för att vinna

    pygame.draw.rect(screen, platform_colour, (100,350,50,50))


# Field import
from field import Field
field = Field()


""" Collect events """
def check_events():
    keys = pygame.key.get_pressed()         # Keys that get pressed, including once and hold down
    for event in pygame.event.get():        # Goes through all user inputs as events
        if event.type == pygame.QUIT:       # If user presses X on window
            return False, keys              # Return false (will close the window later in the code), return keys
    return True, keys                       # Otherwise keep window open, always return keys


""" Game State """
from enum import Enum
class GameState(Enum):
    PLAYING = 1
    WON = 2
    LOST = 3


""" Clock """
clock = pygame.time.Clock()                 # Pygame's clock, fairly accurate timing, to use for the game loop


""" keep game open until player wins/loses """
running = True
state = GameState.PLAYING
while running:
    
    delta = clock.tick(60) / 1000                   # The frame is at most updated 60 times per second
    running, keys = check_events()                  # Get the running state and keys pressed
    
    base_frame()                # Clean the frame / remove the players previous position
    
    if state == GameState.PLAYING:
        player.update(keys,delta,field)
        if player.rect.colliderect(goal_rect):
            state = GameState.WON
        if player.rect.colliderect(enemy_rect):
            state = GameState.LOST

    elif state == GameState.LOST:
        text = font.render("Try again! Press r \n ): quit with q", True, TEXT_COLOR)
        screen.blit(text,(100,100))
        if keys[pygame.K_r] and not keys[pygame.K_d]: 
            player.reset_after_death()
            state = GameState.PLAYING
        elif keys[pygame.K_q]: running = False

    elif state == GameState.WON:
        text = font.render("You won! To reset press r, to quit q", True, TEXT_COLOR)
        screen.blit(text,(100,100))
        if keys[pygame.K_r]: 
            player.reset_after_win()
            goal_rect = create_goal()
            state = GameState.PLAYING
        elif keys[pygame.K_q]: running = False

    screen.blit(player.image, player.rect)
    pygame.display.update()     # Update display / screen
    
    


#### old code that was accidentally deleted 
### här är allt som togs bort

""" 
Game: open window, game loop, get tangent input
"""


# Import pygame for graphics and game functions
import pygame
import sys 
import random
import time
import os

""" Window properties """
(width, height)     = (1000, 500)           # Size of window
caption             = "Platform game"       # Window name
background_colour   = (224, 247, 250)       # Amount of red, green, blue (255 is max, 0 is no color)
platform_colour     = (0, 0, 0)       
#dirt_colour        = (205, 175, 140)
#cloud_colour       = (255, 205, 225)
goal_x = random.randint(700, 950)
game_over = False
winner_text = ""


""" Create window """
pygame.init()                                           # Initialize pygame
screen = pygame.display.set_mode((width, height))       # Create window / screen
pygame.display.set_caption(caption)                     # Add caption to window


BASE_DIR = os.path.dirname(__file__)
background_image = pygame.image.load(os.path.join(BASE_DIR, "images", "bg.png")).convert()
background_image = pygame.transform.smoothscale(background_image, (width, height))
bg_width = background_image.get_width()
bg_height = background_image.get_height()

goal_image = pygame.image.load(os.path.join(BASE_DIR, "images", "goal.png")).convert_alpha()
goal_image = pygame.transform.scale(goal_image, (50, 150))
goal_rect = goal_image.get_rect(topleft=(goal_x, 400 - 150))

font = pygame.font.SysFont(None, 72)
TEXT_COLOR = (255, 255, 255)

# Extend player class, create object / player, camera
from player import Player
player = Player()

from camera import Camera
camera = Camera(1000, 500)


""" Base frame """
def base_frame():
        # horizontal scroll based on camera
    offset_x = camera.camera.x % bg_width

    for x in range(-bg_width, width + bg_width, bg_width):
        screen.blit(background_image, (x + offset_x, 0))
        
    pygame.draw.rect(screen, platform_colour, (0, 400, 1000, 100))

    screen.blit(goal_image, camera.apply(goal_rect))
    


""" Collect events """
def check_events():
    keys = pygame.key.get_pressed()         # Keys that get pressed, including once and hold down
    for event in pygame.event.get():        # Goes through all user inputs as events
        if event.type == pygame.QUIT:       # If user presses X on window
            return False, keys              # Return false (will close the window later in the code), return keys
    return True, keys                       # Otherwise keep window open, always return keys


""" Clock """
clock = pygame.time.Clock()                 # Pygame's clock, fairly accurate timing, to use for the game loop


""" keep game open until player wins/loses """
running = True
while running:
    
    delta = clock.tick(60) / 1000                   # The frame is at most updated 60 times per second
    running, keys = check_events()                  # Get the running state and keys pressed
    
    base_frame()                # Clean the frame / remove the players previous position
    
    camera.update(player)
    
    if not game_over:
        ground = 400
        player.update(keys, delta, ground)
        
        if player.rect.colliderect(goal_rect): #hur spelet avslutas, hur spelaren vinner
            game_over = True
            winner_text = "YOU WIN! :-D"
            
            base_frame()
            screen.blit(player.image, camera.apply(player.rect))

            game_over_text = font.render(winner_text, True, TEXT_COLOR)
            screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2,
                                        height // 2 - game_over_text.get_height() // 2))

            pygame.display.update()
            time.sleep(1) #så att spelet inte stängs på en gång
            running = False
            
    screen.blit(player.image, camera.apply(player.rect))

    if game_over:
        game_over_text = font.render(winner_text, True, TEXT_COLOR)
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2,
                                     height // 2 - game_over_text.get_height() // 2))
                                     
  
    pygame.display.update()     # Update display / screen
    
    

  


    
   
        
        
    

