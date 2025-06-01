import pygame
from sys import exit
from random import choices, choice
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
        self.probability = zombie_type['probability']
        self.hability = None
        
        if Zombie_types.get('hability') is not None:
            hability_class = globals()[self.zombie_type["habilidad"]]
            self.hability = hability_class(self)
        
        
        
        image = pygame.image.load(self.image).convert_alpha()
        self.surf = pygame.transform.scale(image, (100, 90))
        self.rect = self.surf.get_rect(topleft=(w, choice([205, 310, 405, 500, 505])))
        self.x = float(self.rect.x)
        
    def movement(self):
        self.x -= self.speed
        self.rect.x = int(self.x)
        if self.rect.right < 250:
            self.kill()
            pygame.quit()
            exit()
    def selfdamage(self, damage=50):
        self.health -= damage
        if self.health <= 0:
            self.kill()
def sprites():
    ADDZOMBIE = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDZOMBIE, choice([3000, 5000, 6000]))
    zombies = pygame.sprite.Group()
    lawnmowers = add_lawnmowers()
    return zombies, ADDZOMBIE, lawnmowers
    
def game(events, zombies, screen, ADDZOMBIE, lawnmowers):
    for event in events:
        # if event.type == pygame.MOUSEMOTION:
        #     print(event.pos)
        if event.type == pygame.MOUSEBUTTONUP:
            for zombie in zombies:
                if zombie.rect.collidepoint(event.pos):
                    zombie.selfdamage()
            
        if event.type == ADDZOMBIE:
            random_z = choices(list(Zombie_types.keys()), weights=[k['probability'] for k in Zombie_types.values()])[0]
            zombie = Zombies(Zombie_types[random_z])
            zombies.add(zombie)
    for zombie in zombies:
        zombie.movement()
        screen.blit(zombie.surf, zombie.rect)
            
    
    
    for mower in lawnmowers:
        mower.movement(zombies)
        screen.blit(mower.image, mower.rect)
        
    