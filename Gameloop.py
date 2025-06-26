import os
import pygame
import Plants as PL

#  ───────────────────────── Actiones  ─────────────────────────

# Accion de la pala
def shovel_action(plants: list, pos: tuple) -> int:
    """
    Funcion designada a la accion de la planta. Se recorren todas las plantas activas 
    en el momento en que el usuario recoge la pala. Si la posicion de la planta coincide
    con la de la pala, se elimina la planta.
    Entradas:
        1. plants (list): lista con todos los sprites de las plantas
        2. pos (tuple): posicion del mouse del usuario luego de solar la pala en una posicion
    Returns:
        1. plant.remove() que devuelve el 50% del costo de la planta (metodo de la clase Plants)
    """
    for plant in plants:
        if plant.rect.collidepoint(pos):
            return plant.remove() # Metodo de clase plants
    return 0


# Planta que fue seleccionada
def plant_placement(selected_object: str, sun_counter: int, placement: tuple, pea_shooters_group: pygame.sprite.Group, 
                    sunflowers_group: pygame.sprite.Group, nuts_group: pygame.sprite.Group, 
                    cherry_group: pygame.sprite.Group, papapum_group: pygame.sprite.Group, 
                    boomerangs_group: pygame.sprite.Group) -> int:
    """
    Funcion utilizada para decidir que planta va a ser posicionada. La funcion verifica que planta fue seleccionada,
    si el usuario cuenta con los soles necesarios. Si los tiene se actualiza el pygame Group correspondiente,
    agregando la planta.
    Entradas:
        1. selected_object (str): string que identifica el objeto (planta seleccionada)
        2. sun_counter (int): cantidad de soles con las que cuenta el usuario en el momento de intentar 
        ubicar una planta
        3. placement (tuple): tupla con la posicion donde quiere ser ubicada la planta.
        4. pea_shooters_group (pygame.sprite.Group): grupo de pygame de los Lanzaguisantes.
        5. sunflowers_group (pygame.sprite.Group): grupo de pygame de los Girasoles.
        6. nuts_group (pygame.sprite.Group): grupo de pygame de las Nueces.
        7. cherry_group (pygame.sprite.Group): grupo de pygame de las Cerezas.
        8. papapum_group (pygame.sprite.Group): grupo de pygame de los Papapum.
        9. boomerangs_group (pygame.sprite.Group): grupo de pygame de las plantas Boomerang
    Returns:
        1. cost (int): costo de haber posicionado una planta. Si no se logra posicionar el return es 0
    """
    cost = 0 # Por si no tiene los soles suficientes para comprar la planta

    if selected_object == 'peashooter_icon' and sun_counter >= 100:

        PS_image = os.path.join("Images", "Peashooter.png")
        Pea_image = os.path.join("Images", "Pea.png")

        plant_placed = PL.PeaShotter(PS_image, placement, Pea_image)
        pea_shooters_group.add(plant_placed)
        cost = 100

    elif selected_object == 'sunflower_icon' and sun_counter >= 50:
        
        SF_image = os.path.join("Images", "Sunflower.png")

        plant_placed = PL.Sunflower(SF_image, placement)
        sunflowers_group.add(plant_placed)
        cost = 50

    elif selected_object == 'nut_icon' and sun_counter >= 50: 

        NT_image = os.path.join("Images", "Nut.png")

        plant_placed = PL.Nut(NT_image, placement)
        nuts_group.add(plant_placed)
        cost = 50 

    elif selected_object == 'cherry_icon' and sun_counter >= 150:

        CB_image = os.path.join("Images", "Cherry.png")
        XPL_image = os.path.join("Images", "explosion.png") 

        plant_placed = PL.cherry(CB_image, placement, XPL_image) 
        cherry_group.add(plant_placed)
        cost = 150

    elif selected_object == 'papapum_icon' and sun_counter >= 25:

        PMU_image = os.path.join('Images', 'papapum_unload.png')
        PML_image = os.path.join('Images', 'papapum_load.png')
        XPL_image = os.path.join("Images", "explosion.png")

        plant_placed = PL.Papapum(PMU_image, PML_image, XPL_image, placement)
        papapum_group.add(plant_placed)
        cost = 25

    elif selected_object == 'boomerang_icon' and sun_counter >= 175:

        boomerang_plant_image = os.path.join('Images', 'boomerang_plant.png')
        boomerang_image = os.path.join('Images', 'boomerang.png')

        plant_placed = PL.Boomerang(boomerang_plant_image, placement, boomerang_image)
        boomerangs_group.add(plant_placed)
        cost = 175
    return cost



# ───────────────────────── Actualizaciones para el modo clasico ─────────────────────────
def update_peas(peas_group: pygame.sprite.Group, boomerangs_bullet_group: pygame.sprite.Group, 
                screen: pygame.surface.Surface):
    """
    Funcion destinada a actualizar la posicion de los proyectiles de las plantas, llamando a su metodo shoot()
    y actualizando la pantalla.
    Entradas:
        1. peas_group (pygame.sprite.Group): grupo de pygame de los guisantes
        2. boomerangs_bullet_group (pygame.sprite.Group): grupo de pygame de los boomerangs
        3. screen (pygame.surface.Surface): pantalla del usuario
    """
    for pea in peas_group:
        pea.shoot()
        screen.blit(pea.image, pea.rect)
    for boomerang in boomerangs_bullet_group:
        boomerang.shoot()
        screen.blit(boomerang.image, boomerang.rect)


def update_plants(plants: list, zombies: pygame.sprite.Group, peas_group: pygame.sprite.Group, 
                  suns_group: pygame.sprite.Group, boomerangs_bullet_group: pygame.sprite.Group, 
                  explosions_group: pygame.sprite.Group, screen: pygame.surface.Surface):
    """
    Funcion destinada a realizar las habilidades de las plantas en pantalla llamando a su atributo ability().
    Se identifica el tag de la habilidad (return de ability()) para realizar la accion que corresponde. A su vez,
    se actualiza la pantalla para cada accion de cada planta efectuada.
    Entradas:
        1. plants (list): lista con los sprites de las plantas en pantalla
        2. zombies (pygame.sprite.Group): grupo de pygame de los zombies en pantalla
        3. peas_group (pygame.sprite.Group): grupo de pygame de los guisantes
        4. suns_group (pygame.sprite.Group): grupo de pygame de los soles
        5. boomerangs_bullet_group (pygame.sprite.Group): grupo de pygame de los boomerangs
        6. explosions_group (pygame.sprite.Group): grupo de pygame de las explosiones
        7. screen (pygame.surface.Surface): pantalla del usuario
    """
    for plant in plants:
        action = plant.ability(zombies)
        if action[1] == 'peashotter':
            peas_group.add(action[0])
        elif action[1] == 'sunflower':
            suns_group.add(action[0])
        elif action[1]  == 'boomerang':
            boomerangs_bullet_group.add(action[0])
        elif action[1] == 'cherry' or action[1] == 'papapum':
            explosions_group.add(action[0])
        screen.blit(plant.image, plant.rect)

def update_zombies(zombies: pygame.sprite.Group, plants: list, peas_group: pygame.sprite.Group, 
                   boomerangs_bullet_group: pygame.sprite.Group, screen: pygame.surface.Surface):
    """
    Funcion destinada a las acciones y actualizacion de los zombies en pantalla. Se verifica el tipo 
    de zombi para realizar la acción correspondiente. Se actualiza la pantalla acorde y las plantas 
    en contacto con un zombi listo para golpear pierden vida.
    Entradas:
        1. zombies (pygame.sprite.Group): grupo de pygame de los zombies en pantalla
        2. plants (list): lista con los sprites de las plantas en pantalla
        3. peas_group (pygame.sprite.Group): grupo de pygame de los guisantes
        4. boomerangs_bullet_group (pygame.sprite.Group): grupo de pygame de los boomerangs
        5. screen (pygame.surface.Surface): pantalla del usuario
    """
    for zombie in zombies:
        if zombie.type == 'Balloon':
            zombie.balloon_ability() # Si el zombi es del tipo globo se realiza su accion propia
        zombie_center = zombie.rect.center
        # Se verifica que plantas estan en contacto con los zombis
        collided_plants = [plant for plant in plants if plant.rect.collidepoint(zombie_center)]
        if collided_plants and zombie.type != 'Balloon':
            for plant in collided_plants:
                if zombie.ready_to_hit(): # Se verifica si paso el cooldown del zombi
                    plant.take_damage(100)
                    zombie.ready_to_hit()
        else:
            zombie.eating = False
            zombie.movement()  # Si no tiene planta en frente avanza
        
        screen.blit(zombie.surf, zombie.rect)
        # Recibir golpes (zombis)
        if pygame.sprite.spritecollide(zombie, peas_group, True): # True elimina el guisante en contacto
            zombie.selfdamage()
        for boomerang in boomerangs_bullet_group:
            # Se verifica que el zombi no haya sido golpeado en el recorrido del boomerang y que este en contacto
            if zombie.id not in boomerang.already_hit_zombies and boomerang.rect.colliderect(zombie.rect):
                zombie.selfdamage()
                # Si es golpeado se agrega a los zombis ya golpeados del boomerang
                boomerang.already_hit_zombies.append(zombie.id)
  

def update_suns(suns_group: pygame.sprite.Group, screen: pygame.surface.Surface):
    """
    Funcion destinada a actualizar la posicion de los soles en pantalla.
    Entradas:
        1. suns_group (pygame.srpite.Group): grupo de pygame de los soles
        2. screen (pygame.surface.Surface): pantalla del usuario
    """
    for sol in suns_group:
        sol.action()
        screen.blit(sol.image, sol.rect)

def update_lawnmowers(lawnmowers: pygame.sprite.Group, zombies: pygame.sprite.Group, screen: pygame.surface.Surface):
    """
    Funcion destinada a actualizar el estado y posicion de las podadoras en pantalla.
    Entradas:
        1. lawnmowers (pygame.sprite.Group): grupo de pygame de las podadoras en pantalla
        2. zombies (pygame.sprite.Group): groupo de pygame de los zombies en pantalla
        3. screen (pygame.surface.Surface): pantalla del usuario
    """
    for mower in lawnmowers:
        mower.movement(zombies) # Atributo de la clase Lawnmower
        screen.blit(mower.image, mower.rect)

def update_grid(cols: int, rows: int, screen: pygame.surface.Surface, 
                frame: pygame.surface.Surface, dark_square: pygame.surface.Surface, 
                light_square: pygame.surface.Surface, start_row: int = 0) -> None:
    """
    Funcion destinada a actualizar la grilla subyacente al juego. Se toman como entrada la cantidad de columnas
    y filas para poder dividir la pantalla proporcionalmente. Ademas, se actualiza las imagenes de cada celda
    para dar el diseño al fondo.
    Entradas:
        1. cols (int): cantidad de columnas
        2. rows (int): cantidad de filas
        3. screen (pygame.surface.Surface): pantalla del usuario
        4. frame (pygame.surface.Surface): superficie del marco
        5. dark_square (pygame.surface.Surface): superficie de las celdas oscuras
        6. light_square (pygame.surface.Surface): superficie de las celdas claras
        7. start_row (int): fila por la que se quiere empezar a actualizar
    """
    width, height = screen.get_size()    # ancho y alto actuales
    cell_width  = width  // cols
    cell_height = height // rows

    for i in range(cols):
        for j in range(start_row, rows):
            if j == 0: # diseño del marco
                screen.blit(frame, (i*cell_width, j*cell_height))
            elif (i + j) % 2 == 0: # si la celda es par se pinta de claro
                screen.blit(light_square, (i*cell_width, j*cell_height))
            else:
                screen.blit(dark_square, (i*cell_width, j*cell_height))


# ───────────────────────── Actualizaciones del modo papapaum   ─────────────────────────

def update_nuts(nuts_toolbar_group: pygame.sprite.Group, belt_group: pygame.sprite.Group, nuts_group_ghost: pygame.sprite.Group, 
                nuts_group: pygame.sprite.Group, screen: pygame.display, dragging: pygame.sprite.Sprite):
    """
    Función donde se actualizan los seed packets de las nueces y sus 'fantasmas' en la cinta.
    Se ordenan dependiendo la distancia con el extremo derecho de la cinta, donde frenaran si no hay otro paquete por delante.

    Entradas:
        nuts_toolbar_group (pygame.sprite.Group): Grupo de los paquetes de las nueces.
        belt_group (pygame.sprite.Group): Grupo de la cinta transportadora.
        nuts_group_ghost (pygame.sprite.Group): Grupo de las nueces 'fantasma'.
        nuts_group (pygame.sprite.Group): Grupo de las nueces colocadas en el área jugable.
        screen (pygame.display): Display.
        dragging (pygame.sprite.Sprite): Nuez que acompaña al mouse.
    """    
    sorted_nuts = sorted(nuts_toolbar_group, key=lambda nut: nut.rect.x) 
    sorted_nuts_ghost = sorted(nuts_group_ghost, key=lambda nut: nut.rect.x)

    for id, (nut, nut_ghost) in enumerate(zip(sorted_nuts, sorted_nuts_ghost)):
        if nut_ghost != dragging:
            nut_ghost.rect.center = nut.rect.center
        
        can_move = True
        
        if nut.rect.collidepoint(list(belt_group)[0].rect.midright):
            can_move = False
            
        if id + 1 < len(sorted_nuts):
            next_nut = sorted_nuts[id + 1]
            if nut.rect.right >= next_nut.rect.left:
                can_move = False
                
        if can_move:
            nut.item_in_belt()
        
        screen.blit(nut_ghost.image, nut_ghost.rect)
        screen.blit(nut.image, nut.rect)
        
    for nut_placed in nuts_group:
        nut_placed.ability()
        screen.blit(nut_placed.image, nut_placed.rect)

def update_zombies_papum(nuts_group: pygame.sprite.Group, zombies_group: pygame.sprite.Group, screen: pygame.display):
    """
    Función que actualiza el movimiento de los zombies, realiza la acción de reducirle quitarle vida al zombie 
    cuando la nuez lo golpea una única vez.

    Entradas:
        1. nuts_group (pygame.sprite.Group): grupo de pygame de las Nueces giratorias
        2. zombies_group (pygame.sprite.Group): grupo de pygame de los zombies en pantalla
        3. screen (pygame.display): pantalla del usuario
    """   

    for zombie in zombies_group:
        zombie.movement()  
        screen.blit(zombie.surf, zombie.rect)
        zombie_center = zombie.rect.center

        for nut in nuts_group:
            if nut.rect.collidepoint(zombie_center) and zombie.id not in nut.already_hit_zombies:
                nut.already_hit_zombies.append(zombie.id)  
                zombie.selfdamage(500)

def nut_placement(placement: tuple, nuts_group: pygame.sprite.Group, nuts_toolbar_group: pygame.sprite.Group):
    """
    Funcion designada a ubicar las Nueces del modo papapapum. Si placement es None (Nuez ubicada en lugar no permitido),
    no se logra posicionar. En caso de ser una tupla con coordenads se agrega al pygame group de las Nueces una nueva
    y se elimina de la cinta.
    """
    if placement:
        nut_placed = PL.Spinning_Nut(os.path.join('Images', 'Nut.png'), placement)
        nuts_group.add(nut_placed)

    # Se eliminan Nueces puestas
    for nuts in nuts_toolbar_group:
        if placement:
            nuts.kill()
            break
