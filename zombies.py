import os
import pygame
import random
import utils as UT
from utils import GAME_OVER

pygame.mixer.init()
class Zombies(pygame.sprite.Sprite):
    def __init__(self, zombie_type, random_z: str):
        super().__init__()
        self.zombie_type = zombie_type
        self.health = zombie_type["health"]
        self.speed = zombie_type["speed"]
        self.image = os.path.join("Images", zombie_type["image"][0])
        self.max_health = zombie_type["health"]
        self.id = random.randint(0, 100000)
        self.type = random_z
        self.start_time = pygame.time.get_ticks()
        self.eating_sound = pygame.mixer.Sound(os.path.join('Audio', 'zombies eating sound.mp3'))
        self.Channel = pygame.mixer.Channel(0)
        self.eating = False
        

        raw = pygame.image.load(self.image).convert_alpha()
        c_w, c_h = UT.cell_size()
        self.surf = pygame.transform.scale(raw, (int(c_h * 1.0), int(c_h * 0.9)))

        self.cx, self.cy = UT.cell_center(10, 6, "zombie")
        self.rect = self.surf.get_rect(center=(self.cx, self.cy))
        self.x = float(self.rect.x)

    def movement(self):
        self.x -= self.speed
        self.rect.x = int(self.x)
        if self.rect.right <= 0:
            pygame.event.post(pygame.event.Event(GAME_OVER))  
            self.kill()
            
    def selfdamage(self, dmg: int = 20):
        self.health -= dmg
        if self.health <= 0:
            self.kill()
    
    def sound(self):
        if self.eating:
            self.Channel.play(self.eating_sound, loops=-1)
        else:
            self.Channel.stop()

    def ready_to_hit(self):
        if not hasattr(self, "_ready_time"):
            self._ready_time = pygame.time.get_ticks()
            return True
        if pygame.time.get_ticks() - self._ready_time >= 1500:
            self._ready_time = pygame.time.get_ticks()
            return True
        return False
    
    
class balloon(Zombies): 
    def __init__(self, zombie_type, random_z):
        super().__init__(zombie_type, random_z)
    def balloon_ability(self):
        if self.health < self.max_health * 0.4:
            self.speed = 0.35
            self.type = 'Normal'
            self.image = os.path.join("Images","Balloonzombie2.png")
            raw = pygame.image.load(self.image).convert_alpha()
            c_w, c_h = UT.cell_size()
            self.surf = pygame.transform.scale(raw, (int(c_h * 1.0), int(c_h * 0.9)))
            self.rect = self.surf.get_rect(center=(self.cx, self.cy))

def get_zombies():
    return pygame.sprite.Group()
