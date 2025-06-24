import os
import pygame
import utils as UT


class DraggingGhost(pygame.sprite.Sprite):
    

    def __init__(self, image: pygame.Surface, key: str):
        super().__init__()
        self.base_image = image 
        self.image = image.copy()
        self.image.set_alpha(128)  
        self.rect = self.image.get_rect(center=UT.cell_center(10, 6, key))
        self.key = key


class SelectableItem(pygame.sprite.Sprite):

    def __init__(self, image: pygame.Surface, key: str):
        super().__init__()
        self.base_image = image.copy()  
        self.image = image
        self.rect = self.image.get_rect(center=UT.cell_center(10, 6, key))
        self.key = key
        self.cooldown_end = 0  
    def item_in_belt(self):
        self.rect.x += 8

    def ready(self):
        
        return pygame.time.get_ticks() >= self.cooldown_end

    def start_cooldown(self):
        
        self.cooldown_end = pygame.time.get_ticks() + UT.SEED_COOLDOWN

    def update(self):
        
        if self.ready():
            self.image = self.base_image
        else:
            
            now   = pygame.time.get_ticks()
            left  = self.cooldown_end - now        
            ratio = left / UT.SEED_COOLDOWN         

            self.image = self.base_image.copy()

            shade = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            shade.fill((0, 0, 0, int(160 * ratio)))   
            self.image.blit(shade, (0, 0))

class Delivery(pygame.sprite.Sprite):
    def __init__(self, image, key, size):
        super().__init__()
        self.speed = 0.3
        self.image = _load_scaled(image, size)
        self.rect = self.image.get_rect(center=UT.cell_center(10, 6, key))
        self.key = key
        
    def item_in_belt(self):
        self.rect.x += self.speed
class Delivery_Ghost(pygame.sprite.Sprite):
    def __init__(self, image, key, size):
        super().__init__()
        self.image = _load_scaled(image, size)
        self.image.set_alpha(128)
        self.rect = self.image.get_rect(center=UT.cell_center(10, 6, key))
        self.key = key

def _load_scaled(filename: str, size: tuple[int, int]) -> pygame.Surface:
    path = os.path.join("Images", filename)
    surf = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(surf, size)


def toolbar() -> tuple[pygame.sprite.Group, pygame.sprite.Group]:
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
        ("CB_seedpacket.png", "cherry_icon", "Cherry.png"),
        ("BM_seedpacket.png", "boomerang_icon", "boomerang_plant.png"),
        ("PM_seedpacket.png", "papapum_icon", "papapum_load.png")
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
    seed_size = (int(cell_h * 1.10), int(cell_h))
    belt_size = (int(cell_h * 10), int(cell_h))
    
    belt_group = pygame.sprite.Group()
    belt_group.add(Delivery('belt.png', 'belt_icon', belt_size))
    
    nuts_toolbar_group = pygame.sprite.Group()
    nuts_toolbar_group.add(Delivery('NT_seedpacket.png', 'belt_nut_icon', (seed_size[0]-15, seed_size[1]-15)))
    
    nuts_group_ghost = pygame.sprite.Group()
    nuts_group_ghost.add(Delivery_Ghost('Nut.png', 'belt_icon', (seed_size[0]-15, seed_size[1]-15)))
    
    
    return belt_group, nuts_toolbar_group, nuts_group_ghost
