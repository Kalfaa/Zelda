import pygame
class Item(pygame.sprite.Sprite):
    def __init__(self, name, sprite):
        pygame.sprite.Sprite.__init__(self)
        self.nom_item = name
        self.image = sprite
        self.rect = self.image.get_rect()
        self.etats = 'Null'
        self.x = False
        self.y = False
    def changexy(self ,x,y):
        self.x =x
        self.y =y
        self.rect = self.rect.move(x,y)