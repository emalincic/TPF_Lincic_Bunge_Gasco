import pygame
# Grupos de las plantas
sunflowers = pygame.sprite.Group()
pea_shooters_group = pygame.sprite.Group()
nuts_group = pygame.sprite.Group()
peas_group = pygame.sprite.Group()

def get_all_plants():
    return sunflowers, pea_shooters_group, nuts_group, peas_group

def get_all_plants():
    return sunflowers.sprites() + pea_shooters_group.sprites() + nuts_group.sprites()

# Grupo de los soles
soles_group = pygame.sprite.Group()