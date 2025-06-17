import pygame
from random import randint
COLS, ROWS = 10, 6
GAME_OVER = pygame.USEREVENT + 3
SEED_COOLDOWN = 5_000  
def cell_size():
    surface = pygame.display.get_surface()
    if surface is None:        
        return 0, 0
    w, h = surface.get_size()
    return w // COLS, h // ROWS
# Clase background
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location, screen):
        super().__init__()
        self.screen  = screen
        self.source  = image_file
        self.location = location
        self.update_image()                       # ← primera carga

    def update_image(self):
        w, h = self.screen.get_size()
        raw   = pygame.image.load(self.source).convert()
        self.image = pygame.transform.scale(raw, (w, h))
        self.rect  = self.image.get_rect(topleft=self.location)

# Estilo del mouse:
def mouses(mouse_open, mouse_clicked):
    cursor_opended = pygame.image.load(mouse_open).convert_alpha()
    cursor_opended = pygame.transform.scale(cursor_opended, (40, 40))

    cursor_pressed = pygame.image.load(mouse_clicked).convert_alpha()
    cursor_pressed = pygame.transform.scale(cursor_pressed, (40, 40))

    mouse_opened = pygame.cursors.Cursor((0, 0), cursor_opended)
    mouse_pressed = pygame.cursors.Cursor((0, 0), cursor_pressed)
    return mouse_opened, mouse_pressed

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
    elif key == 'cherry_range':
        cx, cy = pos
        # Explota en 3x3 celdas alrededor del centro (incluyendo la celda donde está la cereza)
        left = cx - cell_width // 2 - cell_width
        top = cy - cell_height // 2 - cell_height
        width = cell_width * 3
        height = cell_height * 3
        return pygame.Rect(left, top, width, height)  
    elif key == 'boomerang_range':
        col = 9
        row = pos // cell_width
        return (col * cell_width + cell_width // 2, row)
    elif key == 'belt_icon':
        row = 0
        col = 1
        cx = col * cell_width + cell_width // 2
        cy = row * cell_height + cell_height // 2
        return (cx, cy)   
    elif key == 'belt_nut_icon':
        row = 0
        col = 0
        cx = col * cell_width + cell_width // 2
        cy = row * cell_height + cell_height // 2
        return (cx, cy)