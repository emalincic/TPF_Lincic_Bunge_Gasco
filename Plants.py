import pygame
import zombies
import SUNS

# Clase Plantas
class Plants(pygame.sprite.Sprite):
    def __init__(self, image_file, pos, cost = 50, life = 300):
        super(Plants, self).__init__()
        non_dimmed = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(non_dimmed, (100, 90))
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
    def __init__(self, image_file, pos, cost=50, life = 300):
        super().__init__(image_file, pos, cost, life)
    def ability(self, zombis):
        if self.ready == None:
            self.ready = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.ready >= 10000:
            fpy = self.rect.centery
            sun = SUNS.SF_sun('Images/sol.png', self.rect.center, fpy)
            self.ready = None
            return (sun, 'sunflower')
        return (None, None)
        

class Nut(Plants):
    def __init__(self, image_file, pos, cost=50, life=4000):
        super().__init__(image_file, pos, cost, life)
    def ability(self, zombies): return (None, None)

class PeaShotter(Plants):
    def __init__(self, image_file, pos, pea_file, cost=50, life=300):
        super().__init__(image_file, pos, cost, life)
        self.pea_file = pea_file
    def ability(self, zombies):
        if not any(z.cy == self.pos[1] for z in zombies):
            return (None, None)
        if self.ready == None:
            self.ready = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.ready >= 1400:
            new_pea = Pea(self.pea_file, (self.pos))
           # peas_group.add(new_pea)
            self.ready = None
            return (new_pea, 'peashotter')
        return (None, None)

class Pea(pygame.sprite.Sprite):
    def __init__(self, image_file, pos):
        super(Pea, self).__init__()
        non_dimmed = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(non_dimmed, (35, 35))
        self.x, self.y = pos
        self.rect = self.image.get_rect(center=(self.x, self.y-20))
    def shoot(self):
        self.rect.move_ip(2, 0)


