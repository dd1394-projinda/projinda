# 
# Game: open window, game loop, get tangent input, win/lose
# 


import pygame
import random


# -----------------
# Window properties
# -----------------
(width, height)     = (1000, 500)           # Size of window
caption             = "Platform game"       # Window name
background_colour   = (224, 247, 250)       # Amount of red, green, blue (255 is max, 0 is no color)
platform_colour     = (230, 180, 200)       
player_colour       = (200, 170, 230)
#dirt_colour        = (205, 175, 140)
#cloud_colour       = (255, 205, 225)


""" Object properties """
goal_x              = random.randint(700, 980)
goal_rect           = pygame.Rect(goal_x, 0, 20, 400)
enemy_rect          = pygame.Rect(200, 350, 50, 50)


""" Create window """
pygame.init()                                           # Initialize pygame
screen = pygame.display.set_mode((width, height))       # Create window / screen
pygame.display.set_caption(caption)                     # Add caption to window
font = pygame.font.SysFont(None, 72)
TEXT_COLOR = (0, 0, 0)


# Extend player class, create object / player
from player import Player
player = Player()


""" Base frame """
def base_frame():
    screen.fill(background_colour)                      # Fill the screen with colour

    pygame.draw.rect(screen, platform_colour, (0, 400, 1000, 100))              # draw block (x,y,width,height), x,y is top left corner (0,0) increases to bottom right corner
    pygame.draw.rect(screen, (255,0,0), enemy_rect)
    pygame.draw.rect(screen, (0, 255, 0), goal_rect) ##målet, där spelaren går för att vinna




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
        ground = 400
        player.update(keys,delta,ground)
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
            state = GameState.PLAYING
        elif keys[pygame.K_q]: running = False

    screen.blit(player.image, player.rect)
    pygame.display.update()     # Update display / screen
    
    

