import pygame
import sys
import os

# ───────────────────────── helpers ──────────────────────────

def _hover_color(col: tuple[int, int, int]) -> tuple[int, int, int]:
    """Genera un color de hover perceptible. 
    Si el color es muy brillante (ej.: amarillo puro), lo oscurece; 
    si es medio/oscuro, lo aclara."""
    r, g, b = col
    bright = r + g + b > 600
    delta  = 70  # intensidad de cambio
    if bright:
        g = max(g - delta, 0)
        b = max(b - delta, 0)
    else:
        r = min(r + delta, 255)
        g = min(g + delta, 255)
        b = min(b + delta, 255)
    return (r, g, b)


def draw_button(surf: pygame.Surface, rect: pygame.Rect, bg_color: tuple[int, int, int],
                text_surf: pygame.Surface, *, border: int = 3, radius: int = 12,
                hover: bool = False):
    """Botón redondeado con contorno, sombra y color de hover."""
    if hover:
        bg_color = _hover_color(bg_color)

    # sombra discreta
    shadow = rect.copy().move(4, 4)
    pygame.draw.rect(surf, (0, 0, 0, 90), shadow, border_radius=radius)

    # cuerpo + contorno
    pygame.draw.rect(surf, bg_color, rect, border_radius=radius)
    pygame.draw.rect(surf, (0, 0, 0), rect, border, border_radius=radius)

    # texto centrado
    surf.blit(text_surf, text_surf.get_rect(center=rect.center))


# ───────────────────────── main menu ─────────────────────────

def main_menu():
    pygame.init()
    default_dims = (1200, 600)
    screen = pygame.display.set_mode(default_dims)
    pygame.display.set_caption("TPF PvZ")

    # fuentes (título más grande y grueso)
    title_font = pygame.font.Font("04B_03__.TTF", 90)
    btn_font   = pygame.font.Font("04B_03__.TTF", 30)

    # sonidos
    pygame.mixer.music.load(os.path.join("Audio", "Main Menu - Plants vs. Zombies 2.mp3"))
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(-1)

    fullscreen = False

    # textos precalculados
    txt_play     = btn_font.render("Jugar",    True, (0, 0, 0))
    txt_papapum  = btn_font.render("Papapum",  True, (0, 0, 0))
    txt_full     = btn_font.render("Pantalla Completa", True, (0, 0, 0))
    txt_window   = btn_font.render("Modo Ventana",      True, (0, 0, 0))

    # tamaños de botones
    btn_play_size    = (200, 60)
    btn_papapum_size = (350, 60)
    btn_toggle_size  = (300, 50)
    margin           = 20

    clock = pygame.time.Clock()

    while True:
        start_time = pygame.time.get_ticks()
        width, height = screen.get_size()
        center_y = int(height * 0.65)

        btn_play_rect = pygame.Rect(0, 0, *btn_play_size)
        btn_play_rect.center = (int(width * 0.25), center_y)

        btn_papapum_rect = pygame.Rect(0, 0, *btn_papapum_size)
        btn_papapum_rect.center = (int(width * 0.75), center_y)

        btn_toggle_rect = pygame.Rect(
            width - btn_toggle_size[0] - margin,
            margin,
            *btn_toggle_size,
        )

        # ───── event loop ─────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_play_rect.collidepoint(event.pos):
                    return start_time, fullscreen
                elif btn_papapum_rect.collidepoint(event.pos):
                    return "papapum", fullscreen
                elif btn_toggle_rect.collidepoint(event.pos):
                    fullscreen = not fullscreen
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) if fullscreen else pygame.display.set_mode(default_dims)

        # ───── drawing ─────
        fondo = pygame.image.load("Images/pvz_udesa.jpeg").convert()
        fondo = pygame.transform.scale(fondo, (width, height))
        screen.blit(fondo, (0, 0))

        # título con sombra destacada
        title_white  = title_font.render("Plants vs Zombies", True, (255, 255, 255))
        title_shadow = title_font.render("Plants vs Zombies", True, (0, 0, 0))
        title_pos = title_white.get_rect(midtop=(width // 2, 80))
        screen.blit(title_shadow, title_pos.move(4, 4))
        screen.blit(title_white,  title_pos)

        mouse_pos = pygame.mouse.get_pos()

        draw_button(screen, btn_play_rect, (100, 255, 0), txt_play,
                    hover=btn_play_rect.collidepoint(mouse_pos))

        draw_button(screen, btn_papapum_rect, (180, 255, 0), txt_papapum,
                    hover=btn_papapum_rect.collidepoint(mouse_pos))

        draw_button(screen, btn_toggle_rect, (150, 255, 0),
                    txt_full if not fullscreen else txt_window,
                    hover=btn_toggle_rect.collidepoint(mouse_pos), radius=8)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    print(main_menu())