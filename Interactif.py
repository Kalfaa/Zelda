import pygame


class Interactif(pygame.sprite.Sprite):
    def __init__(self, obj, sprite):
        pygame.sprite.Sprite.__init__(self)
        self.nom_item = obj.name
        self.image = sprite
        self.rect = self.image.get_rect().move(obj.x, obj.y)
        self.etats = 'Null'
        self.obj = obj
        self.x = obj.x
        self.y = obj.y

    def action(self):
        raise NotImplementedError("You must implement foo's %s method" % type(self).__name__)


class Coffre(Interactif):
    def __init__(self, obj, sprite, item):
        Interactif.__init__(self, obj, sprite)
        self.etats = 'Close'
        self.text = "Voici votre epee ! | Appuyer sur espace pour taper ! "
        self.inside = item

    def change_etats(self, etats):
        self.etats = etats

    def changer_sprite(self, sprite):
        self.image = sprite

    def action(self):
        if self.etats == 'Close':
            self.change_etats('Open')
            self.changer_sprite(pygame.image.load('SPRITE/Open_chest.png'))

    def get_text(self):
        return self.text
