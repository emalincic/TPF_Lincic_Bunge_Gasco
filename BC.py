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