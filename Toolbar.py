import os
import pygame
import utils as UT


class DraggingGhost(pygame.sprite.Sprite):
    """
    Objeto fantasma que sigue al cursor del mouse durante el arrastre.
    La imagen se muestra semitransparente para indicar que es una vista previa.
    """
    def __init__(self, image: pygame.Surface, key: str):
        super().__init__()
        
        self.image = image.copy()
        self.image.set_alpha(128)
        self.rect = self.image.get_rect(center=UT.cell_center(10, 6, key))
        self.key = key

# ───────────────────────── Objects on toolbar's Clasic Mode ─────────────────────────

# class DraggingGhost(pygame.sprite.Sprite):
#     """
#     Objeto fantasma que sigue al cursor del mouse durante el arrastre.
#     La imagen se muestra semitransparente para indicar que es una vista previa.
#     """
#     def __init__(self, image: pygame.Surface, key: str):
#         super().__init__()
#         self.base_image = image 
#         self.image = image.copy()
#         self.image.set_alpha(128)  
#         self.rect = self.image.get_rect(center=UT.cell_center(10, 6, key))
#         self.key = key


class SelectableItem(pygame.sprite.Sprite):
    """
    Representa un ítem seleccionable en la barra de herramientas (toolbar).
    Tras colocar la planta, se activa un cooldown visible mediante un efecto grisáceo
    hasta que el ítem vuelva a estar disponible.
    """
    def __init__(self, image: pygame.Surface, key: str):
        super().__init__()
        self.base_image = image.copy()  
        self.image = image
        self.rect = self.image.get_rect(center=UT.cell_center(10, 6, key))
        self.key = key
        self.cooldown_end = 0  

    def ready(self):
        """
        Verifica si la planta está lista para volver a usarse.
        Returns:
            bool: True si el cooldown terminó, False en caso contrario.
        """
        return pygame.time.get_ticks() >= self.cooldown_end

    def start_cooldown(self):
        """
        Inicia el cooldown del ítem, impidiendo su uso hasta que se cumpla el tiempo definido.
        """
        self.cooldown_end = pygame.time.get_ticks() + UT.SEED_COOLDOWN

    def update(self):
        """
        Actualiza la apariencia del ítem según su estado de cooldown.
        Durante el cooldown, se superpone una capa semitransparente gris.
        Cuando finaliza, se restaura la imagen original.
        """
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

# ───────────────────────── Objects on toolbar's Papapapum Mode  ─────────────────────────

class Delivery(pygame.sprite.Sprite):
    """
    Objeto que representa el paquete de la nuez (seed packet) en movimiento sobre la cinta transportadora.
    """
    def __init__(self, image, key, size):
        super().__init__()
        self.speed = 0.5
        self.image = _load_scaled(image, size)
        self.rect = self.image.get_rect(center=UT.cell_center(10, 6, key))
        self.key = key
        
    def item_in_belt(self):
        """
        Desplaza el objeto hacia la derecha, simulando su movimiento sobre la cinta.
        """
        self.rect.x += self.speed

class Delivery_Ghost(pygame.sprite.Sprite):
    """
    Objeto fantasma que sigue al cursor del mouse durante el arrastre.
    La imagen se muestra semitransparente para indicar que es una vista previa.
    """
    def __init__(self, image, key, size):
        super().__init__()
        self.image = _load_scaled(image, size)
        self.image.set_alpha(128)
        self.rect = self.image.get_rect(center=UT.cell_center(10, 6, key))
        self.key = key

def _load_scaled(filename: str, size: tuple[int, int]) -> pygame.Surface:
    """Carga una imagen del directorio *Images* y la devuelve escalada.
    Entradas
    filename : str
        Nombre del archivo de imagen (por ejemplo "Peashooter.png").
    size : tuple[int, int]
        Dimensiones finales del ``pygame.Surface`` en píxeles
        *(ancho, alto)*.
    Returns
        pygame.Surface
        Superficie de Pygame ya convertida con alpha y escalada al tamaño
        solicitado."""
    path = os.path.join("Images", filename)
    surf = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(surf, size)


def toolbar() -> tuple[pygame.sprite.Group, pygame.sprite.Group]:
    """
    Crea y devuelve los grupos de sprites de la barra de herramientas del modo clásico.

    Returns:
        tuple[pygame.sprite.Group, pygame.sprite.Group]: 
            - Grupo con ítems seleccionables (paquetes de semillas).
            - Grupo con íconos fantasma para arrastrar al tablero.
    """
    _ , cell_h = UT.cell_size()

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
    """
    Crea los grupos de sprites para el modo de cinta transportadora ('Papapapum').

    Returns:
        tuple[pygame.sprite.Group, pygame.sprite.Group, pygame.sprite.Group]:
            - Grupo de la cinta transportadora.
            - Grupo con ítems (semillas) que aparecen en la cinta.
            - Grupo con íconos fantasma para previsualizar la colocación.
    """
    _, cell_h = UT.cell_size()
    seed_size = (int(cell_h * 1.10), int(cell_h))
    icon_size = (int(cell_h * 0.70), int(cell_h * 0.80))  # iconos "fantasma"
    belt_size = (int(cell_h * 20), int(cell_h - 5))
    
    belt_group = pygame.sprite.Group()
    belt_group.add(Delivery('belt.png', 'belt_icon', belt_size))
    
    nuts_toolbar_group = pygame.sprite.Group()
    nuts_toolbar_group.add(Delivery('NT_seedpacket.png', 'belt_nut_icon', (seed_size[0]-20, seed_size[1]-20)))
    
    nuts_group_ghost = pygame.sprite.Group()
    
    icon_img = _load_scaled('Nut.png', icon_size)
    nuts_group_ghost.add(DraggingGhost(icon_img, 'nut_icon'))
    
    return belt_group, nuts_toolbar_group, nuts_group_ghost
