import pygame
import utils as UT
import SUNS as SN

class Plants(pygame.sprite.Sprite):
    """
    Clase padre de las plantas (hereda atributos de clase sprite.Sprtie de pygame). 
    Todo objeto de esta clase hereda las siguientes funciones:
    1. take_damage() mata a la planta su vida es menor o igual a cero, sino le resta el daño recibido.
    2. remove() elimina a la planta y retorna el 50 de su costo de soles (utilizada con la pala)
    """
    def __init__(self, image_file: str, pos: tuple, cost: int =50, life: int =300):
        """
        Se toman como entradas: la ruta de la imagen (image_fila), la posicion del centro 
        del objeto (pos), el costo de la planta y su vida.
        Se obtiene el rect (hitbox) de la planta.
        """
        super().__init__()
        cw, ch = UT.cell_size()
        raw = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(raw, (cw, ch))
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)
        self.cost = cost
        self.state = pygame.time.get_ticks()
        self.ready = None
        self.life = life
    def take_damage(self, damage=0):
        """
        Funcion a traves de la cual la planta recibe daño
        Si la vida de la planta es menor o igual a cero muere
        """
        self.life -= damage
        if self.life <= 0: self.kill()
    def remove(self):
        """
        Funcion a traves de la cual la planta puede ser removida por el usuario.
        Complemente el uso de la pala.
        retorna el 50% del costo
        """
        self.kill()
        return int(self.cost / 2)

class Sunflower(Plants):
    def __init__(self, image_file, pos, cost=50, life=300):
        super().__init__(image_file, pos, cost, life)
    def ability(self, zombies):
        if self.ready is None:
            self.ready = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.ready >= 10000:
            sun = SN.SF_sun('Images/sol.png', self.rect.center, self.rect.centery)
            self.ready = None
            return sun, 'sunflower'
        return None, None

class Nut(Plants):
    def __init__(self, image_file, pos, cost=50, life=4000):
        super().__init__(image_file, pos, cost, life)
    def ability(self, zombies):
        return None, None

class Boomerang(Plants):
    def __init__(self, image_file, pos, boomerang_file, cost=175, life=300):
        super().__init__(image_file, pos, cost, life)
        self.boomerang_file = boomerang_file
    def ability(self, zombies):
        if not any(z.cy == self.pos[1] for z in zombies):
            return None, None
        if self.ready is None:
            self.ready = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.ready >= 1400:
            new_boomerang = Boomerang_Bullet(self.boomerang_file, self.pos)
            self.ready = None
            return new_boomerang, 'boomerang'
        return None, None

class Boomerang_Bullet(pygame.sprite.Sprite):
    def __init__(self, image_file, pos):
        super().__init__()
        cw, ch = UT.cell_size()
        raw = pygame.image.load(image_file).convert_alpha()
        size = int(ch * 0.4)
        self.image = pygame.transform.scale(raw, (size, size))
        self.x, self.y = pos
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speed = max(6, cw // 20)

        self.original = pos
        self.final = UT.cell_center(10, 6, 'boomerang_range', self.original[1])
        self.foward = True
        self.backward = False
        self.already_hit_zombies = []
    def shoot(self):
        if self.foward:
            self.rect.move_ip(2, 0)
            if self.rect.centerx == self.final[0]:
                self.foward = False
                self.backward = True
                self.already_hit_zombies = []
        elif self.backward:
            self.rect.move_ip(-2, 0)
            if self.rect.centerx == self.original[0]:
                self.kill()

class PeaShotter(Plants):
    def __init__(self, image_file, pos, pea_file, cost=100, life=300):
        super().__init__(image_file, pos, cost, life)
        self.pea_file = pea_file
    def ability(self, zombies):
        if not any(z.cy == self.pos[1] for z in zombies):
            return None, None
        if self.ready is None:
            self.ready = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.ready >= 1400:
            new_pea = Pea(self.pea_file, self.pos)
            self.ready = None
            return new_pea, 'peashotter'
        return None, None
    

class Pea(pygame.sprite.Sprite):
    def __init__(self, image_file, pos):
        super().__init__()
        cw, ch = UT.cell_size()
        raw = pygame.image.load(image_file).convert_alpha()
        size = int(ch * 0.4)
        self.image = pygame.transform.scale(raw, (size, size))
        self.x, self.y = pos
        self.rect = self.image.get_rect(center=(self.x, self.y - int(ch * 0.25)))
        self.speed = max(6, cw // 20)
    def shoot(self):
        self.rect.move_ip(2, 0)

class Spinning_Nut(Plants):
    def __init__(self, image_file, pos, cost=None, life=None, dims=(1200, 600)):
        super().__init__(image_file, pos, cost, life)
        self.speed = 0
        cw, ch = UT.cell_size()
        self.dims = dims
        raw = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(raw, (cw, ch))
        self.original_image = pygame.transform.scale(raw, (cw, ch))
        self.rect = self.image.get_rect(midright=pos)
        self.angle = 0
        self.already_hit = False
    def ability(self):
        self.speed = 5
        self.rect.x += self.speed
        self.angle -= 8
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.rect.x >= self.dims[0]:
            self.kill()

class cherry(Plants):
    def __init__(self, image_file, pos, cost=200, life=10):
        super().__init__(image_file, pos, cost, life)
    def ability(self, zombies):
        explosion_range = UT.cell_center(10, 6, 'cherry_range', self.pos)
        for zombie in zombies:
            if explosion_range.colliderect(zombie.rect):
                zombie.kill()
        self.kill()
        return None, None

class Papapum(Plants):
    def __init__(self, image_file_loading, image_file_ready, pos, cost=25, life=50):
        super().__init__(image_file_loading, pos, cost, life)
        self.image_file_ready = image_file_ready
        self.transformed = False
    def ability(self, zombies):
        if self.ready is None:
            self.ready = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.ready >= 10000:
            if not self.transformed:
                self.image = self.image_file_ready
                raw = pygame.image.load(self.image).convert_alpha()
                c_w, c_h = UT.cell_size()
                self.image = pygame.transform.scale(raw, (int(c_h * 1.0), int(c_h * 0.9)))
                self.rect = self.image.get_rect(center=self.pos)
                self.transformed = True
                self.life = 1000
            for zombie in zombies:
                if self.rect.collidepoint(zombie.rect.center) and zombie.type != 'balloon':
                    zombie.kill()
                    self.kill()
        return None, None

class Lawnmower(pygame.sprite.Sprite):
    """Podadora que se activa al primer zombi de su fila y avanza hasta salir de pantalla."""

    def __init__(self, x: int, y: int):
        super().__init__()

        # --- Escala de la imagen en función del tamaño de celda actual ---
        raw_img = pygame.image.load("Images/lawnmower.png").convert_alpha()
        c_w, c_h = UT.cell_size()
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
                self.speed = max(6, UT.cell_size()[0] // 20)
        else:
          
            self.rect.x += self.speed
            pygame.sprite.spritecollide(self, zombies, True)

        
            if self.rect.left > self._screen_width + self.rect.width:
                self.kill()

def add_lawnmowers(cols: int = 10, rows: int = 6) -> pygame.sprite.Group:
    lawnmowers = pygame.sprite.Group()
    for row in range(1, rows):  
        center = UT.cell_center(cols, rows, "lawnmower", row)
        if center:
            lawnmowers.add(Lawnmower(*center))
    return lawnmowers
