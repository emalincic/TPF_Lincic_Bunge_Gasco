import pygame


    


class Lawnmower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        image = pygame.image.load('images/lawnmower.png').convert_alpha()
        self.image = pygame.transform.scale(image, (70, 50))
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = 0
        self.active = False
        
    def movement(self, zombies):
        if not self.active:
            if pygame.sprite.spritecollideany(self, zombies):
                self.active = True
                self.speed = 8
        else:
            self.rect.x += self.speed
            pygame.sprite.spritecollide(self, zombies, True)
            if self.rect.left > 1200:
                self.kill()

def add_lawnmowers():
    lawnmowers = pygame.sprite.Group()
    for i in range(5):
        mower = Lawnmower(240,250 + i*100 )
        lawnmowers.add(mower)
    return lawnmowers