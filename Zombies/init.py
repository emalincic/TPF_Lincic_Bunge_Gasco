import pygame
from zombies import sprites, game

def initialization_of_game():
    pygame.init()
    pygame.mixer.init()
    w, h = 1200, 800
    screen = pygame.display.set_mode((w,h))
    pygame.display.set_caption('Plants vs Zombies 2')
    frames = pygame.time.Clock()
    
    zombie, ADDZOMBIE, lawnmowers = sprites()
    
    pygame.mixer.music.load('Zombies\The Zombies Are coming Sound Effect.mp3')
    pygame.mixer.music.set_volume(1.0) 
    pygame.mixer.music.play(0)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        try:
            background = pygame.image.load('Zombies/images/mapa_pvz.png').convert()
            background = pygame.transform.scale(background, (w, h))
        except pygame.error as e:
            print(f"No se pudo cargar la imagen de fondo: {e}") 
            background = pygame.Surface((w, h))
            background.fill((225, 0, 0))
        
        screen.blit(background, (0,0))
        
        game(events, zombie, screen, ADDZOMBIE, lawnmowers)
        pygame.display.update()
        frames.tick(60)
initialization_of_game()