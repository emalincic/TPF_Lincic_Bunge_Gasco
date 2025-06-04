import random
import pygame


def cell_center(cols, rows, key, pos = None, dims=(1200, 600)):
    cell_width = dims[0] // cols
    cell_height = dims[1] // rows
    if key == 'plant': # FALTA TERMINAR
        col = pos[0] // cell_width
        row = pos[1] // cell_height
        if col == 0 or row == 0: return None
        center_x = col * cell_width + cell_width // 2
        center_y = row * cell_height + cell_height // 2
        return (center_x, center_y)
    elif key == 'sun':
        # Elegimos columnas 1 a 9 y filas 1 a 5 (ignoramos la fila y columna 0)
        first_col, last_call = 1, (cols - 2)
        first_row, last_row = 1, (rows - 1)
        col = random.randint(first_col, last_call)
        row = random.randint(first_row, last_row)
        cell_x = col * cell_width
        cell_y = row * cell_height
        cx = random.randint(cell_x, cell_x + cell_width - 1)
        cy = random.randint(cell_y, cell_y + cell_height - 1)
        return (cx, cy)
    elif key == 'lawnmower':
        col = 0
        row = pos
        cx = col * cell_width + cell_width // 2
        cy = row * cell_height + cell_height // 2
        return (cx, cy)
    elif key == 'zombie':
        col = 10
        row = random.randint(1, 6)
        
        cx = col * cell_width + cell_width // 2
        cy = row * cell_height + cell_height // 2
        return (cx, cy)
# Clase soles
class Suns(pygame.sprite.Sprite):
    def __init__(self, image_file, start_pos = None, fpy = None, dims=(1200, 600), value=50, cols = 10, rows = 6):
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

class SF_sun(Suns):
    def __init__(self, image_file, start_pos, fpy, value=50):
        super().__init__(image_file, start_pos, fpy, value)
    
