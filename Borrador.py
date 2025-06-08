import pygame
from random import choice,choices
import BC
import SUNS
from zombies import Zombies
from lawnmower import add_lawnmowers
from main_menu import main_menu
from DataBase import Zombie_types
from Selectables import toolbar, DraggingGhost

# Clase Plantas
class Plants(pygame.sprite.Sprite):
    def __init__(self, image_file, pos, dims = (800, 600), cost = 50, life = 300):
        super(Plants, self).__init__()
        non_dimmed = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(non_dimmed, (100, 90))
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)
        self.cost = cost
        self.state = pygame.time.get_ticks()
        self.ready = None
        self.life = life
    def take_damage(self, damage = 0):
        if self.life <= 0: self.kill()
        else: self.life -= damage
    def remove(self): 
        self.kill()
        return int(self.cost/2)

class Sunflower(Plants):
    def __init__(self, image_file, pos, dims=(800, 600), cost=50, life = 300):
        super().__init__(image_file, pos, dims, cost, life)
    def ability(self):
        if self.ready == None:
            self.ready = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.ready >= 10000:
            fpy = self.rect.centery
            sun = SUNS.SF_sun('Images/sol.png', self.rect.center, fpy)
            soles.add(sun)
            self.ready = None

class Nut(Plants):
    def __init__(self, image_file, pos, dims=(800, 600), cost=50, life=4000):
        super().__init__(image_file, pos, dims, cost, life)
    def ability(self): return None

class PeaShotter(Plants):
    def __init__(self, image_file, pos, pea_file, dims=(800, 600), cost=50, life=300):
        super().__init__(image_file, pos, dims, cost, life)
        self.pea_file = pea_file
    def ability(self):
        if not any(z.cy == self.pos[1] for z in get_zombies()):
            return None
        if self.ready == None:
            self.ready = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.ready >= 1400:
            new_pea = Pea(self.pea_file, (self.pos))
            peas.add(new_pea)
            self.ready = None

class Pea(pygame.sprite.Sprite):
    def __init__(self, image_file, pos, dims=(800, 600)):
        super(Pea, self).__init__()
        non_dimmed = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(non_dimmed, (35, 35))
        self.x, self.y = pos
        self.rect = self.image.get_rect(center=(self.x, self.y-20))
    def shoot(self):
        self.rect.move_ip(2, 0)

# Intizialize pygame
pygame.init()
soles = pygame.sprite.Group()
girasoles = pygame.sprite.Group()
pea_shooters = pygame.sprite.Group()
nuts = pygame.sprite.Group()
peas = pygame.sprite.Group()

def get_all_palnts():
    return girasoles.sprites() + pea_shooters.sprites() + nuts.sprites()
def get_zombies():
    return zombies.sprites()



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
pygame.time.set_timer(ADDZOMBIE, choice([3000, 5000, 6000])) # Milisegundos de aparición
zombies = pygame.sprite.Group()
lawnmowers = add_lawnmowers(10, 6)

# Grupo de soles
soles = pygame.sprite.Group()

zombie_damage = 1500
last_zombie_damage = -zombie_damage

# Clase boton del sol
class Sun_Counter(pygame.sprite.Sprite):
        def __init__(self, image_file, dims):
            super(Sun_Counter, self).__init__()
            



# Ejecutamos menú principal antes del juego
main_menu()

# ========================
# LOOP PRINCIPAL DEL JUEGO
# ========================


run = True
sun_counter = 0
frames = pygame.time.Clock()
    
pygame.mixer.music.load('Audio\The Zombies Are coming Sound Effect.mp3')
pygame.mixer.music.set_volume(1.0) 
pygame.mixer.music.play(0)

toolbar_group, toolbar_group_ghost = toolbar()

selected_object = None
dragging = None
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == SUN_EVENT:
            new_sun = SUNS.Suns('Images/sol.png')
            soles.add(new_sun)
        elif event.type == ADDZOMBIE:
            random_z = choices(list(Zombie_types.keys()), weights=[k['probability'] for k in Zombie_types.values()])[0]
            zombie = Zombies(Zombie_types[random_z], random_z)
            zombies.add(zombie)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for item in toolbar_group_ghost:
                if item.rect.collidepoint(event.pos):
                    selected_object = item.key
                    # dragging = DraggingGhost(item.image)
                    dragging = item
                    original_pos = dragging.rect.center
            # for selectable in selectables:
            #     if selectable.rect.collidepoint(event.pos):
            #         dragging = True
            #         selected_object = selectable
                    
            for sol in soles:
                if sol.rect.collidepoint(event.pos):
                    sun_counter += sol.grab()

            for zombie in zombies:
                if zombie.rect.collidepoint(event.pos):
                    zombie.selfdamage()
        elif event.type == pygame.MOUSEBUTTONUP and dragging:
            pos = pygame.mouse.get_pos()
            placement = SUNS.cell_center(10, 6, 'plant', pos)
            if selected_object == 'shovel_icon': 
                for plant in plants:
                    if plant.rect.collidepoint(pos):
                        plant.remove() 
                        break

            elif placement != None and not any(p.rect.center == placement for p in get_all_palnts()):
                if selected_object == 'peashooter_icon':
                    new_peashooter = PeaShotter('Images/Peashooter.png', placement, 'Images/Pea.png')
                    pea_shooters.add(new_peashooter)
                elif selected_object == 'sunflower_icon':
                    new_sunflower = Sunflower('Images/Sunflower.png', placement)
                    girasoles.add(new_sunflower)
                elif selected_object == 'nut_icon':
                    new_nut = Nut('Images/Nut.png', placement)
                    nuts.add(new_nut)
            # elif any(p.rect.center == placement for p in get_all_palnts()):
            #     for 
            
            dragging.rect.center = original_pos

            dragging = None
            selected_object = None
                # else:
                #     if item.key == 'shovel_icon':
                #         for plant in plants:
                #             plant.remove()

        elif event.type == pygame.MOUSEMOTION and dragging:
            dragging.rect.center = (event.pos)
            
            # dragging.update(event.pos)

        # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
        #     if time - last_sunflower_placed >= sunflower_cooldown:
        #         new_sunflower = PeaShotter('Images/Peashooter.png', pygame.mouse.get_pos(), 'Images/Pea.png')
        #         pea_shooters.add(new_sunflower)
        #         last_sunflower_placed = time
        #     else: print("Not ready") # ACA HABRIA QUE IMPLEMENTAR LO QUE PASA EN EL COOLDOWN DE LAS PLANTAS
        # elif event.type == pygame.KEYDOWN:
        #     pos = pygame.mouse.get_pos()
        #     placement = SUNS.cell_center(10, 6, 'plant', pos)
        #     if placement != None and not any(p.rect.center == placement for p in get_all_palnts()):    
        #         if event.key == pygame.K_p:
        #                 new_peashooter = PeaShotter('Images/Peashooter.png', placement, 'Images/Pea.png')
        #                 pea_shooters.add(new_peashooter)
        #         elif event.key == pygame.K_g:
        #                 new_sunflower = Sunflower('Images/Sunflower.png', placement)
        #                 girasoles.add(new_sunflower)
        #         elif event.key == pygame.K_n:
        #             new_nut = Nut('Images/Nut.png', placement)
        #             nuts.add(new_nut)
    
    soles.update()
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
    plants = get_all_palnts()

    for pea in peas:
        pea.shoot()
        screen.blit(pea.image, pea.rect)
    for plant in plants:
        plant.ability()
        screen.blit(plant.image, plant.rect)
    for zombie in zombies:
        collided_plants = pygame.sprite.spritecollide(zombie, plants, False)
        if collided_plants:# and zombie.balloon_ability(): ### ARREGLAR ZOMBIE GLOBO
            for plant in collided_plants:
                if zombie.ready_to_hit():
                    plant.take_damage(100)
                    zombie.ready_to_hit()
        else:
            zombie.movement()
        screen.blit(zombie.surf, zombie.rect)
        if pygame.sprite.spritecollide(zombie, peas, True):
            zombie.selfdamage()

    for sol in soles:
        sol.action()
        screen.blit(sol.image, sol.rect)
    for mower in lawnmowers:
        mower.movement(zombies)
        screen.blit(mower.image, mower.rect)
        
    toolbar_group_ghost.draw(screen)
    toolbar_group.draw(screen)
    
    pygame.display.update()
    frames.tick(60)

    #print(sun_counter)
    pygame.display.update()

pygame.quit() 