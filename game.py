# -----------------
# Game: open window, game loop, get tangent input, win/lose
# -----------------


# -----------------
# Imports
# -----------------
import pygame
import random
import time
import os

from enum import Enum           # Enumeration, name constant values

from player import Player 
player = Player()

from camera import Camera
camera = Camera(1000, 500)

from field import Field
field = Field()


# -----------------
# WINDOW PROPERTIES
# -----------------
(width, height)     = (1000, 500)           # Window size
caption             = "Platform Game"       # Window name
background_colour   = (0,0,0)               # Amount of red, green, blue (255 is max, 0 is no color)
platform_colour     = (95, 148, 108)      


# -----------------
# CREATE WINDOW
# -----------------
pygame.init()                                           # Initialize pygame
screen = pygame.display.set_mode((width, height))       # Create window / screen
pygame.display.set_caption(caption)                     # Add caption to window
font = pygame.font.SysFont(None, 72)
TEXT_COLOR = (255, 255, 255)


# -----------------
# BACKGROUND
# -----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
background_image = pygame.image.load(os.path.join(BASE_DIR, "images", "bg.png")).convert()      #ladda bgbild
background_image = pygame.transform.smoothscale(background_image, (width, height))              # skala om den till skärmens storlek
bg_width = background_image.get_width()                                                         


# -----------------
# GOAL
# -----------------
def reset_goal():
    goal_x              = random.randint(700, 980)
    goal_y = 400 - 250
    return pygame.Rect(goal_x, goal_y, 75, 225) 
                                    #skala om till rätt storlek
goal_rect = reset_goal()
goal_image = pygame.image.load(os.path.join(BASE_DIR, "images", "goal.png")).convert_alpha()    #ladda in målgrafik
goal_image = pygame.transform.scale(goal_image, (75, 225))  


# -----------------
# ENEMIES
# -----------------
enemy_rect          = pygame.Rect(300, 365, 35, 35)


# -----------------
# BASE FRAME
# -----------------
def base_frame():
    screen.fill(background_colour)                      # Fill the screen with colour
    
    offset_x = camera.camera.x % bg_width 

    for x in range(-bg_width, width + bg_width, bg_width): #gör så att bakgrunden scrollar när spelaren rör på sig
        screen.blit(background_image, (x + offset_x, 0)) 

    platform_rect = pygame.Rect(0,400,1000,100)
    pygame.draw.rect(screen, platform_colour, platform_rect.move(-camera.camera.x, -camera.camera.y))              # draw block (x,y,width,height), x,y is top left corner (0,0) increases to bottom right corner
    pygame.draw.rect(screen, (255,0,0),enemy_rect.move(-camera.camera.x, -camera.camera.y))
    screen.blit(goal_image, goal_rect.move(-camera.camera.x, -camera.camera.y))
    #pygame.draw.rect(screen, (0, 255, 0), goal_rect.move(-camera.camera.x, -camera.camera.y))                            # målet, där spelaren går för att vinna

    small_platform = pygame.Rect(100,350,50,50)
    pygame.draw.rect(screen, platform_colour, small_platform.move(-camera.camera.x, -camera.camera.y))


# -----------------
# TANGENT INPUT
# -----------------
def check_events():
    keys = pygame.key.get_pressed()         # Keys that get pressed, including once and hold down
    for event in pygame.event.get():        # Goes through all user inputs as events
        if event.type == pygame.QUIT:       # If user presses X on window
            return False, keys              # Return false (will close the window later in the code), return keys
    return True, keys                       # Otherwise keep window open, always return keys


# -----------------
# GAME STATE
# -----------------
class GameState(Enum):
    PLAYING = 1
    WON = 2
    LOST = 3
state = GameState.PLAYING


# -----------------
# CLOCK
# -----------------
clock = pygame.time.Clock()                 # Pygame's clock, fairly accurate timing, to use for the game loop


# -----------------
# WINDOW RUNNING
# -----------------
running = True
while running:
    
    delta = clock.tick(60) / 1000                   # The frame is at most updated 60 times per second
    running, keys = check_events()                  # Get the running state and keys pressed
        
    camera.update(player)       #kameran följer efter spelaren
    base_frame()

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
            goal_rect = reset_goal()
            state = GameState.PLAYING
        elif keys[pygame.K_q]: running = False

    player_screen_rect = player.rect.move(-camera.camera.x, -camera.camera.y)
    screen.blit(player.image, player_screen_rect)
    pygame.display.update()     # Update display / screen
    
    