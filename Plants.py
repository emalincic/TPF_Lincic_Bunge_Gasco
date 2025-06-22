import pygame
import utils as UT
import SUNS as SN
import os
pygame.mixer.init()

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
        Complemente el uso de la pala.
        retorna el 50% del costo
        """
        self.kill()
        return int(self.cost / 2)

# 1. Girasol
class Sunflower(Plants):
    """
    Clase de los girasoles (clase hija de Plants). Su habilidad es cada 10 segundos devolver soles
    para que el usuario aumente su contador. Su funcion que ejectua la habilidad es ability().
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
            sun = SN.SF_sun('Images/sol.png', self.rect.center, self.rect.centery)
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
    vuelve hacia la planta luego de llegar hasta el final de la grilla. A los zombis en su trayecto les diminuye
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
        if not any(z.cy == self.pos[1] for z in zombies): #! SE PUEDE MEJORAR (SOLO SI EL ZOMBI ESTA DELANTE DE LA PLANTA)
            return None, None
        if self.ready is None:       # Se empieza timer para disparar un proyectil
            self.ready = pygame.time.get_ticks() 
        elif pygame.time.get_ticks() - self.ready >= 1400: # Se resta tiempo actual a tiempo desde el ultimo disparo
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
        Se reciben como entradas la ruta de la imagen (image_file) y la posicion del centro del obeto (pos).
        """
        super().__init__()
        cw, ch = UT.cell_size()
        raw = pygame.image.load(image_file).convert_alpha()
        size = int(ch * 0.4)
        self.image = pygame.transform.scale(raw, (size, size)) # Se ajustan las dimensiones del objeto a la ventana
        self.x, self.y = pos
        self.rect = self.image.get_rect(center=(self.x, self.y)) # Se define el rect del objeto y su posicon
        self.speed = max(6, cw // 20) #! PARA QUE SE USA ESTO?
        self.original = pos         
        self.final = UT.cell_center(10, 6, 'boomerang_range', self.original[1])         # Definimos rango del proyectil
        # Estados para ver si avanza o retrocede
        self.foward = True
        self.backward = False
        self.already_hit_zombies = [] # Se guarda una identificacion de los zombies que ya golpeo
    def shoot(self):
        """
        Habilidad propia del proyectil. Hace que avance su posicon hasta llegar a su rango final.
        Cuando llega al final, comienza a volver hacia la planta, listo para volver a golpear a 
        los zombis en la fila.
        """
        if self.foward:
            self.rect.move_ip(2, 0)
            if self.rect.centerx == self.final[0]: 
                # Cuando llega al final se invierten los valores de movimiento
                self.foward = False
                self.backward = True
                self.already_hit_zombies = [] # Se resetean los zombis que ya golpeo para poder golpearlos mientras retrocede
        elif self.backward:
            self.rect.move_ip(-2, 0)
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
        self.shooting_sound = pygame.mixer.Sound(os.path.join('Audio', 'zombies eating sound.mp3'))
        self.Channel = pygame.mixer.Channel(1)
        self.shooting = False
    def ability(self, zombies: pygame.sprite.Group) -> tuple: #! USAMOS ESE TYPEHINT PARA LOS ZOMBIS?
        """
        Clase para la habilidad del Lanzaguisante. Dispara un proyectil que recorre la fila, hasta
        impactar con un zombi.
        La salida (cuando se ejecuta la habilidad) es una tupla con dos elementos:
         1. Objeto de la clase Pea (un proyectil)
         2. String que identifica que la accion fue hecha por el lanzaguisantes ('peashotter')        
        """
        # Se verifica que haya zombis para disparar en su fila
        if not any(z.cy == self.pos[1] for z in zombies): 
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
        self.speed = max(6, cw // 20) #! LO MISMO ACA QUE ES ESTO
    def shoot(self):
        """
        Metodo que avanca la posicion del guisante
        """
        self.rect.move_ip(2, 0)

# 5. Cereza Bomba
class cherry(Plants):
    """
    Clase de la planta Cereza (clase hija de Plants). Su habilidad es explotar y eliminar a los zombis
    en un range 3x3 a su alrededor. Su funcion se ejecuta en ability().
    """
    def __init__(self, image_file: str, pos: tuple, cost: int=200, life: int=10):
        """
        Se toman como entradas: la ruta de la imagen (image_file), la posicion del centro 
        del objeto (pos), la ruta de la imagen de su proyectil (pea_file), el costo de la planta y su vida.
        La inicializacion es casi identica que para la clase padre Plants.       
        """
        super().__init__(image_file, pos, cost, life)
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
        self.kill() # Se elimina la planta luego de explotar
        return None, None

# 6. Papapum
class Papapum(Plants):
    """
    Clase del Papapum (clase hija de Plants). Su habilidad es explotar cuando un zombi
    lo pisa. Pero primero debe cargarse. Su funcion se ejecuta en ability().
    """
    def __init__(self, image_file_loading: str, image_file_ready: str, pos: tuple, cost: int=200, life: int=50):
        """
        Se toman como entradas: la ruta de la imagen del papapum bajo tierra (image_file_loading), la ruta de la imagen
        del papaum listo para explotar (image_file_ready), la posicion del centro 
        del objeto (pos), la ruta de la imagen de su proyectil (pea_file), el costo de la planta y su vida.
        La inicializacion es casi identica que para la clase padre Plants con la unica diferencia 
        que se tiene en cuenta la nocion de que las planta esta lista o no para explotar.       
        """
        super().__init__(image_file_loading, pos, cost, life)
        self.image_file_ready = image_file_ready
        self.transformed = False # Se setea en falso que este transformado
    def ability(self, zombies: pygame.sprite.Group) -> tuple:
        """
        Clase para la habilidad del papaum. Comienza el timer para transformarse cuando primero se 
        ejectua la funcion. Luego de 10 segundos se transforma y se activa su habilidad 
        que es que si algun zombi lo pisa muere instantaneamente. La salida es una tupla con ambos 
        elementos siendo None pues no es necesaria identificar su habilidad en el gameloop.     
        """
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
                if self.rect.collidepoint(zombie.rect.center) and zombie.type != 'balloon':
                    zombie.kill() 
                    self.kill()
        return None, None
    
# 7. Papa Giratoria (propia del modo especial)
class Spinning_Nut(Plants):
    """
    Clase de la Nuez giratorio (clase hija de Plants). Propia del modo especial, la
    Nuez rueda y elimina a los zombis en su fila. Su habilidad se ejecuta en la funcion
    ability().
    """
    def __init__(self, image_file: str, pos: tuple, cost=None, life=None, dims: tuple=(1200, 600)):
        super().__init__(image_file, pos, cost, life)
        self.speed = 0
        cw, ch = UT.cell_size()
        self.dims = dims
        raw = pygame.image.load(image_file).convert_alpha()     # Se transforma la imagen
        self.image = pygame.transform.scale(raw, (cw - 10, ch - 10))
        self.original_image = pygame.transform.scale(raw, (cw - 10, ch - 10))
        self.rect = self.image.get_rect(midright=pos)
        self.pos = pygame.Vector2(self.rect.center)  # posición flotante precisa
        self.angle = 0
        self.already_hit = False

    def ability(self):
        """
        Clase para la habilidad de la Nuez giratoria. Cada vez que se llama avanca a la Nuez.
        Cuando llega al final del trayecto es eliminada.   
        """
        self.speed = 7
        self.pos.x += self.speed  # movimiento con precisión flotante
        self.angle -= 8

        # rotar imagen
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)  # usar pos exacta como centro

        if self.rect.left >= self.dims[0]:
            self.kill()


# ────────────────────────── Podadora ──────────────────────────
class Lawnmower(pygame.sprite.Sprite):
    """
    Clase de las Podadoras (hija de la clase sprite.Sprite de pygame). Se activa cuando un zombi entra 
    en contacto con ella y avanza hasta salir de pantalla. Su movimiento se ejectua a traves del 
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
        Funcion que activa el movimiento de la podadora cuando un zombi
        entra en contacto con ella. Si se encuentra un zombi en su camino
        lo elimina inmediatamente.
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
