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
enemy_colour        = (230, 69, 60)
TEXT_COLOR          = (255, 255, 255)
TEXT_FONT           = "consolas"                            # Type of font
TEXT_WIN            = "You won!"                            # Game state messages
TEXT_LOSE           = "Maybe try again..."
TEXT_FUNCTIONS      = "Press r to reset and q to quit"      # Instructions message
SCREEN_WIDTH        = 1000
SCREEN_HEIGHT       = 500
TILE                = 100
TILE_AMOUNT         = 70
WORLD_WIDTH         = TILE_AMOUNT * TILE
WORLD_HEIGHT        = 550


# -----------------
# CREATE WINDOW
# -----------------
pygame.init()                                           # Initialize pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))     # Create screen
pygame.display.set_caption(caption)                     # Add caption to window

player = Player() #initiera spelare

camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT)
field = Field(WORLD_WIDTH, WORLD_HEIGHT, TILE)


# -----------------
# FONT
# -----------------
font        = pygame.font.SysFont(TEXT_FONT, 75)               # Create font
small_font  = pygame.font.SysFont(TEXT_FONT, 30)


# -----------------
# IMAGES
# -----------------
BASE_DIR            = os.path.dirname(os.path.abspath(__file__))                                           # Define directory as the current
background_image    = pygame.image.load(os.path.join(BASE_DIR, "images", "bg.png")).convert()      # Ladda in bilden
background_image    = pygame.transform.smoothscale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))              # Skala om den till skärmens storlek
bg_width            = background_image.get_width()                                                         
grass_img           = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "images", "grass.png")).convert(), (TILE, TILE//5))
grass2_img           = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "images", "grass2.png")).convert(), (TILE, TILE//5))
enemy_img           = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "images", "enemy.png")).convert(), (40,40))
dirt_img            = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "images", "dirt.png")).convert(), (TILE, TILE))


# -----------------
# GOAL & SIGN
# -----------------
sign_rect = pygame.Rect(0,0,0,0)        # Placeholder, more of the sign in reset_goal and base_frame

def reset_goal():       # Function to reset goal for randomization
    global sign_rect
    side = random.randint(0, 1)

    goal_w = 75         # Goal properties
    goal_h = 225

    sign_w = 150        # Sign properties
    sign_h = 80
    sign_y = 270

    if side == 0:       # If left side, goal left, sign right
        goal_x = 10
        sign_rect = pygame.Rect(WORLD_WIDTH - 20 - sign_w, sign_y, sign_w, sign_h)
    if side == 1:       # Opposite
        goal_x = WORLD_WIDTH - goal_w - 10
        sign_rect = pygame.Rect(20, sign_y, sign_w, sign_h)
    
    goal_y = 400 - goal_h 
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

    # DRAW PLATFORMS
    for p in field.platforms:       # Blocks are made in field.py, from the list of platforms, paint them all onto the screen
        drawn = p.move(-camera.camera.x, -camera.camera.y)
        if drawn.right < 0 or drawn.left > SCREEN_WIDTH:   # Skip if off screen horizontally
            continue
        screen.blit(grass2_img, (drawn.x, drawn.top))              # Top tile = grass
        for y in range(drawn.top + TILE//5, drawn.bottom, TILE):
            screen.blit(dirt_img, (drawn.x, y))     
    
    

    # -----------------
    # DRAW SIGN
    # -----------------
    pygame.draw.rect(screen, (60, 40, 20), (sign_rect.x + 55 - camera.camera.x, sign_rect.y + sign_rect.height - camera.camera.y, 10, 50))
    pygame.draw.rect(screen, (60, 40, 20), (sign_rect.x - camera.camera.x, sign_rect.y - camera.camera.y, sign_rect.width, sign_rect.height))
    sign_font = pygame.font.SysFont("Arial", 14, bold=True)
    lines = ["Can't you read a map?", "The goal is on the", "other side!"]
    for i, line in enumerate(lines):
        img = sign_font.render(line, True, (255, 255, 255))
        screen.blit(img, (sign_rect.x + 5 - camera.camera.x, sign_rect.y + 10 + (i * 20) - camera.camera.y))
    
    # DRAW GOAL
    screen.blit(goal_image, goal_rect.move(-camera.camera.x, -camera.camera.y))

    # DRAW ENEMIES
    for e in field.enemies:
        drawn = e.move(-camera.camera.x, -camera.camera.y)

        if drawn.right < 0 or drawn.left > SCREEN_WIDTH:
            continue

        if e.width == field.ENEMY_SIZE and e.height == field.ENEMY_SIZE:
            screen.blit(enemy_img, drawn)
        else:
            pygame.draw.rect(screen, enemy_colour, drawn)



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
        
    # DETERMINE/ACT GAME STATE
    if state == GameState.PLAYING:                  # Determine current game state
        player.update(keys,delta,field)             # Update player position
        
        if player.rect.colliderect(goal_rect):      # If contact with goal -> win
            state = GameState.WON
       
        if field.is_enemy(player.rect):             # If contact with enemy block -> lose
            player.die()
            state = GameState.LOST 

    elif state == GameState.LOST:
        player.animate(delta)       #GÖR DÖDANIMATION MEN DEN VAR LOWKEY FUL??
        if keys[pygame.K_r] and not keys[pygame.K_d]:           # Tanget input handle for reset and quit
            player.reset()
            camera.update(player)
            state = GameState.PLAYING               # To keep going after reset  
        elif keys[pygame.K_q]: running = False      # Closes the window immediatly

    elif state == GameState.WON:
        if keys[pygame.K_r]: 
            player.reset()
            field.reset_world()
            goal_rect = reset_goal()
            state = GameState.PLAYING
        elif keys[pygame.K_q]: running = False
        
    camera.update(player)       # Kameran följer efter spelaren
    base_frame()                # Clean frame
    
    # UPDATE PLAYER POSITION
    off_x = (player.image.get_width() - player.rect.width) // 2
    off_y = (player.image.get_height() - player.rect.height)
    screen.blit(player.image, (player.rect.x - off_x - camera.camera.x, player.rect.y - off_y - camera.camera.y))
    
    # -----------------
    # TEXT OVERLAY
    # -----------------
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