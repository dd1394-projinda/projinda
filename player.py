import pygame
import spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        ss_walk = spritesheet.spritesheet("images/walk.png")
        ss_idle = spritesheet.spritesheet("images/idle.png")
        ss_jump = spritesheet.spritesheet("images/jump.png")
        ss_run  = spritesheet.spritesheet("images/run.png")

        self.animations = {
            "walk": ss_walk.load_strip((0, 0, 128, 128), 8),
            "idle": ss_idle.load_strip((0, 0, 128, 128), 8),
            "jump": ss_jump.load_strip((0, 0, 128, 128), 13),
            "run":  ss_run.load_strip((0, 0, 128, 128), 7),
        }