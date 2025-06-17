import pygame
from random import randint
import utils as UT

# Clase soles
class Suns(pygame.sprite.Sprite):
    def __init__(self, image_file, start_pos = None, fpy = None, value=50, cols = 10, rows = 6):
        super(Suns, self).__init__()
        non_dimmed = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(non_dimmed, (80, 80))
        if fpy == None or start_pos == None:
            final_pos = UT.cell_center(cols, rows, 'sun', None)
            self.rect = self.image.get_rect(center=(final_pos[0], 0))
            self.final_pos = (final_pos[0], final_pos[1])
        else:
            self.rect = self.image.get_rect(center=(start_pos))
            self.final_pos = (start_pos[0], start_pos[1])

        self.state = True
        self.value = value
        self.time = None
    def action(self):
        if self.rect.center == self.final_pos:
            if self.time is None:
                self.time = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - self.time >= 10000:
                self.kill()
            self.state = False
        elif self.state:
            self.rect.move_ip((0, 1))

    def grab(self):
        self.kill()
        return self.value

class SF_sun(Suns):
    def __init__(self, image_file, start_pos, fpy, value=50):
        super().__init__(image_file, start_pos, fpy, value)


