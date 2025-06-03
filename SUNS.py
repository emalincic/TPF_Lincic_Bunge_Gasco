import random
import pygame

def cell_center(cols, rows, key, pos = None, dims=(1200, 600)):
    if key == 'plant':
        cell_width = dims[0] // cols
        cell_height = dims[1] // rows
        col = pos[0] // cell_width
        row = pos[1] // cell_height

        center_x = col * cell_width + cell_width // 2
        center_y = row * cell_height + cell_height // 2
        return (center_x, center_y)
    elif key == 'sun':
        cell_width = dims[0] // cols
        cell_height = dims[1] // rows
        # Elegimos columnas 1 a 9 y filas 1 a 5 (ignoramos la fila y columna 0)
        col = random.randint(1, cols - 1)   # 1 a 9
        row = random.randint(1, rows - 1)   # 1 a 5


    

# Clase soles
class Suns(pygame.sprite.Sprite):
    def __init__(self, image_file, dims=(1200, 600), value=50):
        super(Suns, self).__init__()
        non_dimmed = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(non_dimmed, (80, 80))

        # Tamaño de la grilla (10x6)
        cols = 10
        rows = 6
        cell_width = dims[0] // cols
        cell_height = dims[1] // rows

        # Elegimos columnas 1 a 9 y filas 1 a 5 (ignoramos la fila y columna 0)
        col = random.randint(1, cols - 1)   # 1 a 9
        row = random.randint(1, rows - 1)   # 1 a 5

        # Coordenadas del centro de la celda elegida
        center_x = col * cell_width + cell_width // 2
        start_y = 0  # Empieza arriba
        end_y = row * cell_height + cell_height // 2  # Final en el centro de la celda

        self.rect = self.image.get_rect(center=(center_x, start_y))
        self.final_pos = (center_x, end_y)

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
    
