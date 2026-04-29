# -----------------
# Camera that follows the players movement    
# -----------------


import pygame

class Camera:
    def __init__(self, width, height):      # width and height represents the size of the map
        self.width = width
        self.height = height
        self.camera = pygame.Rect(0, 0, width, height)
        
    def update(self, player):
        x = player.rect.centerx - self.width // 2           # Centrera spelaren på skärmen
        y = player.rect.centery - self.height // 2 - 120    # Flytta skärmen med spelaren vid hopp
        
        self.camera = pygame.Rect(x, y, self.width, self.height)

    def apply(self, rect):
        return rect.move(self.camera.topleft)