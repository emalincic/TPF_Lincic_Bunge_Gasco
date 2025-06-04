import pygame

def main_menu():
    dims = (1200, 600)
    screen = pygame.display.set_mode(dims)
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