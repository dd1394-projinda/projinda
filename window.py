#
# File to open game window
#

import pygame

# Window properties
background_colour = (224, 247, 250)    # Amount of red, green, blue (255 is max)
(width, height) = (1000, 500)       # Size of window
caption = "Platform game"
#dirt_colour = (205, 175, 140)
platform_colour = (230, 180, 200)       # blue
#cloud_colour = (255, 205, 225)
player_colour = (200, 170, 230)


# Create window
screen = pygame.display.set_mode((width, height))       # Create window
pygame.display.set_caption(caption)             # Add caption to window

screen.fill(background_colour)
# draw block (x,y,width,height), x,y is top left corner
pygame.draw.rect(screen, platform_colour, (0, 400, 1000, 100))
#pygame.draw.rect(screen, dirt_colour, (0,430,1000,70))
pygame.draw.rect(screen, player_colour, (470,340,60,60))


# Keep window open until user closes it
running = True
while running:
    for event in pygame.event.get():        # Goes through all user inputs as events
        if event.type == pygame.QUIT:       # If user presses X on window
            running = False                 # End while loop / close window
    
    
    pygame.display.flip()           # Display the window

