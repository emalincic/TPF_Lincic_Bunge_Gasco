import pygame
COLS, ROWS = 10, 6
GAME_OVER = pygame.USEREVENT + 3
def cell_size():
    surface = pygame.display.get_surface()
    if surface is None:        
        return 0, 0
    w, h = surface.get_size()
    return w // COLS, h // ROWS

