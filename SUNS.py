import pygame
from random import randint
import utils as UT

# Clase soles
class Suns(pygame.sprite.Sprite):
    """
    Clase para los soles de nuestro juego (hija de la clase sprite.Sprite de pygame).
    """
    def __init__(self, image_file: str, start_pos = None, fpy = None, value=50, cols = 10, rows = 6):
        """
        Se toman como entradas la ruta de la imagen (image_fila), la posicion incial (start_pos) que 
        es utilizada para los soles que provienen de girasoles al igual que fpy que es 'final position y'.
        Ademas toma como entradad el valor del girasol (value) y las dimensiones de la ventana (cols, rows,)
        """
        super(Suns, self).__init__()
        non_dimmed = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(non_dimmed, (80, 80))
        # Se incializa distinto para soles que caen del cielo y para los que provienen de girasoles
        if fpy == None or start_pos == None:
            final_pos = UT.cell_center(cols, rows, 'sun', None)
            self.rect = self.image.get_rect(center=(final_pos[0], 0))
            self.final_pos = (final_pos[0], final_pos[1])
        else:
            self.rect = self.image.get_rect(center=(start_pos))
            self.final_pos = (start_pos[0], start_pos[1])

        self.state = True
        self.value = value
        self.time = None
    def action(self):
        """
        Metodo para las acciones del sol que son los siguientes:
        1. Si el girasol llego a su posicion final, y luego pasan 10 segundos sin ser recogido desaparece
        2. Si no llego a su posicion final, se mueve su posicon.
        """
        if self.rect.center == self.final_pos:
            if self.time is None:
                self.time = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - self.time >= 10000:
                self.kill()
            self.state = False
        elif self.state:
            self.rect.move_ip((0, 1))
    def grab(self) -> int:
        """
        Metodo para agarrar el sol. Si es agarrado devuelve su value y es eliminado
        """
        self.kill()
        return self.value

class SF_sun(Suns):
    """
    Clase hija de Suns. Comparte todas sus mismas caracteristicas. Sin embargo, se 
    distingue que esta clase es exclusiva para soles que provienen de girasoles. 
    La inicializacion es identifca que para los soles del cielo pero ya se tiene
    en cuenta su posicion inicial y final.
    """
    def __init__(self, image_file, start_pos, fpy, value=50):
        super().__init__(image_file, start_pos, fpy, value)


