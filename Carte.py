import pygame
from pygame.locals import *
from pytmx.util_pygame import load_pygame
import pytmx
from math import *
from Interactif import *
from Item import *
from Perso import SpriteSheet

class Carte:
    def __init__(self,TiledElement,WINDOW):
        self.WINDOW= WINDOW
        self.TiledElement = TiledElement
        self.hauteur = TiledElement.height
        self.largeur = TiledElement.width
        self.liste_wall = self.__creer_tableau()
        self.list_item =self.__creer_tableau()
        self.item= list()
        self.item_ss = SpriteSheet('SPRITE/Sprite_Item.png')
        self.remplir_tableau()

    def __creer_tableau(self):
        l = []
        for i in range(self.hauteur):
            l.append([0] * self.largeur)
        return l


    def afficher_tab(self,liste):
        for i in range(len(liste)):
            print(liste[i])

    def ajouter_obstacle(self,Rect):
        ##if (Rect.y+Rect.height >self.hauteur*16):
            ##raise ('Hauteur plus grande que la carte ' )
        ##if (Rect.y+Rect.width >self.largeur*16):
            ##raise ('Largeur plus grande que la carte')
        x = int(Rect.x)//16
        y = int(Rect.y)//16
        width = ceil(Rect.width)
        height = ceil(Rect.height)
        self.liste_wall[y][x] = Rect.name
        rajout_ligne_y=0
        rajout_ligne_x = 0
        if ((Rect.y+Rect.height)%16 !=0):
            rajout_ligne_y = 1
        if ((Rect.x + Rect.width) % 16 != 0):
            rajout_ligne_x = 1
        for j in range (ceil(height/16+rajout_ligne_y)):
            self.liste_wall[y][x] = Obstacle(Rect)
            for i in range(ceil(width / 16+rajout_ligne_x)):
                self.liste_wall[y+j][x+i] = self.liste_wall[y][x]
                self.liste_wall[y+j][x+i+1] = self.liste_wall[y][x]
    def ajouter_item(self,Rect ,item):
        x = int(Rect.x) // 16
        y = int(Rect.y) // 16
        width = ceil(Rect.width)
        height = ceil(Rect.height)
        self.list_item[y][x] = Rect.name
        rajout_ligne_y = 0
        rajout_ligne_x = 0
        if ((Rect.y + Rect.height) % 16 != 0):
            rajout_ligne_y = 1
        if ((Rect.x + Rect.width) % 16 != 0):
            rajout_ligne_x = 1
        for j in range(ceil(height / 16 + rajout_ligne_y)):
            self.list_item[y][x] = item
            for i in range(ceil(width / 16 + rajout_ligne_x)):
                self.list_item[y + j][x + i] = self.list_item[y][x]
                self.list_item[y + j][x + i + 1] = self.list_item[y][x]

    def remplir_tableau(self):
        for obj in self.TiledElement.objects:
            print (obj.name,obj.x , obj.y)

            if obj.name != None:
                self.ajouter_obstacle(obj)
        for obj in self.TiledElement.get_layer_by_name('Coffre'):
            item =Coffre(obj,pygame.image.load('SPRITE/chest.png'),Item('Sword' ,self.item_ss.get_image(9,9, 14, 14) ))
            self.ajouter_item(item.obj ,item)
            self.item.append(item)

    def afficher_carte(self,surface):
            ti = self.TiledElement.get_tile_image_by_gid
            for layer in self.TiledElement.visible_layers:
                if isinstance(layer, pytmx.TiledTileLayer):
                    for x, y, gid, in layer:
                        tile = ti(gid)
                        if tile:
                            surface.blit(tile, (x * 16,
                                                y * 16))
    def make_map(self):
        temp_surface= pygame.Surface((self.largeur*16,self.hauteur*16))
        self.afficher_carte(temp_surface)
        return temp_surface

    def wall_collision(self ,  Rect1 ,direction= 0,vitesse= 5 ):
            wallcollide = 0
            list_coin = list()
            posy = Rect1.y
            posx = Rect1.x
            WALL_HG = self.liste_wall[(posy) // 16][posx // 16]  #Haut Gauche
            WALL_HD = self.liste_wall[(posy) // 16][(posx+Rect1.width) // 16] #Haut Droite
            if ((posx + Rect1.width) - (posx))>16:
                WALL_HGHD= self.liste_wall[(posy) // 16][(posx+Rect1.width-16) // 16]
                list_coin.append(WALL_HGHD)
            if ((posy+Rect1.height) - (posy))>16:
                WALL_BDHD = self.liste_wall[((posy+Rect1.height)-16) // 16][(posx+Rect1.width) // 16]
                list_coin.append(WALL_BDHD)
            if (posy+Rect1.height - (posy))>16:
                WALL_HGBG= self.liste_wall[((posy+Rect1.height)-16) // 16][(posx) // 16]
                list_coin.append(WALL_HGBG)
            WALL_BG = self.liste_wall[(posy+Rect1.height) // 16][(posx) // 16] #Bas Gauche
            WALL_BD = self.liste_wall[(posy+Rect1.height) // 16][(posx+Rect1.width) // 16]#Bas droite
            if ((posx+Rect1.width)-posx) >16:
                WALL_BDBG=self.liste_wall[(posy+Rect1.height) // 16][((posx+Rect1.width)-16) // 16]
                list_coin.append(WALL_BDBG)
            list_coin.append(WALL_HG)
            list_coin.append(WALL_HD)
            list_coin.append(WALL_BG)
            list_coin.append(WALL_BD)
            for Wall in list_coin:
                if Wall != 0:
                    #wallhitbox = pygame.Rect(Wall.x, Wall.y, Wall.width, Wall.height)
                    wallcollide = Rect1.colliderect(Wall)
                if wallcollide == True:
                    if direction=='droite':
                        Rect1= Rect1.move(-vitesse, 0)
                        espace = Wall.x- (Rect1.x+Rect1.width)
                        print(espace)
                        return espace
                    if direction == 'haut':
                        Rect1= Rect1.move(0,+vitesse)
                        espace =  (Rect1.y) -(Wall.y+Wall.height)
                        print(espace)
                        return espace
                    if direction == 'gauche':
                        Rect1 = Rect1.move(+vitesse,0)
                        espace = (Rect1.x) - (Wall.x+Wall.width)
                        print(espace)
                        return espace
                    if direction =='bas':
                        Rect1 = Rect1.move(0, -vitesse)
                        espace = (Wall.y) - (Rect1.y+Rect1.height)
                        print(espace)
                        return espace
            return vitesse
    def item_collide(self,Rect,direction):
        posy = Rect.y
        posx = Rect.x
        WALL_H = self.list_item[((posy) // 16)-1][int((posx +Rect.width/2)//16)]
        if WALL_H != 0 :
            Rect = Rect.move(0, -5)
            if Rect.colliderect(WALL_H):
                return WALL_H
            else:
                return False
        else:
            return False







class Obstacle(pygame.Rect):
    def __init__(self,Rect):
        self.name= Rect.name
        self.y = Rect.y
        self.x = Rect.x
        self.height = Rect.height
        self.width  = Rect.width
        self.rotation =Rect.rotation
class Camera:
    def __init__(self,width,height):
        self.camera = pygame.Rect(0,0,width,height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    def apply_rect(self,rect):
        return rect.move(self.camera.topleft)
    def update(self , target):
        x = -target.rect.centerx+int(450/2)
        y = -target.rect.centery+int(320/2)
        x=min(0,x)
        y=min(0,y)
        x = max(-(self.width - 450),x)
        y = max(-(self.height - 320 ),y)
        self.camera = pygame.Rect(x, y, self.width, self.height)
#map = Carte(load_pygame('sans-titre.tmx'),WINDOW)

#map.afficher_tab()
#map.afficher_carte()
#pygame.display.flip()
##while 1:
   ## for event in pygame.event.get():
      ##if event.type == KEYDOWN :
        ##if event.key == K_ESCAPE:
            ##pygame.quit()