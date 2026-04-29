""" 
Game: open window, game loop, get tangent input
"""


# Import pygame for graphics and game functions
import pygame
import sys 
import random
import time


""" Window properties """
(width, height)     = (1000, 500)           # Size of window
caption             = "Platform game"       # Window name
background_colour   = (224, 247, 250)       # Amount of red, green, blue (255 is max, 0 is no color)
platform_colour     = (230, 180, 200)       
player_colour       = (200, 170, 230)
#dirt_colour        = (205, 175, 140)
#cloud_colour       = (255, 205, 225)
goal_x = random.randint(700, 950)
goal_rect = pygame.Rect(goal_x, 350, 20, 50)
game_over = False
winner_text = ""


""" Create window """
pygame.init()                                           # Initialize pygame
screen = pygame.display.set_mode((width, height))       # Create window / screen
pygame.display.set_caption(caption)                     # Add caption to window
font = pygame.font.SysFont(None, 72)
TEXT_COLOR = (0, 0, 0)


# Extend player class, create object / player, camera
from player import Player
player = Player()

from camera import Camera
camera = Camera(1000, 500)


""" Base frame """
def base_frame():
    screen.fill(background_colour)                      # Fill the screen with colour

    # draw block (x,y,width,height), x,y is top left corner (0,0) increases to bottom right corner
    pygame.draw.rect(screen, platform_colour, (0, 400, 1000, 100))
    #pygame.draw.rect(screen, dirt_colour, (0,430,1000,70))
    
    pygame.draw.rect(screen, (255, 0, 0), camera.apply(goal_rect)) ##målet, där spelaren går för att vinna


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
    
    

  


    
   
        
        
    

