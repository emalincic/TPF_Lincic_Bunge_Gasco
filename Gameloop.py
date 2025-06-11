import pygame

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
    