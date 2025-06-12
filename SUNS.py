from random import randint
from utils import cell_size;
import pygame


def cell_center(cols, rows, key, pos=None):
    # ← llamamos cada vez
    cell_width, cell_height = cell_size()

    if key == 'plant': #Falta terminar
        col = pos[0] // cell_width
        row = pos[1] // cell_height
        if col == 0 or row == 0:
            return None
        return (col * cell_width + cell_width // 2,
                row * cell_height + cell_height // 2)

    elif key == 'sun':
        col = randint(1, cols - 2)
        row = randint(1, rows - 1)
        cell_x = col * cell_width
        cell_y = row * cell_height
        return (randint(cell_x, cell_x + cell_width - 1),
                randint(cell_y, cell_y + cell_height - 1))

    elif key == 'lawnmower':
        row = pos
        return (cell_width // 2,
                row * cell_height + cell_height // 2)

    elif key == 'zombie':
        row = randint(1, rows - 1)
        screen_w = pygame.display.get_surface().get_width()
        return (screen_w + 50,
                row * cell_height + cell_height // 2)

    elif key == 'shovel_icon':
        col = 9
        row = 0
        cx = col * cell_width + cell_width // 2
        cy = row * cell_height + cell_height // 2
        return (cx, cy)
    elif key == 'sunflower_icon':
        col = 2
        row = 0
        cx = col * cell_width + cell_width // 2
        cy = row * cell_height + cell_height // 2
        return (cx, cy)
    elif key == 'peashooter_icon':
        col = 3
        row = 0
        cx = col * cell_width + cell_width // 2
        cy = row * cell_height + cell_height // 2
        return (cx, cy)
    elif key == 'nut_icon':
        col = 4
        row = 0
        cx = col * cell_width + cell_width // 2
        cy = row * cell_height + cell_height // 2
        return (cx, cy)
    elif key == 'suncounter_icon':
        row = 0
        col = 0.5
        cx = col * cell_width + cell_width // 2
        cy = row * cell_height + cell_height // 2
        return (cx, cy)        
# Clase soles
class Suns(pygame.sprite.Sprite):
    def __init__(self, image_file, start_pos = None, fpy = None, value=50, cols = 10, rows = 6):
        super(Suns, self).__init__()
        non_dimmed = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(non_dimmed, (80, 80))
        if fpy == None or start_pos == None:
            final_pos = cell_center(cols, rows, 'sun', None)
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

# class Sun_Counter(pygame.sprite.Sprite):
#         def __init__(self, image_file, pos):
#             super(Sun_Counter, self).__init__()
#             non_dimmed = pygame.image.load(image_file).convert_alpha()
#             self.image = pygame.transform.scale(non_dimmed, (110, 110))
#             self.pos = pos
#             self.rect = self.image.get_rect(center=pos)

class SF_sun(Suns):
    def __init__(self, image_file, start_pos, fpy, value=50):
        super().__init__(image_file, start_pos, fpy, value)


