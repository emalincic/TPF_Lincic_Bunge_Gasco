import pygame
from SUNS import cell_center

class SelectableItem(pygame.sprite.Sprite):
    def __init__(self, image, key):
        super().__init__()
        self.image = image
        self.pos = cell_center(10, 6, key)
        self.rect = self.image.get_rect(center=self.pos)
        self.key = key


class DraggingGhost(pygame.sprite.Sprite):
    def __init__(self, image, offset=(0,0)):
        super().__init__()
        self.image = image.copy()
        self.image.set_alpha(128)  # Transparente
        self.rect = self.image.get_rect()
        self.offset = offset

    def update(self, mouse_pos):
        self.rect.center = (mouse_pos[0] + self.offset[0], mouse_pos[1] + self.offset[1])

def toolbar():
    toolbar_group = pygame.sprite.Group()
    sunflower_icon = pygame.image.load('Images/Sunflower.png').convert_alpha()
    peashooter_icon = pygame.image.load('Images/Peashooter.png').convert_alpha()
    Nut_icon = pygame.image.load('Images/Nut.png').convert_alpha()
    shovel_icon = pygame.image.load('Images/pala.png').convert_alpha()
    
    sunflower_icon = pygame.transform.scale(sunflower_icon, (80, 80))
    peashooter_icon = pygame.transform.scale(peashooter_icon, (80, 80))
    Nut_icon = pygame.transform.scale(Nut_icon, (80, 80))
    shovel_icon = pygame.transform.scale(shovel_icon, (80, 80))
    
    sunflower = SelectableItem(sunflower_icon, "sunflower_icon")
    peashooter = SelectableItem(peashooter_icon, "peashooter_icon")
    nut = SelectableItem(Nut_icon, "nut_icon")
    shovel = SelectableItem(shovel_icon, "shovel_icon")

    toolbar_group.add(sunflower, peashooter, nut, shovel)
    return toolbar_group