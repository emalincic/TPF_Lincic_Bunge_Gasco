import pygame
from random import choice, choices
import DataBase as DB
import Gameloop as GL
# import Borrador as BR
import Toolbar as TL
# import main_menu as MM
import zombies as ZB

# Ejecutamos menú principal antes del juego
# start_time, fullscreen = MM.main_menu() 
# TODO Intizialize pygame
pygame.init()
peas_group = pygame.sprite.Group()
soles_group = pygame.sprite.Group()
belt, nuts = TL.special_delivery()
#* Grupon de los Zombies
zombies = pygame.sprite.Group()



default_dims = (1200, 600)
screen = pygame.display.set_mode(default_dims)
# screen = pygame.display.get_surface()  # ← no crea otra
# dims   = screen.get_size()   
pygame.display.set_caption('Plants vs Zombies')

ADDZOMBIE = pygame.USEREVENT + 2
pygame.time.set_timer(ADDZOMBIE, choice([3000, 4000, 5000]))
database = DB.Zombie_types

ADDNUT = pygame.USEREVENT + 3
pygame.time.set_timer(ADDNUT, choice([5000, 6000, 7000]))


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
                    is_flag = False #! Arreglo del zombie con bandera
                    
            random_z = choices(list(database.keys()), weights=[k['probability'] for k in database.values()])[0]
            its_time_for_zombies = ZB.Zombies(database[random_z], random_z)
            zombies.add(its_time_for_zombies)
    
        elif event.type == ADDNUT:
            for nut in nuts:
                if not nut.rect.collidepoint(list(belt)[0].rect.midright):
                    nut.item_in_belt()
            
    
    
    # SE ACTUALIZAN LOS OBJETOS
    # Dibujar grilla 10x6 dinámica
    GL.update_grid(10, 6, screen)
    # Actualizamos la posicion de los guisantes
    GL.update_peas(peas_group, screen)
    # Actualizamos acciones de las plantas
    GL.update_plants(nuts, zombies, peas_group, soles_group, screen)
    # Actualizamos acciones de los zombies
    GL.udpate_zombies(zombies, nuts, peas_group, screen)
    
    frames.tick(60)
    pygame.display.update()

pygame.quit() 
