# -----------------
# Camera that follows the players movement    
# -----------------


import pygame

class Camera:
    def __init__(self, screen_width, screen_height, world_width, world_height):      # width and height represents the size of the map
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_width = world_width
        self.world_height = world_height
        self.camera = pygame.Rect(0, 0, screen_width, screen_height)
        
    def update(self, player):
        x = player.rect.centerx - self.screen_width // 2           # Centrera spelaren på skärmen
        
        x = max(0, min(x, self.world_width - self.screen_width))
        y = 0
        
        self.camera = pygame.Rect(x, y, self.screen_width, self.screen_height)

    def apply(self, rect):
        return rect.move(-self.camera.x, -self.camera.y)