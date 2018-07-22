import pygame

from pygame.locals import *
from Perso import SpriteSheet

pygame.init()
fenetre = pygame.display.set_mode((640, 480))
continuer = 1

ss = SpriteSheet('SPRITE/6369.png')
sword = ss.get_image(52, 285, 7, 21)
link_haut = ss.get_image(727, 347, 16, 24)
link_bas = ss.get_image(16, 348, 16, 24)
link_gauche = ss.get_image(388, 350, 16, 24)
link_droite = ss.get_image(388, 350, 16, 24)
link_rect = link_haut.get_rect()
sword2 = sword
rect_origine = sword.get_rect()
rect = sword2.get_rect()
i = False
i_h = -80
i_b = 100
i_g = 0
i_d = 0
j = 0
temp_rect = rect
link_rect = link_haut.get_rect()
link_rect.x = 100
link_rect.y = 100
rect.center = link_rect.center
update_2 = 0
y = 0
action = False
way = False
while continuer:
    pygame.draw.rect(fenetre, pygame.Color("white"), pygame.Rect(0, 0, 640, 480))

    now = pygame.time.get_ticks()

    sword2 = pygame.transform.rotate(sword, i)
    if (j == 35):
        i_h = -80
        i_b = 100
        i_g = 0
        i_d = 0
        j = 0
        y = 0
        action = False
        way = False
    if (action == 'hit'):
        fenetre.blit(sword2, rect)
    fenetre.blit(link_haut, link_rect)
    link_rect = link_haut.get_rect()
    link_rect.x = 100
    link_rect.y = 100
    pygame.display.flip()

    if (action != 'hit'):
        event2 = pygame.event.get()
        for event in event2:
            if event.type == pygame.QUIT:
                continuer = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    action = 'hit'
                    way = 'haut'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    action = 'hit'
                    way = 'bas'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    action = 'hit'
                    way = 'gauche'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_4:
                    action = 'hit'
                    way = 'droite'

    if (action == 'hit'):
        if (way == 'haut'):
            if (now - update_2 > 5):
                update_2 = now
                print(j)
                print('angle' + str(i))
                rect = sword2.get_rect()
                rect.center = link_rect.center
                i_h += 5
                j += 1
                link_haut = ss.get_image(727 + (j // 4 * 32), 347, 16, 24)
                if (j < 17):
                    rect.x = rect.x + 13 - (j * 0.80)
                    rect.y = rect.y - 9 - (j * 0.50)
                elif (j > 16 and j < 22):
                    rect.x = rect.x - ((j - 16) * 2)
                    rect.y = rect.y - 13
                elif (j > 21 and j < 29):
                    rect.x = rect.x - 12
                    rect.y = rect.y - 13 + (j - 21)
                elif (j > 28 and j < 35):
                    rect.x = rect.x - 12
                    rect.y = rect.y + 3

                elif (j == 35):
                    rect.x = rect.x + 13
                    rect.y = rect.y - 7

                i = i_h

        if (way == 'bas'):
            if (now - update_2 > 5):

                update_2 = now
                link_haut = ss.get_image(16 + (j // 4 * 32), 348, 16, 24)
                print(j)
                print('angle' + str(i))
                rect = sword2.get_rect()
                rect.center = link_rect.center
                i_b += 5
                j += 1
                i = i_b
                if (j > 0 and j < 18):
                    rect.x = rect.x - 11 + int(j * 0.80)
                    rect.y = rect.y + 6 + int(j * 0.45)

                elif (j > 17):
                    rect.x = rect.x - 11 + int(j * 0.80)
                    rect.y = rect.y + 2 + int(-j * 0.30 + 14)

    if (way == 'gauche'):
        if (now - update_2 > 5):
            update_2 = now
            rect = sword2.get_rect()
            rect.center = link_rect.center

            i_g += 5
            j += 1
            print(j)
            print('angle' + str(i))
            if (j > 7 and j < 12):
                y = 5
            elif (j > 15 and j < 23):
                y = 7
            elif (j > 23 and j < 27):
                y = 2
            elif (j > 27):
                y = -2
            if (j > 0 and j < 18):
                rect.x = rect.x - 6 + int(-j * 0.40)
                rect.y = rect.y - 12 + int(j * 0.70)
            elif (j > 17):
                rect.x = rect.x - 6 + int(j * 0.10 - 3)
                rect.y = rect.y - 12 + int(j * 0.60 + 2)
            i = i_g
            link_haut = ss.get_image(388 + (j // 4 * 32) - y, 350, 20, 28)
            if (j == 32):
                j = 35
    if (way == 'droite'):
        if (now - update_2 > 5):
            update_2 = now
            rect = sword2.get_rect()
            rect.center = link_rect.center
            i_g -= 5
            j += 1
            print(j)
            print('angle' + str(i))
            if (j > 7 and j < 12):
                y = 5
            elif (j > 15 and j < 23):
                y = 7
            elif (j > 23 and j < 27):
                y = 2
            elif (j > 27):
                y = -2
            if (j > 0 and j < 18):
                rect.x = rect.x + 10 + int(-j * 0.40)
                rect.y = rect.y - 12 + int(j * 0.70)
            elif (j > 17):
                rect.x = rect.x + 10 + int(j * 0.10 - 3)
                rect.y = rect.y - 12 + int(j * 0.60 + 2)
            i = i_g
            link_haut = pygame.transform.flip(ss.get_image(388 + (j // 4 * 32) - y, 350, 20, 28), 1, 0)
            if (j == 32):
                j = 35

##pygame.quit()
