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
platform_colour     = (20, 30, 80)       
goal_x = random.randint(700, 950)
goal_rect = pygame.Rect(goal_x, 350, 20, 50)
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
font = pygame.font.SysFont(None, 72)
TEXT_COLOR = (255, 255, 255)

# Extend player class, create object / player, camera
from player import Player
player = Player()

from camera import Camera
camera = Camera(1000, 500)

from field import Field
field = Field()


""" Base frame """
def base_frame():
        # horizontal scroll based on camera
    offset_x = camera.camera.x % bg_width

    for x in range(-bg_width, width + bg_width, bg_width):
        screen.blit(background_image, (x + offset_x, 0))

    pygame.draw.rect(screen, platform_colour, (0, 400, 1000, 100))
    pygame.draw.rect(screen, (255, 0, 0), camera.apply(goal_rect))


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
        player.update(keys, delta, field)
        
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
    
    

  


    
   
        
        
    
