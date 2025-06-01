import pygame
import random
import BC
import SUNS
from pygame.locals import RLEACCEL

# Inicializamos pygame
pygame.init()

# Creamos ventana
dims = (1200, 600)
screen = pygame.display.set_mode(dims)
pygame.display.set_caption('Plants vs Zombies')

# Creamos el mapa según la imagen
mapa = BC.Background('Images/mapa.jpg', [0, 0], dims)

# Evento personalizado para los soles
SUN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SUN_EVENT, 5000)

# Grupo de soles
soles = pygame.sprite.Group()




# ========================
# MENÚ PRINCIPAL
# ========================
def main_menu():
    font = pygame.font.SysFont("impact", 50)
    button_rect = pygame.Rect(600, 450, 200, 60)
    button_config = pygame.Rect(250, 480, 350, 60)
    clicked = False

    while not clicked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    clicked = True
    
         
        fondo = pygame.image.load("Images/pvz_udesa.jpeg").convert()
        fondo = pygame.transform.scale(fondo, dims)  # opcional: adapta la imagen al tamaño de la pantalla
        screen.blit(fondo, (0, 0))
        title_text = font.render("Plants vs Zombies", True, (255, 255, 255))
        play_text = font.render("Jugar", True, (0, 0, 0))
        config_text = font.render("Configuracion", True, (0, 0, 0))
        screen.blit(title_text, (200, 100))
        pygame.draw.rect(screen, (255, 255, 0), button_rect)  # Botón amarillo
        screen.blit(play_text, (button_rect.x + 40, button_rect.y + 5))
        

        pygame.draw.rect(screen, (150, 255, 0), button_config)  
        screen.blit(config_text, (button_config.x + 10, button_config.y ))
        

        pygame.display.flip()


# Ejecutamos menú principal antes del juego
main_menu()

# ========================
# LOOP PRINCIPAL DEL JUEGO
# ========================
run = True
sun_counter = 0
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == SUN_EVENT:
            new_sun = SUNS.Suns('Images/sol.png')
            soles.add(new_sun)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for sol in soles:
                if sol.rect.collidepoint(event.pos):
                    sun_counter += sol.grab()

    soles.update()
    ##screen.fill((0, 0, 0))
    ##screen.blit(mapa.image, mapa.rect)

    screen.fill((50, 120, 50))  # Fondo verde (opcional)

    # Dibujar grilla 9x5
    cols = 10
    rows = 6
    cell_width = dims[0] // cols   # 1200 / 9 = 133
    cell_height = dims[1] // rows  # 600 / 5 = 120

    for i in range(cols):
        for j in range(rows):
            rect = pygame.Rect(i * cell_width, j * cell_height, cell_width, cell_height)
            pygame.draw.rect(screen, (0, 100, 0), rect, 2)  # Borde verde oscuro
    for sol in soles:
        sol.action()
        screen.blit(sol.image, sol.rect)

    print(sun_counter)
    pygame.display.update()

pygame.quit() 