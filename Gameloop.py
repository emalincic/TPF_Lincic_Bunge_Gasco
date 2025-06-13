import pygame
import Plants as PL

# ACCION DE LA PLANTA
def shovel_action(plants, pos):
    for plant in plants:
        if plant.rect.collidepoint(pos):
            return plant.remove()


# QUE PLANTA FUE SELECCIONADA
def plant_placement(selected_object, sun_counter, placement, pea_shooters_group, sunflowers, nuts_group):
    if selected_object == 'peashooter_icon' and sun_counter >= 100:
        plant_placed = PL.PeaShotter('Images/Peashooter.png', placement, 'Images/Pea.png')
        pea_shooters_group.add(plant_placed)
        cost = 100
    elif selected_object == 'sunflower_icon' and sun_counter >= 50:
        plant_placed = PL.Sunflower('Images/Sunflower.png', placement)
        sunflowers.add(plant_placed)
        cost = 50
    elif selected_object == 'nut_icon' and sun_counter >= 50:
        plant_placed = PL.Nut('Images/Nut.png', placement)
        nuts_group.add(plant_placed)
        cost = 50 
    return cost



# ACCIONES DE LAS ENTIDADES
def update_peas(peas_group, screen):
    for pea in peas_group:
        pea.shoot()
        screen.blit(pea.image, pea.rect)

def update_plants(plants, zombies, peas_group, soles_group, screen):
    for plant in plants:
        action = plant.ability(zombies)
        if action[1] == 'peashotter':
            peas_group.add(action[0])
        elif action[1] == 'sunflower':
            soles_group.add(action[0])
        screen.blit(plant.image, plant.rect)

def udpate_zombies(zombies, plants, peas_group, screen):
    for zombie in zombies:
        if zombie.type == 'balloon':
            zombie.balloon_ability()
        zombie_center = zombie.rect.center
        collided_plants = [plant for plant in plants if plant.rect.collidepoint(zombie_center)]
        if collided_plants and zombie.type != 'balloon':
            for plant in collided_plants:
                if zombie.ready_to_hit():
                    plant.take_damage(100)
                    zombie.ready_to_hit()
        else:
            zombie.movement()  
        screen.blit(zombie.surf, zombie.rect)
        if pygame.sprite.spritecollide(zombie, peas_group, True):
            zombie.selfdamage()   

def update_suns(soles_group, screen):
    for sol in soles_group:
        sol.action()
        screen.blit(sol.image, sol.rect)

def update_lawnmowers(lawnmowers, zombies, screen):
    for mower in lawnmowers:
        mower.movement(zombies)
        screen.blit(mower.image, mower.rect)

def update_grid(cols, rows, screen):
    screen.fill((50, 120, 50))  # Fondo verde (opcional)
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
    