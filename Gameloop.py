import pygame
import Plants as PL

# ACCION DE LA PLANTA
def shovel_action(plants, pos):
    for plant in plants:
        if plant.rect.collidepoint(pos):
            return plant.remove()


# QUE PLANTA FUE SELECCIONADA
def plant_placement(selected_object, sun_counter, placement, pea_shooters_group, sunflowers, nuts_group, cherry_group, papapum_group, boomerangs_group):
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
    elif selected_object == 'cherry_icon' and sun_counter >= 200:
        plant_placed = PL.cherry('Images/Cherry.png', placement)
        cherry_group.add(plant_placed)
        cost = 200
    elif selected_object == 'papapum_icon' and sun_counter >= 25:
        plant_placed = PL.Papapum('Images/papapum_unload.png', 'Images/papapum_load.png', placement)
        papapum_group.add(plant_placed)
        cost = 25
    elif selected_object == 'boomerang_icon' and sun_counter >= 175:
        plant_placed = PL.Boomerang('Images/boomerang_plant.png', placement, 'Images/boomerang.png')
        boomerangs_group.add(plant_placed)
        cost = 175
    return cost



# ACCIONES DE LAS ENTIDADES
def update_peas(peas_group, boomerangs_bullet_group, screen):
    for pea in peas_group:
        pea.shoot()
        screen.blit(pea.image, pea.rect)
    for boomerang in boomerangs_bullet_group:
        boomerang.shoot()
        screen.blit(boomerang.image, boomerang.rect)

def update_plants(plants, zombies, peas_group, soles_group, boomerangs_bullet_group, screen):
    for plant in plants:
        action = plant.ability(zombies)
        if action[1] == 'peashotter':
            peas_group.add(action[0])
        elif action[1] == 'sunflower':
            soles_group.add(action[0])
        elif action[1]  == 'boomerang':
            boomerangs_bullet_group.add(action[0])
        screen.blit(plant.image, plant.rect)

def udpate_zombies(zombies, plants, peas_group, boomerangs_bullet_group, screen):
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
        for boomerang in boomerangs_bullet_group:
            if zombie.id not in boomerang.already_hit_zombies and boomerang.rect.colliderect(zombie.rect):
                zombie.selfdamage()
                boomerang.already_hit_zombies.append(zombie.id)
  

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

# ============================
# UPDATES FOR PAPAPAPAPUM MODE
# ============================
def update_nuts(nuts_toolbar_group,belt_group,nuts_group_ghost,nuts_group, screen, dragging):
    sorted_nuts = sorted(nuts_toolbar_group, key=lambda nut: nut.rect.x) 
    sorted_nuts_ghost = sorted(nuts_group_ghost, key=lambda nut: nut.rect.x)

    for i, (nut, nut_ghost) in enumerate(zip(sorted_nuts, sorted_nuts_ghost)):
        if nut_ghost != dragging:
            nut_ghost.rect.center = nut.rect.center
        
        can_move = True
        
        if nut.rect.collidepoint(list(belt_group)[0].rect.midright):
            can_move = False
            
        if i + 1 < len(sorted_nuts):
            next_nut = sorted_nuts[i + 1]
            if nut.rect.right >= next_nut.rect.left:
                can_move = False
                

        if can_move:
            nut.item_in_belt()
        
        screen.blit(nut_ghost.image, nut_ghost.rect)
        screen.blit(nut.image, nut.rect)
        
    for nut_placed in nuts_group:
        screen.blit(nut_placed.image, nut_placed.rect)

def update_zombies_papum(nuts_group, zombies, screen):
    for zombie in zombies:
        zombie.movement()  
        screen.blit(zombie.surf, zombie.rect)
        zombie_center = zombie.rect.center
        for nut in nuts_group:
            nut.ability()
            if nut.rect.collidepoint(zombie_center) and not nut.already_hit:
                zombie.selfdamage(500) 
                nut.already_hit = True
            nut.already_hit = False

def nut_placement(placement, nuts_group, nuts_toolbar_group):
    if placement:
        nut_placed = PL.Spinning_Nut('Images/Nut.png', placement)
        nuts_group.add(nut_placed)
    for nuts in nuts_toolbar_group:
        if placement:
            nuts.kill()
            break
    