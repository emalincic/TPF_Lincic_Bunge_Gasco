import pygame
from random import choice,choices
import BC
import SUNS as SN
import Plants as PL
from zombies import Zombies, balloon
import zombies as ZB
import lawnmower as LM
from main_menu import main_menu
import DataBase as DB
import Toolbar as TL
import Gameloop as GL
from utils import GAME_OVER
from game_over_menu import show_game_over

# Ejecutamos menú principal antes del juego
start_time, fullscreen = main_menu()  


# TODO Intizialize pygame
pygame.init()
#* Grupos de las Plantas
sunflowers = pygame.sprite.Group()
pea_shooters_group = pygame.sprite.Group()
nuts_group = pygame.sprite.Group()
peas_group = pygame.sprite.Group()
#* Grupo de los soles
soles_group = pygame.sprite.Group()
#* Grupon de los Zombies
zombies = pygame.sprite.Group()

def get_all_plants():
    return sunflowers, pea_shooters_group, nuts_group, peas_group

def get_all_plants():
    return sunflowers.sprites() + pea_shooters_group.sprites() + nuts_group.sprites()

# Creamos ventana
screen = pygame.display.get_surface()  # ← no crea otra
dims   = screen.get_size()             # (ancho, alto) actuales
pygame.display.set_caption('Plants vs Zombies')

# Creamos el mapa según la imagen
mapa = BC.Background('Images/mapa.jpg', [0, 0], screen)

# Evento personalizado para los soles
SUN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SUN_EVENT, 10000)

# Evento de los zombies
ADDZOMBIE = pygame.USEREVENT + 2
pygame.time.set_timer(ADDZOMBIE, choice([5000, 7000, 9000]))
database = DB.Zombie_types
is_flag = True
#Evento de Game Over

# Obtenemos las lawnmowers
lawnmowers = LM.add_lawnmowers(10, 6)

# Obtenemos los estilos del mouse
mouse_opened, mouse_pressed = BC.mouses('Images/Mouse.png', 'Images/Mouse_click.png')
pygame.mouse.set_cursor(mouse_opened)



run = True
sun_counter = 5000
font = pygame.font.Font("04B_03__.TTF", 35) 

frames = pygame.time.Clock()
    
pygame.mixer.music.load('Audio\The Zombies Are coming Sound Effect.mp3') 
pygame.mixer.music.play(0)

toolbar_group, toolbar_group_ghost = TL.toolbar()

selected_object = None
dragging = None
while run:
    current_time = pygame.time.get_ticks()
    events = pygame.event.get()
    
    for event in events:
        if pygame.mouse.get_pressed()[0]:
            pygame.mouse.set_cursor(mouse_pressed)
        else:
            pygame.mouse.set_cursor(mouse_opened)
            
        if event.type == pygame.QUIT:
            run = False
        elif event.type == GAME_OVER:
            
            show_game_over(screen)   
            run = False 
            break
        elif event.type == SUN_EVENT:
            new_sun = SN.Suns('Images/sol.png')
            soles_group.add(new_sun)
        elif event.type == ADDZOMBIE:
          #  def spawn_zombie
            if (current_time - start_time) // 1000 >= 100 and is_flag:
                    flag = ZB.Zombies(DB.Zombie_types['flag'], 'flag')
                    zombies.add(flag)
                    
                    pygame.mixer.music.load('Audio\The Zombies Are coming Sound Effect.mp3')
                    pygame.mixer.music.play(0)
                    pygame.time.set_timer(ADDZOMBIE, choice([2500, 3000, 3500]))
                    is_flag = False #! Arreglo del zombie con bandera
    
            random_z = choices(list(database.keys()), weights=[k['probability'] for k in database.values()])[0]
            if random_z == 'balloon':
                its_time_for_zombies = balloon(database[random_z], random_z)
            else:
                its_time_for_zombies = Zombies(database[random_z], random_z)
            zombies.add(its_time_for_zombies)
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for item in toolbar_group_ghost:
                if item.rect.collidepoint(event.pos):
                    real_card = next(card for card in toolbar_group if card.key == item.key)

                    if real_card.ready():           
                        selected_object = item.key
                        dragging = item
                        original_pos = dragging.rect.center
                    else:
               
                        pass
                    
            for sol in soles_group:
                if sol.rect.collidepoint(event.pos):
                    sun_counter += sol.grab()

        elif event.type == pygame.MOUSEBUTTONUP and dragging:
            pos = pygame.mouse.get_pos()
            placement = SN.cell_center(10, 6, 'plant', pos)

            if selected_object == 'shovel_icon':
                sun_counter += GL.shovel_action(get_all_plants(), pos)

            elif placement is not None and not any(
                    p.rect.center == placement for p in get_all_plants()):
                
                cost = GL.plant_placement(
                    selected_object, sun_counter, placement,
                    pea_shooters_group, sunflowers, nuts_group
                )                                       
                if cost:                                
                    sun_counter -= cost                
                    for card in toolbar_group:          
                        if card.key == selected_object: 
                            card.start_cooldown()       
                            break                       

            dragging.rect.center = original_pos
            dragging = None            
            selected_object = None
        elif event.type == pygame.MOUSEMOTION and dragging:
            dragging.rect.center = (event.pos)

    
    # SE ACTUALIZAN LOS OBJETOS
    # Dibujar grilla 10x6 dinámica
    GL.update_grid(10, 6, screen)
    # Actualizamos la posicion de los guisantes
    GL.update_peas(peas_group, screen)
    # Actualizamos acciones de las plantas
    GL.update_plants(get_all_plants(), zombies, peas_group, soles_group, screen)
    # Actualizamos acciones de los zombies
    GL.udpate_zombies(zombies, get_all_plants(), peas_group, screen)
    # Actualizamos los soles
    GL.update_suns(soles_group, screen)
    # Actaulizamos las cosechadoras
    GL.update_lawnmowers(lawnmowers, zombies, screen)
    
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


