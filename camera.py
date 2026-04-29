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
        x = self.width // 2 - player.rect.centerx ##centrera spelaren på skärmen
       ## y = int (self.game.height / 2) - player.rect.bottom  actually behöver kanske bara scrollning höger och vänster
        
        self.camera = pygame.Rect(x, 0, self.width, self.height)

    def apply(self, rect):
        return rect.move(self.camera.topleft)