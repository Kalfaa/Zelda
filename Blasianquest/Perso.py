import pygame





class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()
        self.width = self.sprite_sheet.get_rect().width
        self.height = self.sprite_sheet.get_rect().height

    def get_image(self, x, y, width, height):
        BLACK = (0, 0, 0)
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """
        # Create a new blank image
        image = pygame.Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Assuming black works as the transparent color
        image.set_colorkey(BLACK)

        # Return the image
        return image


class Perso(pygame.sprite.Sprite):
    liste_vivant = list()

    def __creer_tableau(liste_vivant ,map ):
        for i in range(map.hauteur):
            liste_vivant.append([0] * map.largeur)
        return liste_vivant
    __creer_tableau = staticmethod(__creer_tableau)
    def __init__(self,game,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'player'
        self.x_ss = 2
        self.carte = game.map
        self.vitesse = 5
        self.x = x* 16
        self.y=y*16
        self.game = game
        self.interactif = None
        if not Perso.liste_vivant : #Creer la matrice des vivants si elle n'existe pas
            Perso.__creer_tableau(Perso.liste_vivant , self.carte)


class Hero(Perso):
    def __init__(self,game,x,y):
            Perso.__init__(self, game,x,y)

            self.sprite_coeur = game.sprite_coeur
            self.HP_max = 8
            self.HP_Actuel = 4.5
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
            self.x = x*16
            self.y =y*16
            self.etats = 'Free'
            self.converted_text = False
            self.display = False


    def link_direction(self):
        return self.image

    def get_keys(self,events):

        if (self.etats ==  'Free' ):
                self.vx , self.vy = 0,0
                keys = pygame.key.get_pressed()

                temp = self.rect.copy()

                if keys[pygame.K_LEFT]:

                    temp = temp.move(-self.vitesse, 0)
                    self.image = self.ss.get_image(self.x_ss, self.gauche, self.rect2.width, self.rect2.height)
                    self.x_ss += self.offset
                    pygame.time.delay(45)
                    self.vx = -self.game.map.wall_collision(temp, 'gauche', self.vitesse)
                    self.rect = temp

                    if self.x_ss == 290 and self.gauche == 103:
                            self.x_ss = 2
                            self.gauche = 230
                    if self.x_ss == 290 and self.gauche == 230:
                            self.x_ss = 2
                            self.gauche = 103


                elif keys[pygame.K_RIGHT]:
                    temp = temp.move(+self.vitesse, 0)
                    self.image = self.ss.get_image(self.x_ss, self.droite, self.rect2.width, self.rect2.height)
                    self.x_ss += self.offset
                    pygame.time.delay(45)
                    self.vx =self.game.map.wall_collision(temp,'droite',self.vitesse)
                    self.rect = temp

                    if self.x_ss == 290 and self.droite == 40:
                        self.x_ss = 2
                        self.droite = 167
                    if self.x_ss == 290 and self.droite == 167:
                        self.x_ss = 2
                        self.droite = 40

                elif keys[pygame.K_UP]:
                    temp = temp.move(0, -self.vitesse)
                    self.image = self.ss.get_image(self.x_ss, self.haut, self.rect2.width, self.rect2.height)
                    self.x_ss += self.offset
                    pygame.time.delay(45)
                    self.vy = -self.game.map.wall_collision(temp, 'haut', self.vitesse)
                    self.rect = temp

                    if self.x_ss == 290 and self.haut == 8:
                            self.x_ss = 2
                            self.haut = 135
                    if self.x_ss == 290 and self.haut == 135:
                            self.x_ss = 2
                            self.haut = 8

                elif keys[pygame.K_DOWN]:
                        temp = temp.move(0, +self.vitesse)
                        self.image = self.ss.get_image(self.x_ss, self.bas, self.rect2.width, self.rect2.height)
                        self.x_ss += self.offset
                        self.vy = self.game.map.wall_collision(temp,'bas',self.vitesse)
                        pygame.time.delay(45)
                        self.rect = temp

                        if self.x_ss == 290 and self.bas == 71:
                            self.x_ss = 2
                            self.bas = 198
                        if self.x_ss == 290 and self.bas == 198:
                            self.x_ss = 2
                            self.bas = 71

                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            self.interactif = self.game.map.item_collide(self.rect , 0)
                            if isinstance(self.interactif,Coffre):
                             if (self.interactif.etats == 'Close'):
                                self.interactif.action()
                                self.converted_text = self.split_texte(self.interactif.get_text())
                                self.display = self.converted_text[0]
                                self.image = self.ss2.get_image(46, 256, 20, 24)
                                self.count = 1
                                item = self.interactif.inside
                                item.changexy((self.x+10) , (self.y-15))



        if (self.etats == 'Talk'):
            for event in events:
                 if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_1:
                                pygame.key.set_repeat(400, 50)
                                if (self.count < len(self.converted_text)):
                                        self.display = self.converted_text[self.count]
                                        self.count+=1

                                else:
                                    self.display =False
                                    self.etats = "Free"
                                    self.converted_text = False
                                    self.image = self.ss.get_image(self.x_ss, self.haut , self.width ,self.height)
                                    return True




    def split_texte(self,text):
        tab = list()
        chaine =''
        for i in range(len(text)):
            if text[i] != '|':
                chaine += text[i]
            else:
                tab.append(chaine)
                chaine=''
        tab.append(chaine)
        return tab

    def update(self,event):
        self.get_keys(event)
        self.x+= self.vx
        self.y+= self.vy
        self.rect.topleft = (self.x, self.y)



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
                if ((self.rect.y + self.rect.height) % 16 != 0):
                    rajout_ligne_y = 1
                if ((self.rect.x + self.rect.width) % 16 != 0):
                    rajout_ligne_x = 1
                for j in range(int(self.rect.height // 16 + rajout_ligne_y)):
                    self.liste_vivant[y][x] = self.name
                    for i in range(int(self.rect.width // 16 + rajout_ligne_x)):
                        self.liste_vivant[y + j][x + i] = self.name





class Monstre(Perso):
    def __init__(self, ss, droite, gauche, bas, haut, offset, width, height,  carte, WINDOW):
        Perso.__init__(self, ss, carte, WINDOW)
        self.HP_max = 8
        self.HP_Actuel = 4.5
        self.x_ss = 7
        self.droite = droite
        self.gauche = gauche
        self.bas = bas
        self.haut = haut
        self.image = self.ss.get_image(self.x_ss, self.droite, width, height)
        self.offset = offset
        self.rect = self.image.get_rect()
    def link_direction(self):
        return self.image
    def deplacer(self, direction):
            temp = self.rect.copy()
            if direction == 'haut':
                temp = temp.move(0, -self.vitesse)
                if self.carte.wall_collision(temp):
                    self.image = self.ss.get_image(self.x_ss, self.haut, self.rect.width, self.rect.height)
                    self.x_ss += self.offset
                    pygame.time.delay(45)
                else:
                    self.image = self.ss.get_image(self.x_ss, self.haut, self.rect.width, self.rect.height)
                    self.x_ss += self.offset
                    pygame.time.delay(45)
                    self.rect.y -= self.vitesse
                    self.rect = temp

                if self.x_ss > 55:
                    self.x_ss = 2
            if direction == 'droite':
                temp = temp.move(self.vitesse, 0)
                if self.carte.wall_collision(temp):
                    self.image = self.ss.get_image(self.x_ss, self.droite, self.rect.width, self.rect.height)
                    self.x_ss += self.offset
                    pygame.time.delay(45)
                else:
                    self.image = self.ss.get_image(self.x_ss, self.droite, self.rect.width, self.rect.height)
                    self.x_ss += self.offset
                    pygame.time.delay(45)
                    self.rect.x += self.vitesse
                    self.rect = temp

                if self.x_ss < 55 :
                    self.x_ss=2

            if direction == 'bas':
                temp = temp.move(0, self.vitesse)
                if self.carte.wall_collision(temp):
                    self.image = self.ss.get_image(self.x_ss, self.bas, self.rect.width, self.rect.height)
                    self.x_ss += self.offset
                    pygame.time.delay(45)
                else:
                    self.image = self.ss.get_image(self.x_ss, self.bas, self.rect.width, self.rect.height)
                    self.x_ss += self.offset
                    self.rect.y += self.vitesse
                    pygame.time.delay(45)
                    self.rect = temp

                if self.x_ss == 290 and self.bas == 71:
                    self.x_ss = 2
                    self.bas = 198
                if self.x_ss == 290 and self.bas == 198:
                    self.x_ss = 2
                    self.bas = 71
            if direction == 'gauche':
                temp = temp.move(-self.vitesse, 0)
                if self.carte.wall_collision(temp):
                    self.image = self.ss.get_image(self.x_ss, self.gauche, self.rect.width, self.rect.height)
                    self.x_ss += self.offset
                    pygame.time.delay(45)
                else:
                    self.image = self.ss.get_image(self.x_ss, self.gauche, self.rect.width, self.rect.height)
                    self.x_ss += self.offset
                    self.rect.x -= self.vitesse
                    pygame.time.delay(45)
                    self.rect = temp

                if self.x_ss == 290 and self.gauche == 103:
                    self.x_ss = 2
                    self.gauche = 230
                if self.x_ss == 290 and self.gauche == 230:
                    self.x_ss = 2
                    self.gauche = 103
            self.rect = self.rect.move(self.rect.x, self.rect.y)
