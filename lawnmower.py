import pygame
from SUNS import cell_center
from utils import cell_size


class Lawnmower(pygame.sprite.Sprite):
    """Podadora que se activa al primer zombi de su fila y avanza hasta salir de pantalla."""

    def __init__(self, x: int, y: int):
        super().__init__()

        # --- Escala de la imagen en función del tamaño de celda actual ---
        raw_img = pygame.image.load("Images/lawnmower.png").convert_alpha()
        c_w, c_h = cell_size()
        scale = (int(c_w * 0.9), int(c_h * 0.7))  # ancho ≈ celda completa, alto un poco menor
        self.image = pygame.transform.scale(raw_img, scale)
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 0
        self.active = False
        self._screen_width = pygame.display.get_surface().get_width()
    def movement(self, zombies: pygame.sprite.Group) -> None:
        

        if not self.active:
            
            if pygame.sprite.spritecollideany(self, zombies):
                self.active = True
                self.speed = max(6, cell_size()[0] // 20)
        else:
          
            self.rect.x += self.speed
            pygame.sprite.spritecollide(self, zombies, True)

        
            if self.rect.left > self._screen_width + self.rect.width:
                self.kill()

def add_lawnmowers(cols: int = 10, rows: int = 6) -> pygame.sprite.Group:
    lawnmowers = pygame.sprite.Group()
    for row in range(1, rows):  
        center = cell_center(cols, rows, "lawnmower", row)
        if center:
            lawnmowers.add(Lawnmower(*center))
    return lawnmowers
