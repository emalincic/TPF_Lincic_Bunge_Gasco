import os
import pygame
import sys
from random import choice, choices
import Gameloop as GL
import Toolbar as TL
import zombies as ZB
import utils as UT
import Main
import game_over_menu as GOM
from utils import GAME_OVER
import json

# TODO Intizialize pygame
def papapum():
    pygame.init()
    frames = pygame.time.Clock()
    # Creamos ventana
    screen = pygame.display.get_surface()  # ← no crea otra
    pygame.display.set_caption('Plants vs Zombies')

    #* Sprites Groups de la cinta transportadora y los seed packets de la nuez
    belt_group, nuts_toolbar_group, nuts_group_ghost = TL.special_delivery()
    #* Grupo de las nueces al momento de lanzarse
    nuts_group = pygame.sprite.Group()
    #*  Grupo de los Zombies
    zombies = pygame.sprite.Group()
    
    # Partes del fondo
    marco, claro, oscuro = UT.background_squares(
        screen, 10, 6, 'Images/marco_marron.png', 
        'Images/celda_verde_claro.png', 
        'Images/celda_verde_oscuro.png')

    # Evento personalizado para la aparición de zombies
    ADDZOMBIE = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDZOMBIE, choice([4000, 5000]))
    # Utilización de la base de datos de los zombies
    with open("DataBase.json") as file:
        database = json.load(file)

    # Evento personalizado para la aparición de nueces (seed packets)
    ADDNUT = pygame.USEREVENT + 3
    pygame.time.set_timer(ADDNUT, choice([7000, 8000, 10000]))


    # Obtenemos los estilos del mouse
    mouse_opened, mouse_pressed = UT.mouses('Images/Mouse.png', 'Images/Mouse_click.png')
    pygame.mouse.set_cursor(mouse_opened)

    
    # Cálculos de tamaños para utilizarse luego
    cell_w, cell_h = UT.cell_size()
    seed_size = (int(cell_h * 1.10), int(cell_h))

    # Zombies are coming efecto de sonido
    pygame.mixer.music.load(os.path.join("Audio", "The Zombies Are coming Sound Effect.mp3"))
    pygame.mixer.music.play(0) # Se reproduce una vez
    

    
    is_flag = False # Confirmación si la oleada ya sucedió
    run = True # Verificación de que el juego corra
    dragging = None # Elemeto de la toolbar draggeado

    while run:
        events = pygame.event.get()
        current_time = pygame.time.get_ticks()

        for event in events:
            # Mouse abierto o mouse cerrado
            if pygame.mouse.get_pressed()[0]:
                pygame.mouse.set_cursor(mouse_pressed)
            else:
                pygame.mouse.set_cursor(mouse_opened)
            # Si cierra la ventana se cierra el juego
            if event.type == pygame.QUIT:
                run = False

            # Si pierde se abre la pantalla de 'game over'
            elif event.type == GAME_OVER:               
                GOM.show_game_over(screen)   
                run = False 
                Main.main_menu()
            
            # Se agrega un zombie si se cumple el evento
            elif event.type == ADDZOMBIE:
                # Cronómetro para la oleada
                if (current_time) // 1000 >= 150 and not is_flag:
                        flag = ZB.Zombies(database['flag'], 'flag')
                        zombies.add(flag)
                        pygame.mixer.music.load('Audio\The Zombies Are coming Sound Effect.mp3')
                        pygame.mixer.music.play(0)
                        pygame.time.set_timer(ADDZOMBIE, choice([1500, 2000, 2500])) # Más zombies aparecen
                        pygame.time.set_timer(ADDNUT, choice([4000, 5000, 6000])) # Más nueces aparecen (menos proporción)
                        is_flag = True 

                # Zombie aleatorio según su probabilidad
                random_z = choices(list(database.keys()), weights=[k['probability'] for k in database.values()])[0]
                its_time_for_zombies = ZB.Zombies(database[random_z], random_z)
                zombies.add(its_time_for_zombies)

            # Aparece una nuez en la cinta si se cumple el evento
            elif event.type == ADDNUT:
                new_nut = TL.Delivery('NT_seedpacket.png', 'belt_nut_icon', (seed_size[0]-15, seed_size[1]-15))
                new_ghost_nut = TL.Delivery_Ghost('Nut.png', 'belt_icon', (seed_size[0]-15, seed_size[1]-15))
                nuts_toolbar_group.add(new_nut)
                nuts_group_ghost.add(new_ghost_nut)

            # Evento del mouse
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Arrastrado de la nuez a la zona de juego
                for (nut, nut_ghost) in zip(nuts_toolbar_group,nuts_group_ghost):
                    if nut.rect.collidepoint(event.pos):
                        dragging = nut_ghost
                        dragging.speed = 0
                        original_pos = dragging.rect.center

            # Si se suelta el click luego de tener una planta
            elif event.type == pygame.MOUSEBUTTONUP and dragging:
                # Tomamos posicion del mouse y placement si se busca ubicar una planta
                pos = pygame.mouse.get_pos()
                placement = UT.cell_center(10, 6, 'plant', pos)
                if placement:
                    GL.nut_placement(placement, nuts_group, nuts_toolbar_group)
                    dragging.rect.center = original_pos
                    dragging.kill()
                dragging = None
            
            # Se mueve la planta fantasma en la posición del mause
            elif event.type == pygame.MOUSEMOTION and dragging:
                dragging.rect.center = (event.pos)
                
        
        
        # SE ACTUALIZAN LOS OBJETOS
        # Dibujar grilla 10x6 dinámica
        GL.update_grid(10, 6, screen, marco, oscuro, claro)
        # Actualizamos acciones de las plantas
        belt_group.draw(screen)
        GL.update_nuts(nuts_toolbar_group,belt_group,nuts_group_ghost,nuts_group, screen, dragging)
        was_placed = False
        # Actualizamos acciones de los zombies
        GL.update_zombies_papum(nuts_group, zombies, screen)
        
        frames.tick(60)
        pygame.display.update()

    pygame.quit() 
    sys.exit()

