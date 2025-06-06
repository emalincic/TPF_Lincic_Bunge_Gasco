import pygame
from sys import exit
from random import choices, choice
from DataBase import Zombie_types
from lawnmower import *
from SUNS import cell_center


class Zombies(pygame.sprite.Sprite):
    def __init__(self, zombie_type, random_z):
        super(Zombies, self).__init__()
        self.zombie_type = zombie_type
        self.health = zombie_type['health']
        self.speed = zombie_type['speed']
        self.image = zombie_type['image'][0]
        self.probability = zombie_type['probability']
        self.max_health = zombie_type['health']
        self.hability = None
        self.ready = None
        self.type = random_z
        
        if Zombie_types.get('ability') is not None:
            hability_class = globals()[self.zombie_type["habilidad"]]
            self.hability = hability_class(self)
        
        
        
        image = pygame.image.load(self.image).convert_alpha()
        self.surf = pygame.transform.scale(image, (100, 90))
        
        
        self.cx, self.cy = cell_center(10, 6, 'zombie')
        
        # REVISAR, PROBLEMA DE TERMINADO DE JUEGO
        self.rect = self.surf.get_rect(center=(self.cx, self.cy))
        self.x = float(self.rect.x)
        
    def movement(self):
        self.x -= self.speed
        self.rect.x = int(self.x)
        # Corregir
        if self.rect.right <= 0:
            self.kill()
            print("¡Zombie cruzó! Fin del juego.") # ACA HAY UN PROBLEMA!! ZOMBI SALTA TODO EL TABLERO
            pygame.quit()
            exit()
    def selfdamage(self, damage=20):
        self.health -= damage
        if self.health < self.max_health*0.4:
            try:
                self.image = self.zombie_type['image'][1]
            except:
                self.image = self.zombie_type['image'][0]
            image = pygame.image.load(self.image).convert_alpha()
            self.surf = pygame.transform.scale(image, (100, 90))
            self.rect = self.surf.get_rect(center=(self.cx, self.cy))
            self.speed = 0.5
        if self.health <= 0:
            self.kill()
    def ready_to_hit(self):
        if self.ready == None:
            self.ready = pygame.time.get_ticks()
            return True
        elif pygame.time.get_ticks() - self.ready >= 1500:
            self.ready = pygame.time.get_ticks()
            return True
        return False

    def balloon_ability(self):
        if self.type == 'balloon' and self.health < self.max_health*0.4: 
            return False
        return True
    
