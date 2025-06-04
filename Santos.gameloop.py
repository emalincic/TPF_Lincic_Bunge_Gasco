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



# Clase Plantas
class Plants(pygame.sprite.Sprite):
    def __init__(self, image_file, pos, dims = (800, 600), cost = 50, life = 100):
        super(Plants, self).__init__()
        non_dimmed = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(non_dimmed, (80, 80))
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)
        self.cost = cost
        self.state = pygame.time.get_ticks()
        self.ready = None
        self.life = life
    def take_damage(self, damage = 0):
        if self.life <= 0: self.kill()
        else: self.life -= damage
    def remove(self): 
        self.kill()
        return int(self.cost/2)

class Sunflower(Plants):
    def __init__(self, image_file, pos, dims=(800, 600), cost=50, life = 100):
        super().__init__(image_file, pos, dims, cost, life)
    def ability(self):
        if self.ready == None:
            self.ready = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.ready >= 10000:
            fpy = self.rect.centery
            sun = SUNS.SF_sun('Images/sol.png', self.rect.center, fpy)
            soles.add(sun)
            self.ready = None

class Nut(Plants):
    def __init__(self, image_file, pos, dims=(800, 600), cost=50, life=200):
        super().__init__(image_file, pos, dims, cost, life)
    def ability(self): return None

class PeaShotter(Plants):
    def __init__(self, image_file, pos, pea_file, dims=(800, 600), cost=50, life=100):
        super().__init__(image_file, pos, dims, cost, life)
        self.pea_file = pea_file
    def ability(self):
        if self.ready == None:
            self.ready = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.ready >= 5000:
            new_pea = Pea(self.pea_file, (self.pos))
            peas.add(new_pea)
            self.ready = None

class Pea(pygame.sprite.Sprite):
    def __init__(self, image_file, pos, dims=(800, 600)):
        super(Pea, self).__init__()
        non_dimmed = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(non_dimmed, (50, 50))
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)
    def shoot(self):
        self.rect.move_ip(1, 0)


# Intizialize pygame
pygame.init()
soles = pygame.sprite.Group()
girasoles = pygame.sprite.Group()
pea_shooters = pygame.sprite.Group()
nuts = pygame.sprite.Group()
peas = pygame.sprite.Group()

def get_all_palnts():
    return girasoles.sprites() + pea_shooters.sprites() + nuts.sprites()


sunflower_cooldown = 10000
last_sunflower_placed = -sunflower_cooldown # Tratar de incorporar cooldowns en las clases??
# Game loop
run = True
sun_counter = 0
while run:
    time = pygame.time.get_ticks()
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
 
        # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
        #     if time - last_sunflower_placed >= sunflower_cooldown:
        #         new_sunflower = PeaShotter('Images/Peashooter.png', pygame.mouse.get_pos(), 'Images/Pea.png')
        #         pea_shooters.add(new_sunflower)
        #         last_sunflower_placed = time
        #     else: print("Not ready") # ACA HABRIA QUE IMPLEMENTAR LO QUE PASA EN EL COOLDOWN DE LAS PLANTAS
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                SUNS.cell_center()
                new_peashooter = PeaShotter('Images/Peashooter.png', pygame.mouse.get_pos(), 'Images/Pea.png')
                pea_shooters.add(new_peashooter)
            elif event.key == pygame.K_g:
                    new_sunflower = Sunflower('Images/Sunflower.png', pygame.mouse.get_pos())
                    girasoles.add(new_sunflower)
            elif event.key == pygame.K_n:
                new_nut = Nut('Images/Nut.png', pygame.mouse.get_pos())
                nuts.add(new_nut)



    
    soles.update()
    screen.fill((0, 0, 0))
    screen.blit(mapa.image, mapa.rect)

    for plant in get_all_palnts():
        plant.ability()
        screen.blit(plant.image, plant.rect)
    for pea in peas:
        pea.shoot()
        screen.blit(pea.image, pea.rect)
    for sol in soles:
        sol.action()
        screen.blit(sol.image, sol.rect)
    print(pygame.mouse.get_pos())
    pygame.display.update()
