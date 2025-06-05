import pygame
from SUNS import cell_center

class SelectableItem(pygame.sprite.Sprite):
    def __init__(self, image, key):
        super().__init__()
        self.image = image
        self.pos = cell_center(10, 6, key)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.id = key


class DraggingGhost(pygame.sprite.Sprite):
    def __init__(self, image, offset=(0,0)):
        super().__init__()
        self.image = image.copy()
        self.image.set_alpha(128)  # Transparente
        self.rect = self.image.get_rect()
        self.offset = offset

    def update(self, mouse_pos):
        self.rect.center = (mouse_pos[0] + self.offset[0], mouse_pos[1] + self.offset[1])

