# -----------------
# Game: open window, game loop, tangent input, win/lose
# -----------------


# -----------------
# Imports
# -----------------
import pygame
import random
import os

from enum import Enum           # Enumeration, name constant values

from field import Field


from player import Player


from camera import Camera


# -----------------
# WINDOW PROPERTIES
# -----------------
caption             = "Platform Game"       # Window name
background_colour   = (0,0,0)               # Amount of red, green, blue (255 is max, 0 is no color)
platform_colour     = (95, 148, 108)      
enemy_colour        = (173, 69, 31)
TEXT_COLOR          = (255, 255, 255)
TEXT_FONT           = "consolas"                            # Type of font
TEXT_WIN            = "You won!"                            # Game state messages
TEXT_LOSE           = "Maybe try again..."
TEXT_FUNCTIONS      = "Press r to reset and q to quit"      # Instructions message
SCREEN_WIDTH        = 1000
SCREEN_HEIGHT       = 500
WORLD_WIDTH         = 5000
WORLD_HEIGHT        = 500


# -----------------
# CREATE WINDOW
# -----------------


pygame.init()                                           # Initialize pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))     # Create screen
pygame.display.set_caption(caption)                     # Add caption to window

player = Player() #initiera spelare


camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT)
field = Field(WORLD_WIDTH, WORLD_HEIGHT)
player.set_initial_spawn(field)


# -----------------
# FONT
# -----------------
font = pygame.font.SysFont(TEXT_FONT, 75)               # Create font
small_font = pygame.font.SysFont(TEXT_FONT, 30)



# -----------------
# BACKGROUND
# -----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))                                           # Define directory as the current
background_image = pygame.image.load(os.path.join(BASE_DIR, "images", "bg.png")).convert()      # Ladda in bilden
background_image = pygame.transform.smoothscale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))              # Skala om den till skärmens storlek
bg_width = background_image.get_width()                                                         


# -----------------
# GOAL
# -----------------
def reset_goal():       # Function to reset goal for randomization
    goal_x = random.randint(0, 1)
    if goal_x == 0:
        goal_x = 5
    else: 
        goal_x = 4900
    
    goal_y = 400 - 250 
    
    return pygame.Rect(goal_x, goal_y, 75, 225) 
goal_rect = reset_goal()        # Create the goal  
goal_image = pygame.image.load(os.path.join(BASE_DIR, "images", "goal.png")).convert_alpha()    # Ladda in målgrafik
goal_image = pygame.transform.scale(goal_image, (75, 225))  


# -----------------
# BASE FRAME
# -----------------
def base_frame():                           # Frame where the world is
    
    offset_x = -camera.camera.x % bg_width       # Define the cameras offset

    for x in range(-bg_width, SCREEN_WIDTH + bg_width, bg_width):      # Gör så att bakgrunden scrollar när spelaren rör på sig
        screen.blit(background_image, (x + offset_x, 0))        # Paint it onto the screen

    for p in field.platforms:       # Blocks are made in field.py, from the list of platforms, paint them all onto the screen
        pygame.draw.rect(
            screen,
            platform_colour,
            p.move(-camera.camera.x, -camera.camera.y)
        )

    screen.blit(goal_image, goal_rect.move(-camera.camera.x, -camera.camera.y))

    for e in field.enemies:
        pygame.draw.rect(
            screen,
            enemy_colour,
            e.move(-camera.camera.x, -camera.camera.y)
        )



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
class GameState(Enum):          # Enum to have constant values
    PLAYING = 1
    WON = 2
    LOST = 3
state = GameState.PLAYING       # Set state to playing


# -----------------
# CLOCK
# -----------------
clock = pygame.time.Clock()     # Use for the game loop


# -----------------
# GAME LOOP
# -----------------
running = True      # Loop's running state
while running:      # Game loop keeps the window and game going
    
    delta = clock.tick(60) / 1000        # The frame is at most updated 60 times per second
    running, keys = check_events()       # Get the running state and keys pressed
        

    if state == GameState.PLAYING:                  # Determine current game state
        player.update(keys,delta,field)             # Update player position
        
        if player.rect.colliderect(goal_rect):      # If contact with goal -> win
            state = GameState.WON
       
        if field.is_enemy(player.rect):             # If contact with enemy block -> lose
            state = GameState.LOST

    elif state == GameState.LOST:
        if keys[pygame.K_r] and not keys[pygame.K_d]:           # Tanget input handle for reset and quit
            player.reset_after_death()              # Reset function in player, specific for certain game outcomes
            state = GameState.PLAYING               # To keep going after reset  
        elif keys[pygame.K_q]: running = False      # Closes the window immediatly

    elif state == GameState.WON:
        if keys[pygame.K_r]: 
            player.reset_after_win(field)
            goal_rect = reset_goal()
            state = GameState.PLAYING
        elif keys[pygame.K_q]: running = False
        
    camera.update(player)       # Kameran följer efter spelaren
    base_frame()                # Clean frame
    
    image_rect = player.image.get_rect(midbottom=player.rect.midbottom)       # Move player
    screen.blit(player.image, image_rect.move(-camera.camera.x, -camera.camera.y))                                   # Paint player corresponding to it's environment

    if state == GameState.LOST:
        text = font.render(TEXT_LOSE, True, TEXT_COLOR)                         # Render text
        instructions = small_font.render(TEXT_FUNCTIONS, True, TEXT_COLOR)      
        screen.blit(text,(100,100))                                             # Paint the text on the screen
        screen.blit(instructions,(100,200))
        
    elif state == GameState.WON:
        text = font.render(TEXT_WIN, True, TEXT_COLOR)
        instructions = small_font.render(TEXT_FUNCTIONS, True, TEXT_COLOR)
        screen.blit(text,(100,100))
        screen.blit(instructions,(100,200))
        
    pygame.display.update()     # Update screen
    
    