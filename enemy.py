import pygame
import random
from laser import Laser
from constantes import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self,screen) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.superficie = pygame.image.load("img/red.png").convert_alpha()
        self.width = self.superficie.get_rect().width
        self.height = self.superficie.get_rect().height
        self.rect = self.superficie.get_rect(topleft = (random.choice((0,screen.get_rect().width - self.width - 2)),random.randrange(50,self.height * 3 + 50,self.height + 50)))
        self.speed = random.randrange(1,3)
        self.flag = True
        self.laser = pygame.sprite.Group()
        self.laser_time = pygame.time.get_ticks()
        self.laser_audio = pygame.mixer.Sound("audio/laser.wav")
        self.laser_audio.set_volume(0.5)

    def update(self,screen):
        if(self.rect.x < (screen.get_rect().width - self.width)) and self.flag:
            self.rect.x += self.speed
            if self.rect.x == screen.get_rect().width - self.width:
                self.rect.y += self.height
                self.flag = False
        elif self.rect.x >= 0:
            self.rect.x -= self.speed
            if self.rect.x == 0:
                self.rect.y += self.height
                self.flag = True
        
        if pygame.time.get_ticks() - self.laser_time >= ENEMY_RECHARGE:
            self.laser.add(Laser(self.rect,COLOR_RED,3))
            self.laser_time = pygame.time.get_ticks()
            self.laser_audio.play()

        self.laser.update(screen)
        screen.blit(self.superficie,self.rect)