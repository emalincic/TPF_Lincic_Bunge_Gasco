import pygame
import random
import BC
import SUNS
from pygame.locals import RLEACCEL

# Inicializamos pygame
pygame.init()

# Creamos ventana
dims = (800, 600)
screen = pygame.display.set_mode(dims)
pygame.display.set_caption('Plants vs Zombies')

# Creamos el mapa según la imagen
mapa = BC.Background('Images/mapa.jpg', [0, 0], dims)

# Evento personalizado para los soles
SUN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SUN_EVENT, 5000)

# Grupo de soles
soles = pygame.sprite.Group()

# Clase Lawnmower
class Lawnmower(pygame.sprite.Sprite):
    def __init__(self, image_file, dims=(800, 600)):
        super(Lawnmower, self).__init__()
        non_dimmed = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(non_dimmed, (45, 45))


# ========================
# MENÚ PRINCIPAL
# ========================
def main_menu():
    font = pygame.font.SysFont("arial", 50)
    button_rect = pygame.Rect(300, 250, 200, 60)
    clicked = False

    while not clicked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    clicked = True

        screen.fill((34, 177, 76))  # Fondo verde

        title_text = font.render("Plants vs Zombies", True, (255, 255, 255))
        play_text = font.render("Jugar", True, (0, 0, 0))

        screen.blit(title_text, (200, 100))
        pygame.draw.rect(screen, (255, 255, 0), button_rect)  # Botón amarillo
        screen.blit(play_text, (button_rect.x + 40, button_rect.y + 5))

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
    screen.fill((0, 0, 0))
    screen.blit(mapa.image, mapa.rect)

    for sol in soles:
        sol.action()
        screen.blit(sol.image, sol.rect)

    print(sun_counter)
    pygame.display.update()

pygame.quit()