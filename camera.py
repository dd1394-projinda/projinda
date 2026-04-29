#camera that follows the players movement    
    
import pygame

""""
width and height represents the size of the map
"""
class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.camera = pygame.Rect(0, 0, width, height)
        
    def update(self, player):
        x = player.rect.centerx - self.width // 2 ##centrera spelaren på skärmen
        y = player.rect.centery - self.height // 2 - 120 # actually behöver kanske bara scrollning höger och vänster
        
        self.camera = pygame.Rect(x, y, self.width, self.height)

    def apply(self, rect):
        return rect.move(self.camera.topleft)