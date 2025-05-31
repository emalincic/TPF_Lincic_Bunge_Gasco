import random
import pygame
# Clase soles
class Suns(pygame.sprite.Sprite):
    def __init__(self, image_file, dims = (800, 600), value = 50):
        super(Suns, self).__init__()
        non_dimmed = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(non_dimmed, (80, 80)) # ACA HAY QUE INCORPORAR DIMS

        column = random.randint(82, 694)
        self.rect = self.image.get_rect(center=(column, 0))
        self.state = True
        self.final_pos = (column, random.randint(115, 541))
        self.value = value
        self.time = None

    def action(self):
        if self.rect.center == self.final_pos:
            if self.time == None: self.time = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - self.time >= 10000: self.kill()
            self.state = False
        elif self.state:
            self.rect.move_ip((0, 1))
    
    def grab(self):
        self.kill()
        return self.value


class Plants(pygame.sprite.Sprite):
    def __init__(self, imgae_file, start_position, dims = (800, 600), cost = 50):
        super(Plants, self).__init__()
        non_dimmed = pygame.image.load(imgae_file).convert_alpha()
        self.image = pygame.transform.scale(non_dimmed, (80, 80))
        self.pos = start_position
        self.rect = self.image.get_rect(center=start_position)
        self.cost = cost
        self.state = True

