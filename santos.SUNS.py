import random
import pygame
# Clase soles
class Suns(pygame.sprite.Sprite):
    def __init__(self, image_file, start_pos = None, fpy = None, value = 50):
        super(Suns, self).__init__()
        non_dimmed = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(non_dimmed, (80, 80)) # ACA HAY QUE INCORPORAR DIMS
        
        if start_pos == None:
            start_pos = (random.randint(82, 694), 0)
        if fpy == None:
            fpy = random.randint(114, 541)
            
        self.rect = self.image.get_rect(center=start_pos)
        self.state = True
        self.final_pos = (start_pos[0], fpy)
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

class SF_sun(Suns):
    def __init__(self, image_file, start_pos, fpy, value=50):
        super().__init__(image_file, start_pos, fpy, value)
    
