
from Interactif import *

class Perso(pygame.sprite.Sprite):
    liste_vivant = list()

    def __creer_tableau(liste_vivant, map):
        for i in range(map.hauteur):
            liste_vivant.append([0] * map.largeur)
        return liste_vivant

    __creer_tableau = staticmethod(__creer_tableau)

    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'player'
        self.x_ss = 2
        self.carte = game.map
        self.vitesse = 5
        self.x = x * 16
        self.y = y * 16
        self.game = game
        self.interactif = None
        if not Perso.liste_vivant:  # Creer la matrice des vivants si elle n'existe pas
            Perso.__creer_tableau(Perso.liste_vivant, self.carte)


class Hero(Perso):
    def __init__(self, game, x, y):
        Perso.__init__(self, game, x, y)
        self.sprite_coeur = game.sprite_coeur
        self.HP_max = 8
        self.HP_Actuel = 6
        self.x_ss = 2
        self.droite = 40
        self.gauche = 103
        self.bas = 71
        self.haut = 8
        self.width = 18
        self.height = 24
        self.ss = game.link_ss
        self.ss2 = game.link_ss2
        self.image = self.ss.get_image(self.x_ss, self.droite, self.width, self.height)
        self.offset = 24
        self.rect = self.image.get_rect()
        self.rect2 = self.image.get_rect()
        self.ajouter_vivant()
        self.x = x * 16
        self.y = y * 16
        self.etats = 'Free'
        self.converted_text = False
        self.display = False
        ## variable danimation
        self.compteur_animation = 0
        self.sword = self.ss2.get_image(52, 285, 7, 21)
        self.sword_rect = self.sword.get_rect()
        self.sword_display = self.sword
        self.update_animation = 0
        self.i_h = -80
        self.i_b = 100
        self.i_g = 0
        self.i_d = 0
        self.i = 0
        self.direction = "droite"
        self.compteur_animation2 = 0
        self.inventory = list()
        self.invulnerable = 0
        self.invulnerable_update = 0

    def link_direction(self):
        return self.image

    def clear_animation(self):
        self.i_h = -80
        self.i_b = 100
        self.i_g = 0
        self.i_d = 0
        self.i = 0
        self.update_animation = 0
        self.compteur_animation = 0
        self.compteur_animation2 = 0

    def get_keys(self, events):
        now = pygame.time.get_ticks()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.interactif = self.game.map.item_collide(self.rect, 0)
                    if isinstance(self.interactif, Coffre):
                        if self.interactif.etats == 'Close':
                            self.interactif.action()
                            self.converted_text = self.split_texte(self.interactif.get_text())
                            self.display = self.converted_text[0]
                            self.image = self.ss2.get_image(46, 256, 20, 24)
                            self.count = 1
                            item = self.interactif.inside
                            self.inventory.append(item.nom_item)
                            item.changexy((self.x + 10), (self.y - 15))
                    else:
                        if "Sword" in self.inventory:
                            self.etats = 'hit'

        if self.etats == 'hit':
            if self.direction == "haut":
                if now - self.update_animation > 5:
                    self.update_animation = now
                    self.sword_rect = self.sword_display.get_rect()
                    self.sword_rect.center = self.rect.center
                    self.i_h += 5
                    self.compteur_animation += 1
                    self.image = self.ss2.get_image(727 + (self.compteur_animation // 4 * 32), 347, 16, 24)
                    if self.compteur_animation < 17:
                        self.sword_rect.x = self.sword_rect.x + 13 - (self.compteur_animation * 0.80)
                        self.sword_rect.y = self.sword_rect.y - 9 - (self.compteur_animation * 0.50)
                    elif 16 < self.compteur_animation < 22:
                        self.sword_rect.x = self.sword_rect.x - ((self.compteur_animation - 16) * 2)
                        self.sword_rect.y = self.sword_rect.y - 13
                    elif 21 < self.compteur_animation < 29:
                        self.sword_rect.x = self.sword_rect.x - 12
                        self.sword_rect.y = self.sword_rect.y - 13 + (self.compteur_animation - 21)
                    elif 28 < self.compteur_animation < 35:
                        self.sword_rect.x = self.sword_rect.x - 12
                        self.sword_rect.y = self.sword_rect.y + 3
                    elif self.compteur_animation == 35:
                        self.sword_rect.x = self.sword_rect.x + 13
                        self.sword_rect.y = self.sword_rect.y - 7

                    self.i = self.i_h
            elif self.direction == "droite":
                if now - self.update_animation > 5:
                    self.update_animation = now

                    self.sword_rect = self.sword_display.get_rect()
                    self.sword_rect.center = self.rect.center
                    self.i_d -= 5
                    self.compteur_animation += 1
                    if 7 < self.compteur_animation < 12:
                        self.compteur_animation2 = 5
                    elif 15 < self.compteur_animation < 23:
                        self.compteur_animation2 = 7
                    elif 23 < self.compteur_animation < 27:
                        self.compteur_animation2 = 2
                    elif self.compteur_animation > 27:
                        self.compteur_animation2 = -2
                    self.image = pygame.transform.flip(self.ss2.get_image(
                        388 + (self.compteur_animation // 4 * 32) - self.compteur_animation2, 350, 20, 28),
                        1, 0)
                    if 0 < self.compteur_animation < 18:
                        self.sword_rect.x = self.sword_rect.x + 10 + int(self.compteur_animation * 0.40)
                        self.sword_rect.y = self.sword_rect.y - 12 + int(self.compteur_animation * 0.70)
                    elif self.compteur_animation > 17:
                        self.sword_rect.x = self.sword_rect.x + 10 + int(self.compteur_animation * 0.10 - 3)
                        self.sword_rect.y = self.sword_rect.y - 12 + int(self.compteur_animation * 0.60 + 2)

                    self.i = self.i_d
            elif self.direction == "bas":
                if now - self.update_animation > 5:
                    self.update_animation = now
                    self.image = self.ss2.get_image(16 + (self.compteur_animation // 4 * 32), 348, 16, 24)
                    self.sword_rect = self.sword_display.get_rect()
                    self.sword_rect.center = self.rect.center
                    self.i_b += 5
                    self.compteur_animation += 1
                    if 0 < self.compteur_animation < 18:
                        self.sword_rect.x = self.sword_rect.x - 11 + int(self.compteur_animation * 0.80)
                        self.sword_rect.y = self.sword_rect.y + 6 + int(self.compteur_animation * 0.45)

                    elif self.compteur_animation > 17:
                        self.sword_rect.x = self.sword_rect.x - 11 + int(self.compteur_animation * 0.80)
                        self.sword_rect.y = self.sword_rect.y + 2 + int(-self.compteur_animation * 0.30 + 14)
                    self.i = self.i_b
            elif self.direction == "gauche":
                if now - self.update_animation > 5:
                    self.update_animation = now

                    self.sword_rect = self.sword_display.get_rect()
                    self.sword_rect.center = self.rect.center
                    self.compteur_animation += 1
                    self.i_g += 5
                    if 7 < self.compteur_animation < 12:
                        self.compteur_animation2 = 5
                    elif 15 < self.compteur_animation < 23:
                        self.compteur_animation2 = 7
                    elif 23 < self.compteur_animation < 27:
                        self.compteur_animation2 = 2
                    elif self.compteur_animation > 27:
                        self.compteur_animation2 = -2
                    if 0 < self.compteur_animation < 18:
                        self.sword_rect.x = self.sword_rect.x - 6 + int(-self.compteur_animation * 0.40)
                        self.sword_rect.y = self.sword_rect.y - 12 + int(self.compteur_animation * 0.70)
                    elif self.compteur_animation > 17:
                        self.sword_rect.x = self.sword_rect.x - 6 + int(self.compteur_animation * 0.10 - 3)
                        self.sword_rect.y = self.sword_rect.y - 12 + int(self.compteur_animation * 0.60 + 2)
                    self.i = self.i_g
                    self.image = self.ss2.get_image(
                        388 + (self.compteur_animation // 4 * 32) - self.compteur_animation2, 350, 20, 28)
                    if self.compteur_animation == 32:
                        self.compteur_animation = 35
            return 0

        elif self.etats == 'Free':
            self.vx, self.vy = 0, 0
            keys = pygame.key.get_pressed()

            temp = self.rect.copy()
            if now - self.update_animation > 45:
                self.update_animation = now
                if keys[pygame.K_LEFT]:
                    self.direction = "gauche"
                    temp = temp.move(-self.vitesse, 0)
                    self.image = self.ss.get_image(self.x_ss, self.gauche, self.rect2.width, self.rect2.height)
                    self.x_ss += self.offset

                    self.vx = -self.game.map.wall_collision(temp, 'gauche', self.vitesse)
                    self.rect = temp

                    if self.x_ss == 290 and self.gauche == 103:
                        self.x_ss = 2
                        self.gauche = 230
                    if self.x_ss == 290 and self.gauche == 230:
                        self.x_ss = 2
                        self.gauche = 103


                elif keys[pygame.K_RIGHT]:
                    self.direction = "droite"
                    temp = temp.move(+self.vitesse, 0)
                    self.image = self.ss.get_image(self.x_ss, self.droite, self.rect2.width, self.rect2.height)
                    self.x_ss += self.offset

                    self.vx = self.game.map.wall_collision(temp, 'droite', self.vitesse)
                    self.rect = temp

                    if self.x_ss == 290 and self.droite == 40:
                        self.x_ss = 2
                        self.droite = 167
                    if self.x_ss == 290 and self.droite == 167:
                        self.x_ss = 2
                        self.droite = 40

                elif keys[pygame.K_UP]:
                    self.direction = "haut"
                    temp = temp.move(0, -self.vitesse)
                    self.image = self.ss.get_image(self.x_ss, self.haut, self.rect2.width, self.rect2.height)
                    self.x_ss += self.offset

                    self.vy = -self.game.map.wall_collision(temp, 'haut', self.vitesse)
                    self.rect = temp

                    if self.x_ss == 290 and self.haut == 8:
                        self.x_ss = 2
                        self.haut = 135
                    if self.x_ss == 290 and self.haut == 135:
                        self.x_ss = 2
                        self.haut = 8

                elif keys[pygame.K_DOWN]:
                    self.direction = "bas"
                    temp = temp.move(0, +self.vitesse)
                    self.image = self.ss.get_image(self.x_ss, self.bas, self.rect2.width, self.rect2.height)
                    self.x_ss += self.offset
                    self.vy = self.game.map.wall_collision(temp, 'bas', self.vitesse)

                    self.rect = temp

                    if self.x_ss == 290 and self.bas == 71:
                        self.x_ss = 2
                        self.bas = 198
                    if self.x_ss == 290 and self.bas == 198:
                        self.x_ss = 2
                        self.bas = 71

        elif self.etats == 'Talk':
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.key.set_repeat(400, 50)
                        if self.count < len(self.converted_text):
                            self.display = self.converted_text[self.count]
                            self.count += 1

                        else:
                            self.display = False
                            self.etats = "Free"
                            self.converted_text = False
                            self.image = self.ss.get_image(self.x_ss, self.haut, self.width, self.height)
                            return True

    def split_texte(self, text):
        tab = list()
        chaine = ''
        for i in range(len(text)):
            if text[i] != '|':
                chaine += text[i]
            else:
                tab.append(chaine)
                chaine = ''
        tab.append(chaine)
        return tab

    def update(self, event, list_monstre, now):
        self.get_keys(event)
        if self.invulnerable == 0:
            for monstre in list_monstre:
                if pygame.sprite.collide_mask(self, monstre):
                    self.invulnerable = 1
                    self.prend_degat(0.5)
        else:
            time = now - self.invulnerable_update
            if time > 3000:
                self.invulnerable = 0
                self.invulnerable_update = now
        if self.etats == "Free":
            self.x += self.vx
            self.y += self.vy
            self.rect.topleft = (self.x, self.y)
        elif self.etats == "hit":
            for monstre in list_monstre:
                if monstre.invulnerable == 0:
                    if pygame.sprite.collide_mask(self, monstre):
                        if pygame.Rect.colliderect(monstre.rect, self.sword_rect):
                            monstre.prend_degat(1)
                            print("oo")
        self.mask = pygame.mask.from_surface(self.image)

    def stop(self, direction):
        if direction == 'droite':
            self.x_ss = 2
            self.image = self.ss.get_image(self.x_ss, self.droite, self.rect2.width, self.rect2.height)
        if direction == 'haut':
            self.x_ss = 2
            self.image = self.ss.get_image(self.x_ss, self.haut, self.rect2.width, self.rect2.height)
        if direction == 'bas':
            self.x_ss = 2
            self.image = self.ss.get_image(self.x_ss, self.bas, self.rect2.width, self.rect2.height)
        if direction == 'gauche':
            self.x_ss = 2
            self.image = self.ss.get_image(self.x_ss, self.gauche, self.rect2.width, self.rect2.height)

    def ajouter_vivant(self):
        x = int(self.rect.x) // 16
        y = int(self.rect.y) // 16
        self.liste_vivant[y][x] = self.name
        rajout_ligne_y = 0
        rajout_ligne_x = 0
        if (self.rect.y + self.rect.height) % 16 != 0:
            rajout_ligne_y = 1
        if (self.rect.x + self.rect.width) % 16 != 0:
            rajout_ligne_x = 1
        for j in range(int(self.rect.height // 16 + rajout_ligne_y)):
            self.liste_vivant[y][x] = self.name
            for i in range(int(self.rect.width // 16 + rajout_ligne_x)):
                self.liste_vivant[y + j][x + i] = self.name

    def prend_degat(self, val):
        self.HP_Actuel = self.HP_Actuel - val

    def draw(self, window, camera):
        if self.etats == 'hit':
            if self.compteur_animation == 35:
                self.etats = 'Free'
                self.clear_animation()
                if self.direction == 'droite':
                    self.image = self.ss.get_image(self.x_ss, self.droite, self.width, self.height)
                elif self.direction == 'haut':
                    self.image = self.ss.get_image(self.x_ss, self.haut, self.width, self.height)
                elif self.direction == 'bas':
                    self.image = self.ss.get_image(self.x_ss, self.bas, self.width, self.height)
                elif self.direction == 'gauche':
                    self.image = self.ss.get_image(self.x_ss, self.gauche, self.width, self.height)
            else:
                self.sword_display = pygame.transform.rotate(self.sword, self.i)
                window.blit(self.sword_display, camera.apply_rect(self.sword_rect))
    def checkIfDead(self):
        return self.HP_Actuel <= 0