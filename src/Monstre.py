import random

import pygame

from src.Perso import Perso


class Monstre(Perso):
    def __init__(self, game, x, y):
        Perso.__init__(self, game, x, y)
        self.dir = 1
        self.direction = "droite"
        self.HP_max = 8
        self.HP_Actuel = 1
        self.x_ss = 12
        self.ss = game.mob_ss
        self.droite = 64
        self.gauche = 44
        self.x = x * 16
        self.y = y * 16
        self.bas = 23
        self.haut = 87
        self.width = 25
        self.height = 19
        self.image = self.ss.get_image(self.x_ss, self.droite, self.width, self.height)
        self.offset = 15
        self.rect = self.image.get_rect()
        self.update_animation = 0
        self.vx = 0
        self.vy = 0
        self.update_2 = 0
        self.compteur_action = 0
        self.invulnerable = 0
        self.invulnerable_update = 0

    def __del__(self):
        print(' Monstre died')

    def link_direction(self):
        return self.image

    def update(self, now):
        if self.invulnerable == 1:
            time = now - self.invulnerable_update
            print(self.HP_Actuel)
            if time > 3000:
                self.invulnerable = 0
                self.invulnerable_update = now
        if now - self.update_2 > 450:
            self.update_2 = now
            if self.compteur_action == 0:
                self.dir = random.randint(1, 4)  # 1 droite 2 bas 3 gauche 4 haut
            self.deplacer(self.dir)
            self.compteur_action += 1
            if self.compteur_action == 5:
                self.compteur_action = 0
            self.x += self.vx
            self.y += self.vy
            self.rect.topleft = (self.x, self.y)
        self.mask = pygame.mask.from_surface(self.image)

    def deplacer(self, direction):
        now = pygame.time.get_ticks()
        temp = self.rect.copy()
        if now - self.update_animation > 45:
            self.update_animation = now
            self.vx = 0
            self.vy = 0
            if direction == 4:
                self.direction = "haut"
                temp = temp.move(0, -self.vitesse)
                self.image = self.ss.get_image(self.x_ss, self.haut, self.rect.width, self.rect.height)
                self.vy = -self.game.map.wall_collision(temp, 'haut', self.vitesse)
                self.rect = temp
                if self.x_ss == 41:
                    self.x_ss = 12
                else:
                    self.x_ss = 41
            elif direction == 1:
                self.direction = "droite"
                temp = temp.move(+self.vitesse, 0)
                self.image = self.ss.get_image(self.x_ss, self.droite, self.rect.width, self.rect.height)
                self.vx = self.game.map.wall_collision(temp, 'droite', self.vitesse)
                self.rect = temp
                print(self.x_ss)
                if self.x_ss == 39:
                    self.x_ss = 12
                else:
                    self.x_ss = 39
            elif direction == 2:
                self.direction = "bas"
                temp = temp.move(0, +self.vitesse)
                self.image = self.ss.get_image(self.x_ss, self.bas, self.rect.width, self.rect.height)
                self.vy = self.game.map.wall_collision(temp, 'bas', self.vitesse)
                self.rect = temp
                if self.x_ss == 39:
                    self.x_ss = 11
                else:
                    self.x_ss = 39
            elif direction == 3:
                self.direction = "gauche"
                temp = temp.move(-self.vitesse, 0)
                self.image = self.ss.get_image(self.x_ss, self.gauche, self.rect.width, self.rect.height)
                self.vx = -self.game.map.wall_collision(temp, 'gauche', self.vitesse)
                self.rect = temp
                if self.x_ss == 39:
                    self.x_ss = 12
                else:
                    self.x_ss = 39
        self.rect = self.rect.move(self.rect.x, self.rect.y)

    def prend_degat(self, val):
        self.HP_Actuel = self.HP_Actuel - val
        self.invulnerable = 1

    def checkIfDead(self):
        return self.HP_Actuel <= 0
