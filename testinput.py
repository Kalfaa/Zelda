import pygame

from pygame.locals import *
from Perso import SpriteSheet

# Initialisation de la bibliothèque Pygame

pygame.init()

# Création de la fenêtre

fenetre = pygame.display.set_mode((640, 480))

# Variable qui continue la boucle si = 1, stoppe si = 0

continuer = 1

ss = SpriteSheet('SPRITE/6369.png')
sword = ss.get_image(52, 285, 7, 21)
link = ss.get_image(727, 347, 16, 24)
link_rect = link.get_rect()

sword2 = sword
# Boucle infinie
rect_origine = sword.get_rect()
rect = sword.get_rect()
rect.centerx = 100
rect.centery = 100
i = -80
j = 0
temp_rect = rect
update = 0
action = None
update_2 = 0

while continuer:
    pygame.draw.rect(fenetre, pygame.Color("black"), pygame.Rect(0, 0, 640, 480))

    now = pygame.time.get_ticks()

    event2 = pygame.event.get()

    if (action == 'hit'):

        mask = pygame.mask.from_surface(sword2).outline()
        # pygame.draw.lines(sword2,(200,150,150),1,mask)

        link = ss.get_image(727 + j * 32, 347, 16, 24)
        link_rect = link.get_rect()
        link_rect.x = 100
        link_rect.y = 100 &

        if (now - update_2 > 15):
            sword2 = pygame.transform.rotate(sword, i)
            rect = sword2.get_rect()
            rect.center = link_rect.center
            rect.x = rect.x - 2 * j * 0.80
            rect.y -= 8 + (-j * 0.60)
            update_2 = now
            if (i < 90):
                i += 5
        fenetre.blit(sword2, rect)
        fenetre.blit(link, link_rect)
        pygame.display.flip()
        if (now - update > 85):
            j += 1
            update = now

        if (j == 10):
            j = 0
            i = -80
            action = None

    for event in event2:
        if event.type == pygame.QUIT:
            continuer = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                action = 'hit'

pygame.quit()
