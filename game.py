""" 
Game: open window, game loop, get tangent input
"""


# Import pygame for graphics and game functions
import pygame


""" Window properties """
(width, height)     = (1000, 500)           # Size of window
caption             = "Platform game"       # Window name
background_colour   = (224, 247, 250)       # Amount of red, green, blue (255 is max, 0 is no color)
platform_colour     = (230, 180, 200)       
player_colour       = (200, 170, 230)
#dirt_colour        = (205, 175, 140)
#cloud_colour       = (255, 205, 225)


""" Create window """
pygame.init()                                           # Initialize pygame
screen = pygame.display.set_mode((width, height))       # Create window / screen
pygame.display.set_caption(caption)                     # Add caption to window


# Extend player class, create object / player
from player import Player
player = Player()


""" Base frame """
def base_frame():
    screen.fill(background_colour)                      # Fill the screen with colour

    # draw block (x,y,width,height), x,y is top left corner (0,0) increases to bottom right corner
    pygame.draw.rect(screen, platform_colour, (0, 400, 1000, 100))
    #pygame.draw.rect(screen, dirt_colour, (0,430,1000,70))


""" Collect events """
def check_events():
    keys = pygame.key.get_pressed()         # Keys that get pressed, including once and hold down
    for event in pygame.event.get():        # Goes through all user inputs as events
        if event.type == pygame.QUIT:       # If user presses X on window
            return False, keys              # Return false (will close the window later in the code), return keys
    return True, keys                       # Otherwise keep window open, always return keys


""" Clock """
clock = pygame.time.Clock()                 # Pygame's clock, fairly accurate timing, to use for the game loop


""" Keep window open until user closes it """
running = True
while running:
    delta = clock.tick(60) / 1000                   # The frame is at most updated 60 times per second
    running, keys = check_events()                  # Get the running state and keys pressed

    ground = 400
    player.update(keys, delta, ground)


    base_frame()                # Clean the frame / remove the players previous position
    screen.blit(player.image, player.rect) 
    pygame.display.update()     # Update display / screen