import os
import pygame
from random import choice, choices
import sys
import Plants as PL
import zombies as ZB
import zombies as ZB
import Main
import Toolbar as TL
import Gameloop as GL
import utils as UT
import game_over_menu as GOM
from utils import GAME_OVER
import json



def Clasic():
    
    # TODO Intizialize pygame
    pygame.init()
    # Temporizador del menú princpal
    start_time = Main.time_counter()
    frames = pygame.time.Clock()
    #* Grupos de las Plantas
    sunflowers = pygame.sprite.Group()
    pea_shooters_group = pygame.sprite.Group()
    nuts_group = pygame.sprite.Group()
    peas_group = pygame.sprite.Group()
    cherry_group = pygame.sprite.Group()
    papapum_group = pygame.sprite.Group()
    boomerangs_group = pygame.sprite.Group()
    boomerangs_bullet_group = pygame.sprite.Group()
    #* Grupos de las explosiones 
    explosions_group = pygame.sprite.Group()

    #* Grupo de los soles
    soles_group = pygame.sprite.Group()
    #* Grupon de los Zombies
    zombies = pygame.sprite.Group()

    lawnmowers = PL.add_lawnmowers(10, 6)
    toolbar_group, toolbar_group_ghost = TL.toolbar()

    def get_all_plants() -> list:
        """
        Funcion dinamica que retorna los spirtes de todas las plantas en forma de lista para su proximo uso.
        Returns:
            1. Lista con sprites de las plantas
        """
        return sunflowers.sprites() + pea_shooters_group.sprites() + nuts_group.sprites() + cherry_group.sprites() + papapum_group.sprites() + boomerangs_group.sprites()
    
    # Creamos ventana
    screen = pygame.display.get_surface()  # ← no crea otra
    pygame.display.set_caption('Plants vs Zombies')

    # Partes del fondo
    marco, claro, oscuro = UT.background_squares(
        screen, 10, 6, 'Images/marco_marron.png', 
        'Images/celda_verde_claro.png', 
        'Images/celda_verde_oscuro.png')
    
    # Evento personalizado para los soles
    SUN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SUN_EVENT, 10000)

    # Eventos de los zombies
    ADDZOMBIE = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDZOMBIE, choice([7000, 8000, 9000]))
    with open("DataBase.json") as file:
        database = json.load(file)

    # Gestión de oleadas
    def iniciar_oleada(level: int, database: dict):
        """
        Función que maneja las oleadas adecatendo el tiempo de aparición de los zombies
        Entradas:
            1. level (int): nivel de la oleada
            2. database (dict): Diccionario de la base de datos.
        Returns: -
        """
        flag = ZB.Zombies(database['flag'], 'flag')
        zombies.add(flag)
        pygame.mixer.music.load(os.path.join('Audio', 'The Zombies Are coming Sound Effect.mp3'))
        pygame.mixer.music.play(0)
        for k, v in database.items():
            if k != 'Normal' and k != 'flag':
                if k == "Balloon":
                    v['probability'] += 0.3
                v['probability'] += 0.15
        if level == 1:
            pygame.time.set_timer(ADDZOMBIE,choice([2500, 3000, 3500]))
        elif level == 2:
            pygame.time.set_timer(ADDZOMBIE, choice([1000, 1500]))
            

    # Obtenemos los estilos del mouse
    mouse_opened, mouse_pressed = UT.mouses(
        os.path.join('Images', 'Mouse.png'), 
        os.path.join('Images', 'Mouse_click.png'))
    pygame.mouse.set_cursor(mouse_opened)

    # Llamada de los zombis incial 
    pygame.mixer.music.load('Audio\The Zombies Are coming Sound Effect.mp3')
    pygame.mixer.music.play(0)

    # Características del contador
    font = pygame.font.Font(os.path.join("Fonts", "04B_03__.TTF"), 35) 
    sun_counter = 50

    # Gestión de atributos
    wave_level = 1
    selected_object = None  #|-> Selección del objeto de la barra de plantas
    dragging = None         #|

    # Loop principal
    run = True
    while run:
        current_time = pygame.time.get_ticks()
        temp = (current_time - start_time) // 1000
        events = pygame.event.get()
        
        for event in events:
            # Mouse abierto o mouse cerrado
            if pygame.mouse.get_pressed()[0]: pygame.mouse.set_cursor(mouse_pressed)
            else: pygame.mouse.set_cursor(mouse_opened)

            # Si cierra la venta se cierra el juego   
            if event.type == pygame.QUIT:
                run = False
            
            # Vuelve al menú principal al apretar escape
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False 
                    Main.main_menu()
            
            # Si pierde se abre la pantalla de 'game over'
            elif event.type == GAME_OVER:               
                GOM.show_game_over(screen)   
                run = False 
                Main.main_menu()

            # Se agrega sol si se cumple el evento
            elif event.type == SUN_EVENT:
                new_sun = PL.Suns('Images/sol.png')
                soles_group.add(new_sun)
            
            # Se agrega zombie si se cumple el evento
            elif event.type == ADDZOMBIE:
                if 150 <= temp < 300 and wave_level == 1:
                    iniciar_oleada(wave_level, database)
                    wave_level = 2

                elif temp >= 300 and wave_level == 2:
                    iniciar_oleada(wave_level, database)
                    wave_level = 3

                # Se agrega zombi random
                random_z = choices(list(database.keys()), weights=[k['probability'] for k in database.values()])[0]
                if random_z == 'Balloon':
                    its_time_for_zombies = ZB.balloon(database[random_z], random_z)
                else:
                    its_time_for_zombies = ZB.Zombies(database[random_z], random_z)
                zombies.add(its_time_for_zombies)
            
            # Eventos del mouse
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for item, item_ghost in zip(toolbar_group, toolbar_group_ghost):
                    if item.rect.collidepoint(event.pos):
                        real_card = next(card for card in toolbar_group if card.key == item_ghost.key)
                        # Si no se acabo el cooldown se puede seleccionar
                        if real_card.ready():           
                            selected_object = item.key
                            dragging = item_ghost
                            original_pos = dragging.rect.center
                        else:               
                            pass

                # Si se clickea sol se recoge y se agrega al contador 50 soles     
                for sol in soles_group:
                    if sol.rect.collidepoint(event.pos):
                        sun_counter += sol.grab()

            elif event.type == pygame.MOUSEBUTTONUP and dragging:
                # Tomamos posicion del mouse y placement si se busca ubicar una planta
                pos = pygame.mouse.get_pos()
                placement = UT.cell_center(10, 6, 'plant', pos)

                # Se chequea si la pala recoge una planta
                if selected_object == 'shovel_icon' : 
                    sun_counter += GL.shovel_action(get_all_plants(), pos)

                # Se chequea que no haya plantas donde se quiere ubicar la planta
                elif placement is not None and not any(p.rect.center == placement for p in get_all_plants()):
                    cost = GL.plant_placement(
                        selected_object, sun_counter, placement,
                        pea_shooters_group, sunflowers, nuts_group, cherry_group, papapum_group, boomerangs_group)
                    # Se deducen los costos de ubicar la planta al contador                                       
                    if cost:                                
                        sun_counter -= cost                
                        for card in toolbar_group:          
                            if card.key == selected_object: 
                                card.start_cooldown()       
                                break                       
                # Reset del dragging
                dragging.rect.center = original_pos
                dragging = None            
                selected_object = None

            elif event.type == pygame.MOUSEMOTION and dragging:
                dragging.rect.center = (event.pos)


        # ACTUALIZACIÓN DE OBJETOS
        # Dibujar grilla 10x6 dinámica
        GL.update_grid(10, 6, screen, marco, oscuro, claro)
        # Actualizamos la posicion de los guisantes
        GL.update_peas(peas_group, boomerangs_bullet_group, screen)
        # Actualizamos acciones de las plantas
        GL.update_plants(get_all_plants(), zombies, peas_group, soles_group, boomerangs_bullet_group, explosions_group, screen)
        # Actualizamos acciones de los zombies
        GL.update_zombies(zombies, get_all_plants(), peas_group, boomerangs_bullet_group, screen)
        # Actualizamos los soles
        GL.update_suns(soles_group, screen)
        # Actaulizamos las cosechadoras
        GL.update_lawnmowers(lawnmowers, zombies, screen)
        # Actualizamos las explosiones
        for explosion in explosions_group: explosion.update_screen_boom(screen)
        
        toolbar_group.update()  
        toolbar_group_ghost.draw(screen)
        toolbar_group.draw(screen)
        # Convertir el contador a imagen de texto
        counter = font.render(str(sun_counter), True, (255, 255, 255))  # Blanco
        # Mostrarlo en pantalla, por ejemplo en la esquina superior izquierda
        counter_sprite = list(toolbar_group)[-1]
        counter_center = counter.get_rect(center=counter_sprite.rect.center)
        screen.blit(counter, (counter_center[0]+35, counter_center[1]+5))
        frames.tick(60) # Limitar a 60 FPS
        pygame.display.update()
    pygame.quit() 
    sys.exit()
