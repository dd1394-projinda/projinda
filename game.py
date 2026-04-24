""" 

Game file
__open window
__game loop
__tangent input

"""


# Import pygame for graphics and game functions
import pygame
import sys


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


""" Falsified player, made in place for game loop logic """
class Player():                             # Seperate class for simplicity, easier to change and keeps game base and player seperate
    def __init__(player, x, screen):        # Initialize, parameters x coordinate and screen
        player.screen = screen              # Player is on the previously created screen
        player.x = x                        # Player's x coordinate is defined
    def show(player):                       # Function to show the player on the screen
        pygame.draw.rect(screen, player_colour, (player.x,340,60,60))       # Player is a rectangle, only varying value is currently x-position
x = 470                                     # Where the ground begins
player = Player(x, screen)                  # Create the player
player_speed = 200                          # Pixels per second, that the player can move


""" Clock """
clock = pygame.time.Clock()                 # Pygame's clock, fairly accurate timing, to use for the game loop


""" Keep window open until user closes it """
running = True
while running:
    dt = clock.tick(60)                             # The frame is at most updated 60 times per second
    running, keys = check_events()                  # Get the running state and keys pressed

    if keys[pygame.K_d]:                            # if d is pressed
        player.x += player_speed * dt / 1000        # Player moves to the right
    if keys[pygame.K_a]:
        player.x -= player_speed * dt / 1000

    base_frame()                # Clean the frame / remove the players previous position
    player.show()               # Draw the player, function from the player class
    pygame.display.update()     # Update display / screen