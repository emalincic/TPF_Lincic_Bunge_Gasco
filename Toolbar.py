import os
import pygame
import utils as UT
import SUNS as SN


class DraggingGhost(pygame.sprite.Sprite):
    

    def __init__(self, image: pygame.Surface, key: str):
        super().__init__()
        self.image = image.copy()
        self.image.set_alpha(128)  
        self.rect = self.image.get_rect(center=SN.cell_center(10, 6, key))
        self.key = key


class SelectableItem(pygame.sprite.Sprite):

    def __init__(self, image: pygame.Surface, key: str):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=SN.cell_center(10, 6, key))
        self.key = key
        
    def item_in_belt(self):
        self.rect.x += 8




def _load_scaled(filename: str, size: tuple[int, int]) -> pygame.Surface:
    path = os.path.join("Images", filename)
    surf = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(surf, size)


def toolbar() -> tuple[pygame.sprite.Group, pygame.sprite.Group]:

    cols, rows = 10, 6  # rejilla lógica
    cell_w, cell_h = UT.cell_size()

    
    seed_size = (int(cell_h * 1.10), int(cell_h))       # paquetes
    icon_size = (int(cell_h * 0.70), int(cell_h * 0.80))  # iconos "fantasma"
    counter_size = (int(cell_h * 2.25), int(cell_h * 1.50))

    toolbar_group = pygame.sprite.Group()
    toolbar_group_ghost = pygame.sprite.Group()


    for seed_file, key, icon_file in [
        ("SF_seedpacket.png", "sunflower_icon", "Sunflower.png"),
        ("PS_seedpacket.png", "peashooter_icon", "Peashooter.png"),
        ("NT_seedpacket.png", "nut_icon", "Nut.png"),
        ("SH_seedpacket.png", "shovel_icon", "shovel_ghost.png"),
    ]:
        seed_img = _load_scaled(seed_file, seed_size)
        toolbar_group.add(SelectableItem(seed_img, key))

        icon_img = _load_scaled(icon_file, icon_size)
        toolbar_group_ghost.add(DraggingGhost(icon_img, key))

    
    counter_img = _load_scaled("SC_seedpacket.png", counter_size)
    toolbar_group.add(SelectableItem(counter_img, "suncounter_icon"))

    return toolbar_group, toolbar_group_ghost

def special_delivery():
    
    cell_w, cell_h = UT.cell_size()
    seed_size = (int(cell_h * 1.10), int(cell_h))       # paquetes
    
    belt_group = pygame.sprite.Group()
    
    belt_img = _load_scaled('belt.png', (300, 90))
    belt_group.add(SelectableItem(belt_img, 'belt_icon'))
    
    nuts_group = pygame.sprite.Group()
    
    nut_img = _load_scaled('NT_seedpacket.png', seed_size)
    nuts_group.add(SelectableItem(nut_img, 'nut_icon'))
    
    return belt_group, nuts_group
