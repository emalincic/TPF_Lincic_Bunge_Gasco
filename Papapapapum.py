import pygame
import os
from random import choice, choices
import DataBase as DB
import Gameloop as GL
# import Borrador as BR
import Toolbar as TL
# import main_menu as MM
import zombies as ZB
import utils as UT
import SUNS as SN

# Ejecutamos menú principal antes del juego
# start_time, fullscreen = MM.main_menu() 
# TODO Intizialize pygame
pygame.init()


default_dims = (1200, 600)
screen = pygame.display.set_mode(default_dims)
belt_group, nuts_toolbar_group, nuts_group_ghost = TL.special_delivery()
nuts_group = pygame.sprite.Group()
#* Grupon de los Zombies
zombies = pygame.sprite.Group()
# screen = pygame.display.get_surface()  # ← no crea otra
# dims   = screen.get_size()   
pygame.display.set_caption('Plants vs Zombies')

ADDZOMBIE = pygame.USEREVENT + 2
pygame.time.set_timer(ADDZOMBIE, choice([3000, 4000, 5000]))
is_flag = True
database = DB.Zombie_types

ADDNUT = pygame.USEREVENT + 3
pygame.time.set_timer(ADDNUT, choice([7000, 8000, 10000]))


cursor_opended = pygame.image.load('Images/Mouse.png').convert_alpha()
cursor_opended = pygame.transform.scale(cursor_opended, (40, 40))

cursor_pressed = pygame.image.load('Images/Mouse_click.png').convert_alpha()
cursor_pressed = pygame.transform.scale(cursor_pressed, (40, 40))

mouse_opened = pygame.cursors.Cursor((0, 0), cursor_opended)
mouse_pressed = pygame.cursors.Cursor((0, 0), cursor_pressed)

pygame.mouse.set_cursor(mouse_opened)

run = True

frames = pygame.time.Clock()
    
pygame.mixer.music.load('Audio\The Zombies Are coming Sound Effect.mp3') 
pygame.mixer.music.play(0)

cell_w, cell_h = UT.cell_size()


seed_size = (int(cell_h * 1.10), int(cell_h))

selected_object = None
dragging = None
was_placed = False
while run:
    events = pygame.event.get()
    current_time = pygame.time.get_ticks()
    for event in events:
        if pygame.mouse.get_pressed()[0]:
            pygame.mouse.set_cursor(mouse_pressed)
        else:
            pygame.mouse.set_cursor(mouse_opened)
            
        if event.type == pygame.QUIT:
            run = False
        
        elif event.type == ADDZOMBIE:
            if (current_time) // 1000 >= 100 and is_flag:
                    flag = ZB.Zombies(DB.Zombie_types['flag'], 'flag')
                    zombies.add(flag)
                    
                    pygame.mixer.music.load('Audio\The Zombies Are coming Sound Effect.mp3')
                    pygame.mixer.music.play(0)
                    pygame.time.set_timer(ADDZOMBIE, choice([1500, 2000, 2500]))
                    is_flag = False 
                    
            random_z = choices(list(database.keys()), weights=[k['probability'] for k in database.values()])[0]
            its_time_for_zombies = ZB.Zombies(database[random_z], random_z)
            zombies.add(its_time_for_zombies)
    
        elif event.type == ADDNUT:
            new_nut = TL.Delivery('NT_seedpacket.png', 'belt_nut_icon', (seed_size[0]-15, seed_size[1]-15))
            new_ghost_nut = TL.Delivery_Ghost('Nut.png', 'belt_icon', (seed_size[0]-15, seed_size[1]-15))
            nuts_toolbar_group.add(new_nut)
            nuts_group_ghost.add(new_ghost_nut)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for (nut, nut_ghost) in zip(nuts_toolbar_group,nuts_group_ghost):
                if nut.rect.collidepoint(event.pos):
                    dragging = nut_ghost
                    dragging.speed = 0
                    original_pos = dragging.rect.center

        elif event.type == pygame.MOUSEBUTTONUP and dragging:
            pos = pygame.mouse.get_pos()
            placement = SN.cell_center(10, 6, 'plant', pos)
            if placement:
                GL.nut_placement(placement, nuts_group, nuts_toolbar_group)
                dragging.rect.center = original_pos
                dragging.kill()
            dragging = None
        elif event.type == pygame.MOUSEMOTION and dragging:
            dragging.rect.center = (event.pos)
            
    
    
    # SE ACTUALIZAN LOS OBJETOS
    # Dibujar grilla 10x6 dinámica
    GL.update_grid(10, 6, screen)
    # Actualizamos acciones de las plantas
    belt_group.draw(screen)
    GL.update_nuts(nuts_toolbar_group,belt_group,nuts_group_ghost,nuts_group, screen, dragging)
    was_placed = False
    # Actualizamos acciones de los zombies
    GL.update_zombies_papum(nuts_group, zombies, screen)
    
    frames.tick(60)
    pygame.display.update()

pygame.quit() 
