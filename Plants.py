import pygame
from utils import cell_size
import SUNS

class Plants(pygame.sprite.Sprite):
    def __init__(self, image_file, pos, cost=50, life=300):
        super().__init__()
        cw, ch = cell_size()
        raw = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(raw, (cw, ch))
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)
        self.cost = cost
        self.state = pygame.time.get_ticks()
        self.ready = None
        self.life = life
    def take_damage(self, damage=0):
        if self.life <= 0:
            self.kill()
        else:
            self.life -= damage
    def remove(self):
        self.kill()
        return int(self.cost / 2)

class Sunflower(Plants):
    def __init__(self, image_file, pos, cost=50, life=300):
        super().__init__(image_file, pos, cost, life)
    def ability(self, zombies):
        if self.ready is None:
            self.ready = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.ready >= 10000:
            sun = SUNS.SF_sun('Images/sol.png', self.rect.center, self.rect.centery)
            self.ready = None
            return sun, 'sunflower'
        return None, None

class Nut(Plants):
    def __init__(self, image_file, pos, cost=50, life=4000):
        super().__init__(image_file, pos, cost, life)
    def ability(self, zombies):
        return None, None

class Boomerang(Plants):
    def __init__(self, image_file, pos, boomerang_file, cost=175, life=300):
        super().__init__(image_file, pos, cost, life)
        self.boomerang_file = boomerang_file
    def ability(self, zombies):
        if not any(z.cy == self.pos[1] for z in zombies):
            return None, None
        if self.ready is None:
            self.ready = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.ready >= 1400:
            new_boomerang = Boomerang_Bullet(self.boomerang_file, self.pos)
            self.ready = None
            return new_boomerang, 'boomerang'
        return None, None

class Boomerang_Bullet(pygame.sprite.Sprite):
    def __init__(self, image_file, pos):
        super().__init__()
        cw, ch = cell_size()
        raw = pygame.image.load(image_file).convert_alpha()
        size = int(ch * 0.4)
        self.image = pygame.transform.scale(raw, (size, size))
        self.x, self.y = pos
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speed = max(6, cw // 20)

        self.original = pos
        self.final = SUNS.cell_center(10, 6, 'boomerang_range', self.original[1])
        self.foward = True
        self.backward = False
        self.already_hit_zombies = set()
    def shoot(self):
        if self.foward:
            self.rect.move_ip(2, 0)
            if self.rect.centerx == self.final[0]:
                self.foward = False
                self.backward = True
                self.already_hit_zombies = set()
        elif self.backward:
            self.rect.move_ip(-2, 0)
            if self.rect.centerx == self.original[0]:
                self.kill()

class PeaShotter(Plants):
    def __init__(self, image_file, pos, pea_file, cost=100, life=300):
        super().__init__(image_file, pos, cost, life)
        self.pea_file = pea_file
    def ability(self, zombies):
        if not any(z.cy == self.pos[1] for z in zombies):
            return None, None
        if self.ready is None:
            self.ready = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.ready >= 1400:
            new_pea = Pea(self.pea_file, self.pos)
            self.ready = None
            return new_pea, 'peashotter'
        return None, None
    

class Pea(pygame.sprite.Sprite):
    def __init__(self, image_file, pos):
        super().__init__()
        cw, ch = cell_size()
        raw = pygame.image.load(image_file).convert_alpha()
        size = int(ch * 0.4)
        self.image = pygame.transform.scale(raw, (size, size))
        self.x, self.y = pos
        self.rect = self.image.get_rect(center=(self.x, self.y - int(ch * 0.25)))
        self.speed = max(6, cw // 20)
    def shoot(self):
        self.rect.move_ip(2, 0)

class Spinning_Nut(Plants):
    def __init__(self, image_file, pos, cost=None, life=None):
        super().__init__(image_file, pos, cost, life)
        self.speed = 8
        cw, ch = cell_size()
        self.image = pygame.transform.scale(raw, (cw, ch))
        self.original_image = pygame.transform.scale(raw, (cw, ch))
        raw = pygame.image.load(image_file).convert_alpha()
        self.rect = self.image.get_rect(midright=pos)
        self.rotation = 0
    def ability(self):
        self.rotation += 1
        self.image = pygame.transform.rotate(self.original_image, self.rotation)

class cherry(Plants):
    def __init__(self, image_file, pos, cost=200, life=10):
        super().__init__(image_file, pos, cost, life)
    def ability(self, zombies):
        explosion_range = SUNS.cell_center(10, 6, 'cherry_range', self.pos)
        for zombie in zombies:
            if explosion_range.colliderect(zombie.rect):
                zombie.kill()
        self.kill()
        return None, None

class Papapum(Plants):
    def __init__(self, image_file_loading, image_file_ready, pos, cost=25, life=50):
        super().__init__(image_file_loading, pos, cost, life)
        self.image_file_ready = image_file_ready
        self.transformed = False
    def ability(self, zombies):
        if self.ready is None:
            self.ready = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.ready >= 10000:
            if not self.transformed:
                self.image = self.image_file_ready
                raw = pygame.image.load(self.image).convert_alpha()
                c_w, c_h = cell_size()
                self.image = pygame.transform.scale(raw, (int(c_h * 1.0), int(c_h * 0.9)))
                self.rect = self.image.get_rect(center=self.pos)
                self.transformed = True
                self.life = 1000
            for zombie in zombies:
                if self.rect.collidepoint(zombie.rect.center) and zombie.type != 'balloon':
                    zombie.kill()
                    self.kill()
        return None, None

