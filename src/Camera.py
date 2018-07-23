import pygame


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(450 / 2)
        y = -target.rect.centery + int(320 / 2)
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - 450), x)
        y = max(-(self.height - 320), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)
