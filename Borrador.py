import pygame
from random import choice,choices
import BC
import SUNS
import Plants as PL
from zombies import Zombies, get_zombies
from lawnmower import add_lawnmowers
from main_menu import main_menu
from DataBase import Zombie_types
from Selectables import toolbar
# Ejecutamos menú principal antes del juego
start_time = main_menu()
# Intizialize pygame
pygame.init()
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
pygame.time.set_timer(SUN_EVENT, 5000)

ADDZOMBIE = pygame.USEREVENT + 2
pygame.time.set_timer(ADDZOMBIE, choice([5000, 7000, 9000]))
is_flag = True
lawnmowers = add_lawnmowers(10, 6)

zombie_damage = 1500
last_zombie_damage = -zombie_damage

# Clase boton del sol
class Sun_Counter(pygame.sprite.Sprite):
        def __init__(self, image_file, pos):
            super(Sun_Counter, self).__init__()
            non_dimmed = pygame.image.load(image_file).convert_alpha()
            self.image = pygame.transform.scale(non_dimmed, (110, 110))
            self.pos = pos
            self.rect = self.image.get_rect(center=pos)

sun_amount = Sun_Counter('Images/Sun_Counter.png', SUNS.cell_center(10, 6, 'sun_counter'))

font = pygame.font.Font("04B_03__.TTF", 35)


#screen.blit(sun_amount.image, sun_amount.rect)
#suns_text = font.render(str(sun_counter), True, (0, 0, 0))
#screen.blit(suns_text, (sun_amount.rect.centerx - 35, sun_amount.rect.centery + 10))     


run = True
sun_counter = 1000
frames = pygame.time.Clock()
    
pygame.mixer.music.load('Audio\The Zombies Are coming Sound Effect.mp3') 
pygame.mixer.music.play(0)

toolbar_group, toolbar_group_ghost = toolbar()

selected_object = None
dragging = None
while run:
    current_time = pygame.time.get_ticks()
    events = pygame.event.get()
    
    for event in events:
        if event.type == pygame.QUIT:
            run = False
            
        elif event.type == SUN_EVENT:
            new_sun = SUNS.Suns('Images/sol.png')
            soles_group.add(new_sun)
            
        elif event.type == ADDZOMBIE:
            if (current_time - start_time) // 1000 >= 100 and is_flag:
                    flag = Zombies(Zombie_types['flag'], 'flag')
                    zombies.add(flag)
                    
                    pygame.mixer.music.load('Audio\The Zombies Are coming Sound Effect.mp3')
                    pygame.mixer.music.play(0)
                    pygame.time.set_timer(ADDZOMBIE, choice([1000, 2000, 3000]))
                    is_flag = False #! Arreglo del zombie con bandera
                    
            random_z = choices(list(Zombie_types.keys()), weights=[k['probability'] for k in Zombie_types.values()])[0]
            its_time_for_zombies = Zombies(Zombie_types[random_z], random_z)
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
            placement = SUNS.cell_center(10, 6, 'plant', pos)
            if selected_object == 'shovel_icon': 
                for plant in plants:
                    if plant.rect.collidepoint(pos):
                        plant.remove() 
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

    
    soles_group.update()
    screen.fill((50, 120, 50))  # Fondo verde (opcional)

    # Dibujar grilla 10x6 dinámica
    cols = 10
    rows = 6
    width, height = screen.get_size()    # ancho y alto actuales
    cell_width  = width  // cols
    cell_height = height // rows

    for i in range(cols):
        for j in range(rows):
            rect = pygame.Rect(i * cell_width,
                            j * cell_height,
                            cell_width,
                            cell_height)
            pygame.draw.rect(screen, (0, 100, 0), rect, 2)

    plants = get_all_plants()

    for pea in peas_group:
        pea.shoot()
        screen.blit(pea.image, pea.rect)
    for plant in plants:
        action = plant.ability(zombies)
        print(action)
        if action[1] == 'peashotter':
            peas_group.add(action[0])
        elif action[1] == 'sunflower':
            soles_group.add(action[0])


        screen.blit(plant.image, plant.rect)
    
    for zombie in zombies:
        if zombie.type == 'balloon' and zombie.balloon_ability():
            zombie.movement()
        else:
            collided_plants = pygame.sprite.spritecollide(zombie, plants, False)
            if collided_plants:# and zombie.balloon_ability(): #! ARREGLAR ZOMBIE GLOBO
                for plant in collided_plants:
                    if zombie.ready_to_hit():
                        plant.take_damage(100)
                        zombie.ready_to_hit()
            else:
                zombie.movement()
            
            screen.blit(zombie.surf, zombie.rect)
            
            if pygame.sprite.spritecollide(zombie, peas_group, True):
                zombie.selfdamage()

    for sol in soles_group:
        sol.action()
        screen.blit(sol.image, sol.rect)
    for mower in lawnmowers:
        mower.movement(zombies)
        screen.blit(mower.image, mower.rect)
        
    toolbar_group_ghost.draw(screen)
    toolbar_group.draw(screen)
    print(sun_counter)
    pygame.display.update()
    frames.tick(60)

    #print(sun_counter)
    pygame.display.update()

pygame.quit() 