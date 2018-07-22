import pygame


class Obstacle(pygame.Rect):
    def __init__(self, rect):
        self.name= rect.name
        self.y = rect.y
        self.x = rect.x
        self.height = rect.height
        self.width  = rect.width
        self.rotation =rect.rotation