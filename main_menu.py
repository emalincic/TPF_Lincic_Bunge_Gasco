import pygame
import sys
import os

def main_menu():
    pygame.init()
    default_dims = (1200, 600)
    screen = pygame.display.set_mode(default_dims)
    pygame.display.set_caption("TPF PvZ")
    font = pygame.font.Font("04B_03__.TTF", 50)
    btn_font = pygame.font.Font("04B_03__.TTF", 25)   

    btn_play_size   = (200, 60)
    btn_toggle_size = (300, 50)   # ancho suficiente para el texto
    margin = 20

    fullscreen = False

    pygame.mixer.music.load(os.path.join('Audio', 'Main Menu - Plants vs. Zombies 2.mp3'))
    pygame.mixer.music.set_volume(1.0) 
    pygame.mixer.music.play(-1)
    
    while True:
        start_time = pygame.time.get_ticks()
        # Obtengo tamaño dinámico en cada iteración
        width, height = screen.get_size()

        # Defino rects de botones
        btn_play   = pygame.Rect(600, 450, *btn_play_size)
        btn_toggle = pygame.Rect(
            width  - btn_toggle_size[0] - margin,  # x: pantalla_ancho - ancho_boton - margen
            margin,                                # y: margen superior
            *btn_toggle_size
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_play.collidepoint(event.pos):
                    return start_time,fullscreen # sale del menú y arranca el juego

                elif btn_toggle.collidepoint(event.pos):
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode(default_dims)

        # Dibujo de fondo y botones
        fondo = pygame.image.load("Images/pvz_udesa.jpeg").convert()
        fondo = pygame.transform.scale(fondo, (width, height))
        screen.blit(fondo, (0, 0))

        title_text = font.render("Plants vs Zombies", True, (255, 255, 255))
        screen.blit(title_text, (200, 100))

        # Botón Jugar
        pygame.draw.rect(screen, (255, 255, 0), btn_play)
        play_text = font.render("Jugar", True, (0, 0, 0))
        screen.blit(play_text, (btn_play.x + 40, btn_play.y + 5))

        # Botón Toggle Fullscreen en esquina superior derecha
        pygame.draw.rect(screen, (150, 255, 0), btn_toggle)
        label = "Pantalla Completa" if not fullscreen else "Modo Ventana"
        toggle_text = btn_font.render(label, True, (0, 0, 0))
        # Centrar texto verticalmente en el botón
        text_x = btn_toggle.x + 10
        text_y = btn_toggle.y + (btn_toggle.height - toggle_text.get_height()) // 2
        screen.blit(toggle_text, (text_x, text_y))

        pygame.display.flip()
        pygame.time.Clock().tick(60)