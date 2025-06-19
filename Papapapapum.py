import sys
import os
import pygame
from random import choice, choices

import DataBase as DB
import Gameloop as GL
import Toolbar as TL
import zombies as ZB
import utils as UT
import SUNS as SN

# ───────────────────────── modo Papapum ──────────────────────────

def run_papapum(fullscreen: bool):
    """Modo cinta transportadora. Devuelve
    • "quit" → el jugador cerró la ventana.
    • "menu" → terminó la partida y desea volver al menú."""

    pygame.init()
    pygame.display.set_mode(
        (0, 0) if fullscreen else (1200, 600),
        pygame.FULLSCREEN if fullscreen else 0,
    )
    screen = pygame.display.get_surface()
    pygame.display.set_caption('Plants vs Zombies — Papapum')

    # grupos/elementos
    belt_group, nuts_toolbar_group, nuts_group_ghost = TL.special_delivery()
    nuts_group   = pygame.sprite.Group()
    zombies      = pygame.sprite.Group()

    # eventos
    ADDZOMBIE = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDZOMBIE, choice([3000, 4000, 5000]))
    ADDNUT    = pygame.USEREVENT + 3
    pygame.time.set_timer(ADDNUT, choice([7000, 8000, 10000]))

    database = DB.Zombie_types
    is_flag = True

    # cursores
    mouse_opened, mouse_pressed = UT.mouses('Images/Mouse.png', 'Images/Mouse_click.png')
    pygame.mouse.set_cursor(mouse_opened)

    pygame.mixer.music.load(os.path.join('Audio', 'The Zombies Are coming Sound Effect.mp3'))
    pygame.mixer.music.play(0)

    cell_w, cell_h = UT.cell_size()
    seed_size = (int(cell_h * 1.10), int(cell_h))

    dragging = None
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if pygame.mouse.get_pressed()[0]:
                pygame.mouse.set_cursor(mouse_pressed)
            else:
                pygame.mouse.set_cursor(mouse_opened)

            # ───── spawns ─────
            if event.type == ADDZOMBIE:
                if pygame.time.get_ticks() // 1000 >= 100 and is_flag:
                    zombies.add(ZB.Zombies(database['flag'], 'flag'))
                    pygame.time.set_timer(ADDZOMBIE, choice([1500, 2000, 2500]))
                    is_flag = False
                key = choices(list(database.keys()), weights=[v['probability'] for v in database.values()])[0]
                zombies.add(ZB.Zombies(database[key], key))

            if event.type == ADDNUT:
                nuts_toolbar_group.add(TL.Delivery('NT_seedpacket.png', 'belt_nut_icon', (seed_size[0]-15, seed_size[1]-15)))
                nuts_group_ghost.add(TL.Delivery_Ghost('Nut.png', 'belt_icon', (seed_size[0]-15, seed_size[1]-15)))

            # ───── drag‑and‑drop de nuts ─────
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for nut, nut_ghost in zip(nuts_toolbar_group, nuts_group_ghost):
                    if nut.rect.collidepoint(event.pos):
                        dragging = nut_ghost
                        dragging.speed = 0
                        original_pos = dragging.rect.center
                        break

            if event.type == pygame.MOUSEBUTTONUP and dragging:
                placement = UT.cell_center(10, 6, 'plant', event.pos)
                if placement:
                    GL.nut_placement(placement, nuts_group, nuts_toolbar_group)
                    dragging.rect.center = original_pos
                    dragging.kill()
                dragging = None

            if event.type == pygame.MOUSEMOTION and dragging:
                dragging.rect.center = event.pos

        # ───── updates / render ─────
        GL.update_grid(10, 6, screen)
        belt_group.draw(screen)
        GL.update_nuts(nuts_toolbar_group, belt_group, nuts_group_ghost, nuts_group, screen, dragging)
        GL.update_zombies_papum(nuts_group, zombies, screen)

        pygame.display.flip()
        clock.tick(60)

    return "menu"   # nunca se ejecuta hoy, pero dejamos consistente


# ───────────────────────── ejecución directa ─────────────────────────

if __name__ == "__main__":
    print(run_papapum(False))
