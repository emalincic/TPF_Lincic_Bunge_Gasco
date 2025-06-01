import pygame
from sys import exit
from random import choice, randint
from DataBase import Zombie_types
from lawnmower import *
w = 1200
h = 800

class Zombies(pygame.sprite.Sprite):
    def __init__(self, zombie_type):
        super(Zombies, self).__init__()
        self.health = zombie_type['health']
        self.speed = zombie_type['speed']
        self.image = zombie_type['image']
        
        image = pygame.image.load(self.image).convert_alpha()
        self.surf = pygame.transform.scale(image, (100, 90))
        self.rect = self.surf.get_rect(topleft=(w, choice([205, 310, 405, 500, 505])))
        self.x = float(self.rect.x)
        
    def movement(self):
        self.x -= self.speed
        self.rect.x = int(self.x)
        if self.rect.right < 250:
            self.kill()
            
def sprites():
    ADDZOMBIE = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDZOMBIE, choice([2000, 4000, 6000]))  # Enemigos cada 500ms (medio segundo)
    zombies = pygame.sprite.Group()
    lawnmowers = add_lawnmowers()
    return zombies, ADDZOMBIE, lawnmowers
    
def game(events, zombies, screen, ADDZOMBIE, lawnmowers):
    for event in events:
        if event.type == pygame.MOUSEMOTION:
            print(event.pos)
        if event.type == ADDZOMBIE:
            random_z = choice(list(Zombie_types.keys()))
            zombie = Zombies(Zombie_types[random_z])
            zombies.add(zombie)
    for zombie in zombies:
        zombie.movement()
        screen.blit(zombie.surf, zombie.rect)
    
    
    for mower in lawnmowers:
        mower.movement(zombies)
        screen.blit(mower.image, mower.rect)