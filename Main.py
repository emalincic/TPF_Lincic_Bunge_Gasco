import sys
import random
import pygame
import os
# módulos propios
import SUNS as SN
import Plants as PL
import zombies as ZB
import DataBase as DB
import Toolbar as TL
import Gameloop as GL
import utils as UT
import game_over_menu as GOM
from utils import GAME_OVER
import Papapapapum as PP
import main_menu as MM

# ───────────────────────── modo clásico ──────────────────────────

def run_classic(start_time: int, fullscreen: bool):
    """Bucle principal del PvZ clásico. Devuelve
    • "quit"  → el jugador cerró la ventana.
    • "menu"  → terminó la partida o pantalla Game‑Over.
    """
    pygame.init()
    pygame.display.set_mode(
        (0, 0) if fullscreen else (1200, 600),
        pygame.FULLSCREEN if fullscreen else 0,
    )

    # ─── grupos de sprites ───
    sunflowers = pygame.sprite.Group()
    pea_shooters_group = pygame.sprite.Group()
    nuts_group = pygame.sprite.Group()
    peas_group = pygame.sprite.Group()
    cherry_group = pygame.sprite.Group()
    papapum_group = pygame.sprite.Group()
    boomerangs_group = pygame.sprite.Group()
    boomerangs_bullet_group = pygame.sprite.Group()
    soles_group = pygame.sprite.Group()
    zombies = pygame.sprite.Group()

    def get_all_plants():
        return (sunflowers.sprites() + pea_shooters_group.sprites() +
                nuts_group.sprites() + cherry_group.sprites() +
                papapum_group.sprites() + boomerangs_group.sprites())

    screen = pygame.display.get_surface()
    UT.Background('Images/mapa.jpg', [0, 0], screen)  # fondo

    # eventos
    SUN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SUN_EVENT, 10_000)
    ADDZOMBIE = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDZOMBIE, random.choice([5000, 7000, 9000]))
    database = DB.Zombie_types
    is_flag = True

    lawnmowers = PL.add_lawnmowers(10, 6)
    mouse_opened, mouse_pressed = UT.mouses('Images/Mouse.png', 'Images/Mouse_click.png')
    pygame.mouse.set_cursor(mouse_opened)

    sun_counter = 5000
    font = pygame.font.Font('04B_03__.TTF', 35)
    toolbar_group, toolbar_group_ghost = TL.toolbar()

    pygame.mixer.music.load(os.path.join('Audio', 'The Zombies Are coming Sound Effect.mp3'))
    pygame.mixer.music.play(0)

    clock = pygame.time.Clock()

    # ─── bucle de juego ───
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"  # ← salir de la app

            if pygame.mouse.get_pressed()[0]:
                pygame.mouse.set_cursor(mouse_pressed)
            else:
                pygame.mouse.set_cursor(mouse_opened)

            if event.type == GAME_OVER:
                GOM.show_game_over(screen)
                running = False
                break

            if event.type == SUN_EVENT:
                soles_group.add(SN.Suns('Images/sol.png'))

            if event.type == ADDZOMBIE:
                if (current_time - start_time) // 1000 >= 100 and is_flag:
                    zombies.add(ZB.Zombies(database['flag'], 'flag'))
                    pygame.time.set_timer(ADDZOMBIE, random.choice([2500, 3000, 3500]))
                    is_flag = False
                choice_key = random.choices(list(database.keys()), weights=[k['probability'] for k in database.values()])[0]
                zombie = ZB.balloon(database[choice_key], choice_key) if choice_key == 'balloon' else ZB.Zombies(database[choice_key], choice_key)
                zombies.add(zombie)

            # ---------------- barra de herramientas ----------------
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for ghost in toolbar_group_ghost:
                    if ghost.rect.collidepoint(event.pos):
                        real_card = next(card for card in toolbar_group if card.key == ghost.key)
                        if real_card.ready():
                            selected = ghost.key
                            dragging = ghost
                            orig = dragging.rect.center
                            break
                else:
                    selected = None
                    dragging = None

                for sun in soles_group:
                    if sun.rect.collidepoint(event.pos):
                        sun_counter += sun.grab()

            elif event.type == pygame.MOUSEBUTTONUP and 'dragging' in locals() and dragging:
                pos = pygame.mouse.get_pos()
                placement = UT.cell_center(10, 6, 'plant', pos)
                if selected == 'shovel_icon':
                    sun_counter += GL.shovel_action(get_all_plants(), pos)
                elif placement and not any(p.rect.center == placement for p in get_all_plants()):
                    cost = GL.plant_placement(selected, sun_counter, placement,
                                              pea_shooters_group, sunflowers, nuts_group,
                                              cherry_group, papapum_group, boomerangs_group)
                    if cost:
                        sun_counter -= cost
                        next(card for card in toolbar_group if card.key == selected).start_cooldown()
                dragging.rect.center = orig
                dragging = None
                selected = None

            elif event.type == pygame.MOUSEMOTION and 'dragging' in locals() and dragging:
                dragging.rect.center = event.pos

        # -------------- updates y render --------------
        GL.update_grid(10, 6, screen)
        GL.update_peas(peas_group, boomerangs_bullet_group, screen)
        GL.update_plants(get_all_plants(), zombies, peas_group,
                         soles_group, boomerangs_bullet_group, screen)
        GL.udpate_zombies(zombies, get_all_plants(), peas_group,
                         boomerangs_bullet_group, screen)
        GL.update_suns(soles_group, screen)
        GL.update_lawnmowers(lawnmowers, zombies, screen)

        toolbar_group.update()
        toolbar_group_ghost.draw(screen)
        toolbar_group.draw(screen)

        counter = font.render(str(sun_counter), True, (255, 255, 255))
        counter_sprite = list(toolbar_group)[-1]
        screen.blit(counter, counter.get_rect(center=(counter_sprite.rect.centerx+35, counter_sprite.rect.centery+5)))

        pygame.display.flip()
        clock.tick(60)

    return "menu"   # terminó la partida


# ──────────────────────── lanzador principal ────────────────────────

if __name__ == "__main__":
    while True:
        (mode, aux), fullscreen = MM.main_menu()

        if mode == "classic":
            result = run_classic(aux, fullscreen)
        elif mode == "papapum":
            result = PP.run_papapum(fullscreen)
        else:
            result = "menu"

        if result == "quit":
            pygame.quit()
            sys.exit()
