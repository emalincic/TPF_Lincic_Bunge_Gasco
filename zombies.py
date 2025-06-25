import os
import pygame
import random
import utils as UT
from utils import GAME_OVER

pygame.mixer.init()
class Zombies(pygame.sprite.Sprite):
    """Zombi base utilizado en ambos modos de juego.
    Cada zombi se comporta como un sprite de Pygame que avanza de derecha
    a izquierda,
    Dispara un evento `GAME_OVER` si logra atravesar toda la pantalla.
    Entradas
        1. zombie_type (dict): Diccionario con las propiedades del zombi
            (clave/valor: "health", "speed", "image").
        2. random_z (str): Etiqueta descriptiva del tipo de zombi (p. ej.
            "Normal", "ConeHead", etc.).
    """
    def __init__(self, zombie_type, random_z: str):
        super().__init__()
        self.zombie_type = zombie_type
        self.health = zombie_type["health"]
        self.speed = zombie_type["speed"]
        self.image = os.path.join("Images", zombie_type["image"][0])
        self.max_health = zombie_type["health"]
        self.id = random.randint(0, 100000)
        self.type = random_z
        self.start_time = pygame.time.get_ticks()
        self.eating_sound = pygame.mixer.Sound(os.path.join('Audio', 'zombies eating sound.mp3'))
        self.Channel = pygame.mixer.Channel(0)
        self.eating = False
        

        raw = pygame.image.load(self.image).convert_alpha()
        _ , c_h = UT.cell_size()
        self.surf = pygame.transform.scale(raw, (int(c_h * 1.0), int(c_h * 0.9)))

        self.cx, self.cy = UT.cell_center(10, 6, "zombie")
        self.rect = self.surf.get_rect(center=(self.cx, self.cy))
        self.x = float(self.rect.x)

    def movement(self) -> None:
        """Avanza el zombi y comprueba si llega al extremo izquierdo.
        Cuando "self.rect.right" cruza el borde izquierdo se emite un
        evento "GAME_OVER" y el sprite se elimina.
        """
        self.x -= self.speed
        self.rect.x = int(self.x)
        if self.rect.right <= 0:
            pygame.event.post(pygame.event.Event(GAME_OVER))  
            self.kill()
            
    def selfdamage(self, dmg: int = 20)-> None:
        """Aplica daño al zombi; lo elimina si la salud llega a 0.

        Entradas:
            1. dmg (int, optional): Cantidad de daño a infligir.  
                Default = 20.
        """
        self.health -= dmg
        if self.health <= 0:
            self.kill()
    
    def sound(self) -> None:
        """Inicia o detiene el sonido de masticar según self.eating."""

        if self.eating:
            self.Channel.play(self.eating_sound, loops=-1)
        else:
            self.Channel.stop()

    def ready_to_hit(self)-> bool:
        """Determina si pasó suficiente tiempo para volver a atacar.

        Returns:
            bool: "True" si han transcurrido ≥ 1.5 s desde el último golpe.
        """
        if not hasattr(self, "_ready_time"):
            self._ready_time = pygame.time.get_ticks()
            return True
        if pygame.time.get_ticks() - self._ready_time >= 1500:
            self._ready_time = pygame.time.get_ticks()
            return True
        return False
    
    
class balloon(Zombies): 
    """Zombi con globo: flota y se mueve más rápido hasta que sufre daño."""
    def __init__(self, zombie_type, random_z):
        super().__init__(zombie_type, random_z)
    def balloon_ability(self):
        """Reduce la velocidad y cambia sprite al pincharse el globo.

        Cuando la salud cae por debajo del 40 %:
        * se reduce la velocidad a 0.35 px/frame,
        * se reasigna el tipo a ``'Normal'``,
        * se cambia la imagen a “Balloonzombie2.png”.
        """
        if self.health < self.max_health * 0.4:
            self.speed = 0.35
            self.type = 'Normal'
            self.image = os.path.join("Images","Balloonzombie2.png")
            raw = pygame.image.load(self.image).convert_alpha()
            c_w, c_h = UT.cell_size()
            self.surf = pygame.transform.scale(raw, (int(c_h * 1.0), int(c_h * 0.9)))
            self.rect = self.surf.get_rect(center=(self.cx, self.cy))