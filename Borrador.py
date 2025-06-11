import pygame
from random import choice,choices
import BC
import SUNS as SN
import Plants as PL
from zombies import Zombies
import zombies as ZB
import lawnmower as LM
from main_menu import main_menu
import DataBase as DB
import Toolbar as TL
import Gameloop as GL

# Ejecutamos menú principal antes del juego
start_time = main_menu()


# Intizialize pygame
pygame.init()
# Grupos de las Plantas
sunflowers = pygame.sprite.Group()
pea_shooters_group = pygame.sprite.Group()
nuts_group = pygame.sprite.Group()
peas_group = pygame.sprite.Group()
# Grupo de los soles
soles_group = pygame.sprite.Group()

def get_all_plants():
    return sunflowers, pea_shooters_group, nuts_group, peas_group

def get_all_plants():
    return sunflowers.sprites() + pea_shooters_group.sprites() + nuts_group.sprites()

# Grupo de los zombies
zombies = pygame.sprite.Group()

sunflower_cooldown = 10000
last_sunflower_placed = -sunflower_cooldown # Tratar de incorporar cooldowns en las clases??

# Creamos ventana
dims = (1200, 600)
screen = pygame.display.set_mode(dims)
pygame.display.set_caption('Plants vs Zombies')

# Creamos el mapa según la imagen
mapa = BC.Background('Images/mapa.jpg', [0, 0], dims)

# Evento personalizado para los soles
SUN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SUN_EVENT, 10000)

ADDZOMBIE = pygame.USEREVENT + 2
pygame.time.set_timer(ADDZOMBIE, choice([5000, 7000, 9000]))
database = DB.Zombie_types
is_flag = True
lawnmowers = LM.add_lawnmowers(10, 6)

zombie_damage = 1500
last_zombie_damage = -zombie_damage

cursor_opended = pygame.image.load('Images/Mouse.png').convert_alpha()
cursor_opended = pygame.transform.scale(cursor_opended, (40, 40))

cursor_pressed = pygame.image.load('Images/Mouse_click.png').convert_alpha()
cursor_pressed = pygame.transform.scale(cursor_pressed, (40, 40))

mouse_opened = pygame.cursors.Cursor((0, 0), cursor_opended)
mouse_pressed = pygame.cursors.Cursor((0, 0), cursor_pressed)

pygame.mouse.set_cursor(mouse_opened)

run = True
sun_counter = 50
font = pygame.font.Font("04B_03__.TTF", 50) 

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
            
        elif event.type == SUN_EVENT:
            new_sun = SN.Suns('Images/sol.png')
            soles_group.add(new_sun)
            
        elif event.type == ADDZOMBIE:
            if (current_time - start_time) // 1000 >= 100 and is_flag:
                    flag = ZB.Zombies(DB.Zombie_types['flag'], 'flag')
                    zombies.add(flag)
                    
                    pygame.mixer.music.load('Audio\The Zombies Are coming Sound Effect.mp3')
                    pygame.mixer.music.play(0)
                    pygame.time.set_timer(ADDZOMBIE, choice([2500, 3000, 3500]))
                    is_flag = False #! Arreglo del zombie con bandera
                    
            random_z = choices(list(database.keys()), weights=[k['probability'] for k in database.values()])[0]
            its_time_for_zombies = Zombies(database[random_z], random_z)
            zombies.add(its_time_for_zombies)
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for item in toolbar_group_ghost:
                if item.rect.collidepoint(event.pos):
                    selected_object = item.key
                    dragging = item
                    original_pos = dragging.rect.center
                    
            for sol in soles_group:
                if sol.rect.collidepoint(event.pos):
                    sun_counter += sol.grab()

        elif event.type == pygame.MOUSEBUTTONUP and dragging:
            pos = pygame.mouse.get_pos()
            placement = SN.cell_center(10, 6, 'plant', pos)
            if selected_object == 'shovel_icon': 
                for plant in get_all_plants():
                    if plant.rect.collidepoint(pos):
                        sun_counter += plant.remove() 
                        break

            elif placement != None and not any(p.rect.center == placement for p in get_all_plants()):
                if selected_object == 'peashooter_icon' and sun_counter >= 100:
                    new_peashooter = PL.PeaShotter('Images/Peashooter.png', placement, 'Images/Pea.png')
                    pea_shooters_group.add(new_peashooter)
                    sun_counter -= 100
                elif selected_object == 'sunflower_icon' and sun_counter >= 50:
                    new_sunflower = PL.Sunflower('Images/Sunflower.png', placement)
                    sunflowers.add(new_sunflower)
                    sun_counter -= 50
                elif selected_object == 'nut_icon' and sun_counter >= 50:
                    new_nut = PL.Nut('Images/Nut.png', placement)
                    nuts_group.add(new_nut)
                    sun_counter -= 50 
            dragging.rect.center = original_pos
            dragging = None
            selected_object = None
        elif event.type == pygame.MOUSEMOTION and dragging:
            dragging.rect.center = (event.pos)

        # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
        #     if time - last_sunflower_placed >= sunflower_cooldown:
        #         new_sunflower = PeaShotter('Images/Peashooter.png', pygame.mouse.get_pos(), 'Images/Pea.png')
        #         pea_shooters.add(new_sunflower)
        #         last_sunflower_placed = time
        #     else: print("Not ready") # ACA HABRIA QUE IMPLEMENTAR LO QUE PASA EN EL COOLDOWN DE LAS PLANTAS

    
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
    
        
    toolbar_group_ghost.draw(screen)
    toolbar_group.draw(screen)
    print(sun_counter)
    # Convertir el contador a imagen de texto
    counter = font.render(str(sun_counter), True, (255, 255, 255))  # Blanco
    # Mostrarlo en pantalla, por ejemplo en la esquina superior izquierda
    counter_sprite = list(toolbar_group)[-1]
    counter_center = counter.get_rect(center=counter_sprite.rect.center)
    screen.blit(counter, (counter_center[0]+20, counter_center[1]))
    frames.tick(60)
    pygame.display.update()

pygame.quit() 


