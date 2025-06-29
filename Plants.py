import pygame
import utils as UT
import os

# ────────────────────────── Plantas ────────────────────────── 
class Plants(pygame.sprite.Sprite):
    """
    Clase padre de las plantas (hereda atributos de clase sprite.Sprtie de pygame). 
    Todo objeto de esta clase hereda las siguientes funciones:
    1. take_damage() mata a la planta su vida es menor o igual a cero, sino le resta el daño recibido.
    2. remove() elimina a la planta y retorna el 50 de su costo de soles (utilizada con la pala)
    """
    def __init__(self, image_file: str, pos: tuple, cost: int =50, life: int =300):
        """
        Se toman como entradas: la ruta de la imagen (image_file), la posicion del centro 
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
        self.ready = None # Se utiliza en las habilidades de las plantas
        self.life = life 
    def take_damage(self, damage=0):
        """
        Funcion a traves de la cual la planta recibe daño
        Si la vida de la planta es menor o igual a cero muere
        """
        self.life -= damage
        if self.life <= 0: self.kill()
    def remove(self) -> int:
        """
        Funcion a traves de la cual la planta puede ser removida por el usuario.
        Complementa el uso de la pala.
        retorna el 50% del costo
        """
        self.kill()
        return int(self.cost / 2)

# 1. Girasol
class Sunflower(Plants):
    """
    Clase de los girasoles (clase hija de Plants). Su habilidad es cada 10 segundos devolver soles
    para que el usuario aumente su contador. Su funcion que ejecuta la habilidad es ability().
    """
    def __init__(self, image_file: str, pos: tuple, cost: int=50, life: int=300):
        """
        Se toman como entradas: la ruta de la imagen (image_file), la posicion del centro 
        del objeto (pos), el costo de la planta y su vida.
        La inicializacion es igual que para la clase padre Plants.
        """
        super().__init__(image_file, pos, cost, life)
    def ability(self, zombies) -> tuple:
        """
        Clase para la habilidad del girasol. Cada 10 segundos, libera un girasol que puede ser recogido por el usuario.
        Toma como entradas al grupo de sprites de los zombies para evitar conflictos con otras plantas en el gameloop.
        La salida (cuando se ejecuta la habilidad) es una tupla con dos elementos:
         1. Objeto de la clase SF_sun (un sol)
         2. String que identifica que la accion fue hecha por el girasol ('sunflower')
        """
        if self.ready is None:
            self.ready = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.ready >= 10000:
            sun = SF_sun('Images/sol.png', self.rect.center, self.rect.centery)
            self.ready = None
            return sun, 'sunflower'
        return None, None

# 2. Nuez
class Nut(Plants):
    """
    Clase de las Nueces (clase hija de Plants). No tiene habilidad, su caracteristica unica
    es que tiene mas vida que otras plantas. 
    """
    def __init__(self, image_file: str, pos: tuple, cost: int=50, life: int=4000):
        """
        Se toman como entradas: la ruta de la imagen (image_file), la posicion del centro 
        del objeto (pos), el costo de la planta y su vida.
        La inicializacion es igual que para la clase padre Plants.       
        """
        super().__init__(image_file, pos, cost, life)
    def ability(self, zombies) -> tuple:
        """
        No tiene habilidad pero se define este metodo para evitar conflictos en el gameloop.
        """
        return None, None

# 3. Boomerang
class Boomerang(Plants):
    """
    Clase de las plantas Boomerang (clase hija de Plants). Su habilidad es tirar un proyectil (un boomerang) que
    vuelve hacia la planta luego de llegar hasta el final de la grilla. A los zombis en su trayecto les disminuye
    vida. Su habilidad se ejecuta en ability().
    """
    def __init__(self, image_file: str, pos: tuple, boomerang_file: str, cost: int=175, life: int=300):
        """
        Se toman como entradas: la ruta de la imagen (image_file), la posicion del centro 
        del objeto (pos), la ruta de la imagen de su proyectil (boomerang_file), el costo de la planta y su vida.
        La inicializacion es casi identica que para la clase padre Plants 
        con la unica diferencia que tambien se solicita la ruta de la imagen del proyectil.        
        """
        super().__init__(image_file, pos, cost, life)
        self.boomerang_file = boomerang_file
    def ability(self, zombies: pygame.sprite.Group) -> tuple:
        """
        Clase para la habilidad de la planta Boomerang. Dispara un proyectil que recorre toda la fila. 
        Se verifica que haya zombis en su fila para disparar. 
        La salida (cuando se ejecuta la habilidad) es una tupla con dos elementos:
         1. Objeto de la clase Boomerang_Bullet (un proyectil)
         2. String que identifica que la accion fue hecha por la planta boomerang ('boomerang')        
        """
        # Se verifica que haya zombis para disparar en su fila
        if not any(z.cy == self.pos[1] and z.rect.x >= self.pos[0] for z in zombies):
            return None, None
        if self.ready is None:       # Se empieza timer para disparar un proyectil
            self.ready = pygame.time.get_ticks() 
        elif pygame.time.get_ticks() - self.ready >= 1500: # Se resta tiempo actual a tiempo desde el ultimo disparo
            new_boomerang = Boomerang_Bullet(self.boomerang_file, self.pos)   # Proyectil 
            self.ready = None
            return new_boomerang, 'boomerang'
        return None, None

# 3.1. Proyectil de la planta Boomerang
class Boomerang_Bullet(pygame.sprite.Sprite):
    """
    Clase para los proyectiles de la planta boomerang. Es una clase hija de la clase sprite.Sprite de pygame.
    Tiene su metodo shoot() para avanzar su posicion o retrocederla segun corresponda (el trayecto del proyectil).
    """
    def __init__(self, image_file: str, pos: tuple):
        """
        Se reciben como entradas la ruta de la imagen (image_file) y la posicion del centro del objeto (pos).
        """
        super().__init__()
        cw, ch = UT.cell_size()
        raw = pygame.image.load(image_file).convert_alpha()
        size = int(ch * 0.4)
        self.image = pygame.transform.scale(raw, (size, size)) # Se ajustan las dimensiones del objeto a la ventana
        self.x, self.y = pos
        self.rect = self.image.get_rect(center=(self.x, self.y)) # Se define el rect del objeto y su posicion
        self.speed = max(4, cw // 20)
        self.original = pos         
        self.final = UT.cell_center(10, 6, 'boomerang_range', self.original[1])         # Definimos rango del proyectil
        # Estados para ver si avanza o retrocede
        self.foward = True
        self.backward = False
        self.already_hit_zombies = [] # Se guarda una identificacion de los zombies que ya golpeo

    def shoot(self):
        """
        Habilidad propia del proyectil. Hace que avance su posicion hasta llegar a su rango final.
        Cuando llega al final, comienza a volver hacia la planta, listo para volver a golpear a 
        los zombis en la fila.
        """
        if self.foward:
            self.rect.x += self.speed
            if self.rect.centerx == self.final[0]: 
                # Cuando llega al final se invierten los valores de movimiento
                self.foward = False
                self.backward = True
                self.already_hit_zombies = [] # Se resetean los zombis que ya golpeo para poder golpearlos mientras retrocede
        elif self.backward: 
            self.rect.x -= self.speed
            # Cuando vuelve a su posicion original se elimina el objeto
            if self.rect.centerx == self.original[0]:
                self.kill() 

# 4. Lanzaguisantes
class PeaShotter(Plants):
    """
    Clase del Lanzaguisantes (clase hija de Plants). Su habilidad es tirar un proyectil (un guisante) que al impactar
    con un zombi le disminuye su vida, y el guisante desaparece. Su funcion se ejecuta en ability().
    """
    def __init__(self, image_file: str, pos: tuple, pea_file: str, cost: int=100, life: int=300):
        """
        Se toman como entradas: la ruta de la imagen (image_file), la posicion del centro 
        del objeto (pos), la ruta de la imagen de su proyectil (pea_file), el costo de la planta y su vida.
        La inicializacion es casi identica que para la clase padre Plants 
        con la unica diferencia que tambien se solicita la ruta de la imagen del proyectil.        
        """
        super().__init__(image_file, pos, cost, life)
        self.pea_file = pea_file

    def ability(self, zombies: pygame.sprite.Group) -> tuple:
        """
        Clase para la habilidad del Lanzaguisante. Dispara un proyectil que recorre la fila, hasta
        impactar con un zombi.
        La salida (cuando se ejecuta la habilidad) es una tupla con dos elementos:
         1. Objeto de la clase Pea (un proyectil)
         2. String que identifica que la accion fue hecha por el lanzaguisantes ('peashotter')        
        """
        # Se verifica que haya zombis para disparar en su fila
        if not any(z.cy == self.pos[1] and z.rect.x >= self.pos[0] for z in zombies): 
            return None, None
        if self.ready is None:
            self.ready = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.ready >= 1400: # Cada 1.4 segundos dispara un proyectil
            new_pea = Pea(self.pea_file, self.pos)
            self.ready = None
            return new_pea, 'peashotter'
        return None, None

# 4.1. Proyectil del Lanzaguisantes
class Pea(pygame.sprite.Sprite):
    """
    Clase para los proyectiles del Lanzaguisantes. Es una clase hija de la clase sprite.Sprite de pygame.
    Tiene su metodo shoot() para avanzar su posicion.
    """
    def __init__(self, image_file: str, pos: tuple):
        super().__init__()
        cw, ch = UT.cell_size()
        raw = pygame.image.load(image_file).convert_alpha() 
        size = int(ch * 0.4)
        self.image = pygame.transform.scale(raw, (size, size)) # Se dimensiona la imagen
        self.x, self.y = pos
        self.rect = self.image.get_rect(center=(self.x, self.y - int(ch * 0.25))) # Se obtiene el rect del guisante
        self.speed = max(4, cw // 20)
    def shoot(self):
        """
        Metodo que avanza la posicion del guisante
        """
        self.rect.x += self.speed

# 5. Cereza Bomba
class cherry(Plants):
    """
    Clase de la planta Cereza (clase hija de Plants). Su habilidad es explotar y eliminar a los zombis
    en un range 3x3 a su alrededor. Su funcion se ejecuta en ability().
    """
    def __init__(self, image_file: str, pos: tuple, explosion_file: str, cost: int=200, life: int=10):
        """
        Se toman como entradas: la ruta de la imagen (image_file), la posicion del centro 
        del objeto (pos), la ruta de la imagen de su explosion (explosion_file), el costo de la planta y su vida.
        La inicializacion es casi identica que para la clase padre Plants con la 
        diferencia de que se pide la ruta de la imagen de la explosion.       
        """
        super().__init__(image_file, pos, cost, life)
        self.explosion_file = explosion_file

    def ability(self, zombies: pygame.sprite.Group) -> tuple:
        """
        Clase para la habilidad de la cereza. Al ser ubicada explota inmediatamente matando
        a todo zombi en un radio 3x3.
        La salida es una tupla con ambos elementos siendo None pues no es
        necesaria identificar su habilidad en el gameloop.     
        """
        explosion_range = UT.cell_center(10, 6, 'cherry_range', self.pos) # Se obtiene su area de explosion
        for zombie in zombies:
            if explosion_range.colliderect(zombie.rect): # Si un zombi se encuentra en el rango muere
                zombie.kill()
        explosion = plant_boom(self.explosion_file, self.pos, scale=3)
        self.kill() # Se elimina la planta luego de explotar
        return explosion, 'cherry'

# 6. Papapum
class Papapum(Plants):
    """
    Clase del Papapum (clase hija de Plants). Su habilidad es explotar cuando un zombi
    lo pisa. Pero primero debe cargarse. Su funcion se ejecuta en ability().
    """
    def __init__(self, image_file_loading: str, image_file_ready: str, explosion_file: str, pos: tuple, cost: int=200, life: int=50):
        """
        Se toman como entradas: la ruta de la imagen del papapum bajo tierra (image_file_loading), la ruta de la imagen
        del papaum listo para explotar (image_file_ready), la ruta de la imagen de su explosion (explosion_file) la posicion del centro 
        del objeto (pos), la ruta de la imagen de su proyectil (pea_file), el costo de la planta y su vida.
        La inicializacion es casi identica que para la clase padre Plants con la unica diferencia 
        que se tiene en cuenta la nocion de que las planta esta lista o no para explotar, y que se carga el archivo de
        su explosion.       
        """
        super().__init__(image_file_loading, pos, cost, life)
        self.image_file_ready = image_file_ready
        self.transformed = False # Se setea en falso que este transformado
        self.explosion_file = explosion_file

    def ability(self, zombies: pygame.sprite.Group) -> tuple:
        """
        Clase para la habilidad del papaum. Comienza el timer para transformarse cuando primero se 
        ejecuta la funcion. Luego de 10 segundos se transforma y se activa su habilidad 
        que es que si algun zombi lo pisa muere instantaneamente. La salida es una tupla con ambos 
        elementos siendo None pues no es necesaria identificar su habilidad en el gameloop.     
        """
        explosion = (None, None) # Si el papapum no explota
        if self.ready is None:
            self.ready = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.ready >= 10000: # luego de 10 segundos es transformado
            if not self.transformed:
                # Se modifican su imagen y rect
                self.image = self.image_file_ready
                raw = pygame.image.load(self.image).convert_alpha()
                c_w, c_h = UT.cell_size()
                self.image = pygame.transform.scale(raw, (int(c_h * 1.0), int(c_h * 0.9)))
                self.rect = self.image.get_rect(center=self.pos)
                self.transformed = True # Se setea en True que ya se transformo
                self.life = 1000
            for zombie in zombies:
                # Si un zombi lo pisa se muere, excepto el zombi del globo.
                if self.rect.collidepoint(zombie.rect.center) and zombie.type != 'Balloon':
                    zombie.kill() 
                    explosion = (plant_boom(self.explosion_file, self.pos), 'papapum') # Si el papapum explota
                    self.kill()
        return explosion
    
# 7. Papa Giratoria (propia del modo especial)
class Spinning_Nut(Plants):
    """
    Clase de la Nuez giratorio (clase hija de Plants). Propia del modo especial, la
    Nuez rueda y elimina a los zombis en su fila. Su habilidad se ejecuta en la funcion
    ability().
    """
    def __init__(self, image_file: str, pos: tuple, cost=None, life=None):
        super().__init__(image_file, pos, cost, life)
        self.speed = 0
        self.angle = 0
        
        cw, ch = UT.cell_size()
        raw = pygame.image.load(image_file).convert_alpha()     # Se transforma la imagen
        self.image = pygame.transform.scale(raw, (cw - 10, ch - 10))
        self.original_image = pygame.transform.scale(raw, (cw - 10, ch - 10))
        self.rect = self.image.get_rect(midright=pos)
        self.pos = pygame.Vector2(self.rect.center)  # posición flotante precisa
        
        self.already_hit_zombies = [] # Se guarda una identificacion de los zombies que ya golpeo
        self.already_hit = False

    def ability(self):
        """
        Clase para la habilidad de la Nuez giratoria. Cada vez que se llama avanza la Nuez.
        Cuando llega al final del trayecto es eliminada.   
        """
        self.speed = 7
        self.pos.x += self.speed  # movimiento con precisión flotante
        self.angle -= 8

        # rotar imagen
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)  # usar pos exacta como centro

        screen_w = pygame.display.get_surface().get_width()
        if self.rect.left >= screen_w: # La nuez se elimina cuando exede el borde de la pantalla 
            self.kill()
            
# Extra: clase de las explosiones
class plant_boom(pygame.sprite.Sprite):
    """
    Clase dedicada a las imagenes de las explosiones de las plantas (cherry y papaum). Hija de la
    clase sprite.Sprite de pygame. Para incizializar se pide la ruta de la imagen (image_file), la 
    posicion de la explosion (pos), el tiempo en pantalla de la explosion (time_in_screen) y un 
    factor para el area de la explosion (scale). El metodo update_screen_boom() actualiza la pantalla.
    """
    def __init__(self, image_file: str, pos: tuple, time_in_screen: int = 2000, scale: float = 1):
        """
        Se toman como entradas la ruta de la imagen (image_file), la posicion de la explosion (pos) 
        y el tiempo en pantalla de la explosion (time_in_screen). Ademas se toma la entrada scale
        para poder decidir el area de la explosion.
        """
        super().__init__()
        cw, ch = UT.cell_size()
        raw = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(raw, (int(cw*scale), int(ch*scale)))
        self.pos = pos

        self.rect = self.image.get_rect(center=pos)  
        self.time_in_screen = time_in_screen 
        self.start_time = pygame.time.get_ticks()     
    def update_screen_boom(self, screen: pygame.surface.Surface):
        """
        Metodo utilizado para actualizar la pantalla segun la duracion de la explosion.
        Toma como entrada screen (pygame.surface.Surface) que es la pantalla del usuario
        a ser actualizada.
        """
        # Si el tiempo desde que exploto no supera su tiempo en pantalla se actualiza
        if pygame.time.get_ticks() - self.start_time < self.time_in_screen:
            screen.blit(self.image, self.rect)
        else: self.kill() 

# ────────────────────────── Podadora ──────────────────────────
class Lawnmower(pygame.sprite.Sprite):
    """
    Clase de las Podadoras (hija de la clase sprite.Sprite de pygame). Se activa cuando un zombi entra 
    en contacto con ella y avanza hasta salir de pantalla. Su movimiento se ejecuta a traves del 
    metodo movement()
    """

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

    def movement(self, zombies: pygame.sprite.Group):
        """
        Funcion que activa el movimiento de la podadora cuando un zombi entra en contacto 
        con ella. Si se encuentra un zombi en su camino lo elimina inmediatamente.
        """
        if not self.active:
            if pygame.sprite.spritecollideany(self, zombies):
                self.active = True
                self.speed = max(6, UT.cell_size()[0] // 20)
        else:
            self.rect.x += self.speed
            pygame.sprite.spritecollide(self, zombies, True) # Elimina zombis en su posicion (a medida que avanza)

            if self.rect.left > self._screen_width + self.rect.width:
                self.kill()

def add_lawnmowers(cols: int = 10, rows: int = 6) -> pygame.sprite.Group:
    """
    Funcion utilizada para agregar las podadoras segun la cantidad de filas.
    Tiene como entrada la cantidad de columnas y filas.
    Como salida devuelve un pygame.sprite.Group con la podadoras
    """
    lawnmowers = pygame.sprite.Group()
    for row in range(1, rows):  
        center = UT.cell_center(cols, rows, "lawnmower", row) # Se obtiene posicion del centro
        if center:
            lawnmowers.add(Lawnmower(*center))
    return lawnmowers

# ────────────────────────── Soles ────────────────────────── 
class Suns(pygame.sprite.Sprite):
    """
    Clase para los soles de nuestro juego (hija de la clase sprite.Sprite de pygame).
    """
    def __init__(self, image_file: str, start_pos = None, fpy = None, value=50, cols = 10, rows = 6):
        """
        Se toman como entradas la ruta de la imagen (image_file), la posicion incial (start_pos) que 
        es utilizada para los soles que provienen de girasoles al igual que fpy que es 'final position y'.
        Ademas toma como entrada el valor del girasol (value) y las dimensiones de la ventana (cols, rows,)
        """
        super(Suns, self).__init__()
        non_dimmed = pygame.image.load(image_file).convert_alpha()
        cw, ch = UT.cell_size()
        self.image = pygame.transform.scale(non_dimmed, (ch*0.75, ch*0.75))
        # Se inicializa distinto para soles que caen del cielo y para los que provienen de girasoles
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
        2. Si no llego a su posicion final, se mueve su posicion.
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


