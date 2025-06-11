import pygame
from SUNS import cell_center
import os

class DraggingGhost(pygame.sprite.Sprite):
    def __init__(self, image, key):
        super().__init__()
        self.image = image
        self.image.set_alpha(128)
        self.pos = cell_center(10, 6, key)
        self.rect = self.image.get_rect(center=self.pos)
        self.key = key


class SelectableItem(pygame.sprite.Sprite):
    def __init__(self, image, key):
        super().__init__()
        self.image = image
        self.pos = cell_center(10, 6, key)
        self.rect = self.image.get_rect(center=self.pos)
        self.key = key


def toolbar():
    toolbar_group = pygame.sprite.Group()
    
    SF = pygame.image.load(os.path.join('Images','SF_seedpacket.png')).convert_alpha()
    SF_seedpacket = pygame.transform.scale(SF, (115, 90))
    PS = pygame.image.load(os.path.join('Images','PS_seedpacket.png')).convert_alpha()
    PS_seedpacket = pygame.transform.scale(PS, (115, 90))
    NT = pygame.image.load(os.path.join('Images','NT_seedpacket.png')).convert_alpha()
    NT_seedpacket = pygame.transform.scale(NT, (115, 90))
    SH = pygame.image.load(os.path.join('Images','SH_seedpacket.png')).convert_alpha()
    SH_seedpacket = pygame.transform.scale(SH, (115, 90))
    SC = pygame.image.load(os.path.join('Images','SC_seedpacket.png')).convert_alpha()
    SC_seedpacket = pygame.transform.scale(SC, (225, 165))

    
    
    SF_seedpacket = SelectableItem(SF_seedpacket, 'sunflower_icon')
    PS_seedpacket = SelectableItem(PS_seedpacket, 'peashooter_icon')
    NT_seedpacket = SelectableItem(NT_seedpacket, 'nut_icon')
    SH_seedpacket = SelectableItem(SH_seedpacket, 'shovel_icon')
    SC_seedpacket = SelectableItem(SC_seedpacket, 'suncounter_icon')
    
    toolbar_group.add(SF_seedpacket, PS_seedpacket, NT_seedpacket, SH_seedpacket, SC_seedpacket)
    
    toolbar_group_ghost = pygame.sprite.Group()
    
    sunflower = pygame.image.load('Images/Sunflower.png').convert_alpha()
    sunflower_icon = pygame.transform.scale(sunflower, (100, 90))
    peashooter = pygame.image.load('Images/Peashooter.png').convert_alpha()
    peashooter_icon = pygame.transform.scale(peashooter, (100, 90))
    Nut = pygame.image.load('Images/Nut.png').convert_alpha()
    Nut_icon = pygame.transform.scale(Nut, (100, 90))
    shovel = pygame.image.load('Images/shovel_ghost.png').convert_alpha()
    shovel_icon = pygame.transform.scale(shovel, (100, 90))
    
    sunflower = DraggingGhost(sunflower_icon, "sunflower_icon")
    peashooter = DraggingGhost(peashooter_icon, "peashooter_icon")
    nut = DraggingGhost(Nut_icon, "nut_icon")
    shovel = DraggingGhost(shovel_icon, "shovel_icon")

    toolbar_group_ghost.add(sunflower, peashooter, nut, shovel)
    return toolbar_group, toolbar_group_ghost

