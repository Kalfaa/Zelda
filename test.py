import pygame
from pygame.locals import *
from Perso import *
from Carte import *
import time
from pytmx.util_pygame import load_pygame






class Game:
    def __init__(self):
        pygame.init()
        self.all_sprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.WINDOW = pygame.display.set_mode((450, 320))
        self.load_data()
        self.running = True
        pygame.key.set_repeat(400, 30)
        #SpriteSheet('origin.gif')
        self.debugwall = False
        self.debuglink= False
        self.event = False




        # all_sprites.add(Monstre)
    def load_data(self):
        self.sprite_coeur = list()
        self.sprite_coeur.append(pygame.image.load('SPRITE/Heart00.png').convert())
        self.sprite_coeur.append(pygame.image.load('SPRITE/Heart025.png').convert())
        self.sprite_coeur.append(pygame.image.load('SPRITE/Heart05.png').convert())
        self.sprite_coeur.append(pygame.image.load('SPRITE/Heart075.png').convert())
        self.sprite_coeur.append(pygame.image.load('SPRITE/Heart1.png').convert())
        self.map = Carte(load_pygame('Grande_map.tmx'), self.WINDOW)
        self.textbox =pygame.image.load('SPRITE/textbox2.png').convert()
        self.mob_ss = SpriteSheet('SPRITE/origin.gif')

        self.update_animation = 0
        self.map_image = self.map.make_map()
        self.map_rect = self.map_image.get_rect()
        self.link_ss =SpriteSheet('SPRITE/Link.png')
        self.link_ss2=SpriteSheet('SPRITE/6369.png')
        pygame.font.init()
        font_path = "SPRITE/ReturnofGanon.ttf"
        font_size = 32
        self.font = pygame.font.Font(font_path, font_size)
        for obj in self.sprite_coeur:
            obj.set_colorkey((255, 255, 255))


    def update(self):
        now = pygame.time.get_ticks()
        self.Link.update(self.event)
        self.monstre.update()
        self.camera.update(self.Link)

        if (self.Link.invulnerable == 0 ):
            if (pygame.sprite.collide_mask(self.Link,self.monstre)):
                self.Link.invulnerable = 1
                self.Link.prend_degat(0.5)

        else:
            time = now - self.update_animation
            print(time)
            if( time >3000):
                self.Link.invulnerable = 0
                self.update_animation = now

    def draw(self):
        self.WINDOW.blit(self.map_image, self.camera.apply_rect(self.map_rect))

        if (self.Link.etats == 'hit'):
            if (self.Link.compteur_animation == 35):
                self.Link.etats = 'Free'
                self.Link.clear_animation()
                if (self.Link.direction =='droite'):
                    self.Link.image = self.Link.ss.get_image(self.Link.x_ss, self.Link.droite, self.Link.width, self.Link.height)
                elif (self.Link.direction =='haut'):
                    self.Link.image =  self.Link.ss.get_image(self.Link.x_ss, self.Link.haut, self.Link.width, self.Link.height)
                elif (self.Link.direction =='bas'):
                    self.Link.image =self.Link.ss.get_image(self.Link.x_ss, self.Link.bas, self.Link.width, self.Link.height)
                elif (self.Link.direction =='gauche'):
                    self.Link.image =  self.Link.ss.get_image(self.Link.x_ss, self.Link.gauche, self.Link.width, self.Link.height)
            else:
                self.Link.sword_display = pygame.transform.rotate(self.Link.sword, self.Link.i)
                self.WINDOW.blit(self.Link.sword_display , self.camera.apply_rect(self.Link.sword_rect))





        if self.debugwall:
            self.debug_collision(self.map)
        for sprite in self.all_sprites:
            self.WINDOW.blit(sprite.image, self.camera.apply(sprite))
        if self.debuglink:
            pygame.draw.rect(self.WINDOW, pygame.Color('red'), self.camera.apply_rect(self.Link.rect))
            pygame.draw.rect(self.WINDOW, pygame.Color('red'), self.camera.apply_rect(self.Link.sword_rect))
            pygame.draw.rect(self.WINDOW, pygame.Color('red'), self.camera.apply_rect(self.monstre.rect))#debug link hitbox
        self.afficher_coeur()

        if (self.Link.display):
            self.Link.etats = 'Talk'
            self.WINDOW.blit(self.textbox, (30, 180))
            self.WINDOW.blit(self.Link.interactif.inside.image, self.camera.apply(self.Link.interactif.inside)) ## FAUT TROUVER UNE SOLUTION CAR CA CEST DE LA MERDE
            self.afficher_text(self.Link.display)



        pygame.display.flip()


    def heart(self, remplissage, position):
        if remplissage == 0:
            self.WINDOW.blit(self.sprite_coeur[0], (450 - (self.Link.HP_max - position) * 32, 0))
            return True
        if remplissage == 0.25:
            self.WINDOW.blit(self.sprite_coeur[1], (450 - (self.Link.HP_max - position) * 32, 0))
            return True
        if remplissage == 0.5:
            self.WINDOW.blit(self.sprite_coeur[2], (450 - (self.Link.HP_max - position) * 32, 0))
            return True
        if remplissage == 0.75:
            self.WINDOW.blit(self.sprite_coeur[3], (450 - (self.Link.HP_max - position) * 32, 0))
            return True
        if remplissage == 1:
            self.WINDOW.blit(self.sprite_coeur[4], (450 - (self.Link.HP_max - position) * 32, 0))
            return True

    def afficher_coeur(self):
        cpt = 0
        temp_HP_Actuel = self.Link.HP_Actuel
        while (self.Link.HP_max >= cpt):
            if temp_HP_Actuel > 0:
                temp_HP_Actuel -= 1
                if temp_HP_Actuel+1 > 0:
                    self.heart(1, cpt)
                if temp_HP_Actuel < 0:
                    self.heart(abs(temp_HP_Actuel), cpt)
                    temp_HP_Actuel = 0
            else:
                self.heart(0, cpt)
            cpt += 1

    def afficher_text(self,display):
        longueur_text = len(display)
        stop = 0
        # i=20
        j = 0
        i = 18
        if (longueur_text>28):


            while i < longueur_text:
                a = display[i]
                if (display[i] == ' ' and (i-stop) >23):
                    text= self.font.render(display[0+stop:i],1,(255,255,255))
                    self.WINDOW.blit(text, (45, 190+(j*30)))
                    stop = i
                    j += 1
                    i+=1
                else:
                    i+=1
        text = self.font.render(display[stop:longueur_text], 1, (255, 255, 255))
        self.WINDOW.blit(text, (45, 200+(j*30)))



    def events(self):
        self.event = pygame.event.get()
        for event in self.event:
            if event.type == KEYDOWN and event.key == K_SPACE:
                print(self.Link.x)
                print(self.Link.y)
            if  event.type == KEYDOWN and event.key == K_F12 :
                if self.debugwall == False:
                    self.debugwall = True
                else:
                    self.debugwall = False
            if event.type == KEYDOWN and event.key == K_F11:
                pygame.key.set_repeat(400, 30)
                if self.debuglink == False:
                    self.debuglink = True
                else:
                    self.debuglink = False
            if event.type == KEYDOWN and event.key == K_F10:
                self.Link.prend_degat(1)

            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def run(self):
        self.clock.tick(self.FPS)
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
    def new(self):
        self.Link = Hero(self , 255/16 , 49/16)
        self.monstre=Monstre(self, 255/16, 180/16)
        self.all_sprites.add(self.Link)
        self.all_sprites.add(self.monstre)
        self.camera = Camera(self.map.largeur*16, self.map.hauteur*16)
        self.map.afficher_tab(self.map.list_item)
        for item in self.map.item:
            self.all_sprites.add(item)

    def debug_collision(self,map):
        for obj in map.TiledElement.objects:
            if obj.name != None:
                rect = pygame.Rect(obj.x,obj.y, obj.width , obj.height )
                pygame.draw.rect(self.WINDOW , pygame.Color("green") , self.camera.apply_rect(rect))



g = Game()
g.new()
g.run()
pygame.quit()
