import pygame
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