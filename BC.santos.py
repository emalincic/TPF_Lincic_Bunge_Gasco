import pygame
# Clase background
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location, dims = (800, 600)):
        pygame.sprite.Sprite.__init__(self)
        img_nodimensionado = pygame.image.load(image_file)
        self.image = pygame.transform.scale(img_nodimensionado, dims)
        self.rect = self.image.get_rect()
        self.rect.y, self.rect.x = location
