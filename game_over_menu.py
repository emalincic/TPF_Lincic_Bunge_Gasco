import pygame
import os
def show_game_over(screen):
    font_big = pygame.font.Font("04B_03__.TTF", 120)
    font_small = pygame.font.Font("04B_03__.TTF", 40)

    text_title  = font_big.render("PERDISTE", True, (250, 30, 30))
    text_hint   = font_small.render("Presiona cualquier tecla", True, (255, 255, 255))

    
    screen.fill((0, 0, 0))
    screen.blit(
        text_title,
        text_title.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 60))
    )
    screen.blit(
        text_hint,
        text_hint.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 40))
    )
    pygame.display.flip()
    pygame.mixer.Sound(os.path.join('Audio', "The Zombies Ate Your Brains! - Player's House - Plants vs. Zombies 2.mp3")).play()
    
    waiting = True
    while waiting:
        for ev in pygame.event.get():
            if ev.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                waiting = False
        pygame.time.Clock().tick(60)
    return True          