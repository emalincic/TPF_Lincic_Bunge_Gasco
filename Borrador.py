import pygame
import random
import BC
import SUNS
from pygame.locals import (RLEACCEL)

# Creamos Pagina
dims = (800, 600)
screen = pygame.display.set_mode(dims)
pygame.display.set_caption('Plants vs Zombies')

# Creamos el mapa segun la imagen
mapa = BC.Background('Images/mapa.jpg', [0, 0], dims)

# Sun Frequency
SUN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SUN_EVENT, 5000)

# Clase lawmmower
class Lawmnmower(pygame.sprite.Sprite):
    def __init__(self, image_file, dims = (800, 600)):
        super(Lawmnmower, self).__init__()
        non_dimmed = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(non_dimmed, (45, 45))


# Intizialize pygame
pygame.init()

soles = pygame.sprite.Group()



# Game loop
run = True
sun_counter = 0
while run:
    # manejo de evento
    for event in pygame.event.get():
        # quit
        if event.type == pygame.QUIT:
            run = False
        elif event.type == SUN_EVENT:
            new_sun = SUNS.Suns('Images/sol.png')
            soles.add(new_sun) 
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for sol in soles:
                if sol.rect.collidepoint(event.pos): 
                    sun_counter += sol.grab()


    soles.update()
    screen.fill((0, 0, 0))
    screen.blit(mapa.image, mapa.rect)
    for sol in soles:
        sol.action()
        screen.blit(sol.image, sol.rect)
    #print(pygame.mouse.get_pos())
    print(sun_counter)
    pygame.display.update()
