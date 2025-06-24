import pygame
from random import randint



# COLS, ROWS = 10, 6
#! ESTO PORQUE ESTA ACA?
GAME_OVER = pygame.USEREVENT + 4
SEED_COOLDOWN = 5_000  
def cell_size(COLS=10, ROWS=6) -> tuple:
    """
    Funcion utilizada para calcular el tamaño de las celdas. 
    """
    surface = pygame.display.get_surface()
    if surface is None:        
        return 0, 0
    w, h = surface.get_size()
    return w // COLS, h // ROWS

# Estilo del mouse:
def mouses(mouse_open: str, mouse_clicked: str) -> pygame.cursors.Cursor:
    """
    La funcion recibe como entradas las imagenes correspondientes al mouse siendo clickeado
    y si no es clickeado. Se dimensionan las imagenes y se transforma el cursor usando
    clases de pygame.
    Entradas:
        1. mouse_open (str): ruta de la imagen del mouse abierto
        2. mouse_clicked (str): ruta de la imagen del mouse clickeado
    Returns:
        1. mouse_opened (pygame.cursors.Cursor): objeto de la clase cursors.Cursor
        2. mouse_pressed (pygame.cursors.Cursor): objeto de la clase cursors.Cursor
    """
    cursor_opended = pygame.image.load(mouse_open).convert_alpha()
    cursor_opended = pygame.transform.scale(cursor_opended, (40, 40))

    cursor_pressed = pygame.image.load(mouse_clicked).convert_alpha()
    cursor_pressed = pygame.transform.scale(cursor_pressed, (40, 40))

    mouse_opened = pygame.cursors.Cursor((0, 0), cursor_opended)
    mouse_pressed = pygame.cursors.Cursor((0, 0), cursor_pressed)
    print(type(mouse_opened))
    return mouse_opened, mouse_pressed

# Partes del fondo
def background_squares(screen: pygame.surface.Surface, cols: int, rows: int, image_banner: str, 
                       image_light_square: str, image_dark_square: str) -> pygame.surface.Surface:
    """
    Funcion destinada a transformar las imagenes para las celdas claras, oscuras y el marco (parte superior).
    Se dimensionan las celdas acorde a las dimensiones de la pantalla. Se retoran las superficies para los
    3 tipos de celdas.
    Entradas:
        1. screen (pygame.surface.Surface): pantalla del usuario
        2. cols (int): cantidad de columnas
        3. rows (int): cantidad de filas
        4. image_banner (str): ruta de la imagen del banner
        5. image_light_square (str): ruta de la imagen de la celda clara
        6. image_dark_square (str): ruta de la imagen de la celda oscura
    Returns:
        1. scaled_banner (pygame.surface.Surface): superficie del marco
        2. scaled_light_square (pygame.surface.Surface): superficie de la celda clara
        3. scaled_dark_square (pygame.surface.Surface): superficie de la celdas oscuras  
    """
    width, height = screen.get_size()    # ancho y alto actuales
    cell_width  = width  // cols    # dimensiones de cada celda
    cell_height = height // rows
    # Se transforman las imagenes a superficies dimensionadas de pygame
    banner = pygame.image.load(image_banner)
    scaled_banner = pygame.transform.scale(banner, (cell_width, cell_height))

    dark_square = pygame.image.load(image_light_square).convert_alpha()
    scaled_light_square = pygame.transform.scale(dark_square, (cell_width, cell_height))

    light_square = pygame.image.load(image_dark_square).convert_alpha()
    scaled_dark_square = pygame.transform.scale(light_square, (cell_width, cell_height))
    return scaled_banner, scaled_light_square, scaled_dark_square

# Funcion para el poscionamiento de los objetos (funcion universal)
def cell_center(cols: int, rows: int, key: str, pos=None):
    """
    Funcion universal para el correcto poscionamiento de los objetos en las celdas. La funcion toma
    las columnas y filas de la pantalla. Ademas toma una key dependiendo de que se este posicionando.
    Escencialmente la funcion busca centrar los elementos en su celda correspondiente. 
    La siguiente es una lista de las keys y su uso de la variable pos
        1. plant - pos es una tupla con las coordenadas de la celda donde se quiere posicionar una planta
        2. sun - None
        3. lawnmower - pos es la fila a la cual pertence la podadora
        4. zombi - None
        5. shovel_icon - None
        6. sunflower_icon - None
        7. peashooter_icon - None
        8. nut_icon - None
        9. boomerang_icon - None
        10. cherry_icon - None
        11. papapum_icon - None
        12. suncounter_icon - None
        13. cherry_range - tupla con las coordenadas del centro de una celda en la que fue posicionada 
                            una planta cereza
        14. boomerang_range - coordenada correspondiente al eje y al que pertence el proyectil
        15. belt_icon - None
        16. belt_nut_icon - None
    Entradas:
        1. cols (int): cantidad de columnas
        2. rows (int): cantidad de filas
        3. key (str): key segun que se esta posicionando
        4. pos (None): posicion que varia su formato (tupla, int, etc) segun que se esta posicionando (key).
    Returns:
        Varia segun key, suele referirse a coordenadas centradas aunque puede variar
    """
    # ← llamamos cada vez
    cell_width, cell_height = cell_size()
    if key == 'plant': #Falta terminar
        col = pos[0] // cell_width
        row = pos[1] // cell_height
        if col == 0 or row == 0:
            return None
        return (col * cell_width + cell_width // 2,
                row * cell_height + cell_height // 2)
    elif key == 'sun':
        col = randint(1, cols - 2)
        row = randint(1, rows - 1)
        cell_x = col * cell_width
        cell_y = row * cell_height
        return (randint(cell_x, cell_x + cell_width - 1),
                randint(cell_y, cell_y + cell_height - 1))
    elif key == 'lawnmower':
        row = pos
        return (cell_width // 2,
                row * cell_height + cell_height // 2)
    elif key == 'zombie':
        row = randint(1, rows - 1)
        screen_w = pygame.display.get_surface().get_width()
        return (screen_w + 50,
                row * cell_height + cell_height // 2)
    elif key == 'shovel_icon':
        col = 9
        row = 0
        cx = col * cell_width + cell_width // 2
        cy = row * cell_height + cell_height // 2
        return (cx, cy)
    elif key == 'sunflower_icon':
        col = 2
        row = 0
        cx = col * cell_width + cell_width // 2
        cy = row * cell_height + cell_height // 2
        return (cx, cy)
    elif key == 'peashooter_icon':
        col = 3
        row = 0
        cx = col * cell_width + cell_width // 2
        cy = row * cell_height + cell_height // 2
        return (cx, cy)
    elif key == 'nut_icon':
        col = 4
        row = 0
        cx = col * cell_width + cell_width // 2
        cy = row * cell_height + cell_height // 2
        return (cx, cy)
    elif key == 'boomerang_icon':
        col = 5
        row = 0
        cx = col * cell_width + cell_width // 2
        cy = row * cell_height + cell_height // 2
        return (cx, cy)
    elif key == 'cherry_icon':
        col = 6
        row = 0
        cx = col * cell_width + cell_width // 2
        cy = row * cell_height + cell_height // 2
        return (cx, cy)
    elif key == 'papapum_icon':
        col = 7
        row = 0
        cx = col * cell_width + cell_width // 2
        cy = row * cell_height + cell_height // 2
        return (cx, cy)
    elif key == 'suncounter_icon':
        row = 0
        col = 0.5
        cx = col * cell_width + cell_width // 2
        cy = row * cell_height + cell_height // 2
        return (cx, cy) 
    elif key == 'cherry_range':
        cx, cy = pos
        # Explota en 3x3 celdas alrededor del centro (incluyendo la celda donde está la cereza)
        left = cx - cell_width // 2 - cell_width
        top = cy - cell_height // 2 - cell_height
        width = cell_width * 3
        height = cell_height * 3
        return pygame.Rect(left, top, width, height)  
    elif key == 'boomerang_range':
        col = 9
        row = pos // cell_width
        return (col * cell_width + cell_width // 2, row)
    elif key == 'belt_icon':
        row = 0
        col = 1
        cx = col * cell_width + cell_width // 2
        cy = row * cell_height + cell_height // 2
        return (cx, cy)   
    elif key == 'belt_nut_icon':
        row = 0
        col = 0
        cx = col * cell_width + cell_width // 2
        cy = row * cell_height + cell_height // 2
        return (cx, cy)