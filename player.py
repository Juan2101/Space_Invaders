import pygame
from laser import Laser
from constantes import *

lasers = pygame.sprite.Group()

class Player:
    def __init__(self,screen) -> None:
        self.superficie = pygame.image.load("img/player.png").convert_alpha()
        self.rect = self.superficie.get_rect(midbottom = (screen.get_rect().width/2,screen.get_rect().height))
        self.laser_flag = True
        self.laser_time = 0
        self.score = 0
        self.health = 3
        self.explosion_audio = pygame.mixer.Sound("audio/explosion.wav")
        self.explosion_audio.set_volume(0.5)
        self.explosion_enemy_audio = pygame.mixer.Sound("audio/explosion.wav")
        self.laser_audio = pygame.mixer.Sound("audio/laser.wav")

    def display_score(self,screen,font):
        score_superficie = font.render(f"Score: {self.score}",False,COLOR_WHITE)
        score_rect = score_superficie.get_rect(topleft = (5,-5))

        screen.blit(score_superficie,score_rect)

    def display_health(self,screen,font,enemies):
        for enemy in enemies:
            if pygame.sprite.spritecollide(self,enemy.laser,True):
                self.health -= 1
                self.explosion_audio.play()
        if pygame.sprite.spritecollide(self,enemies,False):
            self.health = 0
            self.explosion_audio.play()

        health_icon = pygame.image.load("img/health.png").convert_alpha()
        health_icon_rect = health_icon.get_rect(topright = (535,7))

        health_superficie = font.render(f" x{self.health}",False,COLOR_WHITE)
        health_rect = health_superficie.get_rect(topright = (595,-5))

        screen.blit(health_icon,health_icon_rect)
        screen.blit(health_superficie,health_rect)

    def update(self,screen,enemies):
        keys = pygame.key.get_pressed()
        if True in keys:
            if keys[pygame.K_RIGHT]:
                new_pos = self.rect.x + 3
                if new_pos < screen.get_rect().width - self.rect.width:
                    self.rect.x += 3
            elif keys[pygame.K_LEFT]:
                new_pos = self.rect.x - 3
                if new_pos > 0:
                    self.rect.x -= 3

            if keys[pygame.K_SPACE] and self.laser_flag:
                lasers.add(Laser(self.rect,COLOR_BLUE,-5))
                self.laser_audio.play()
                self.laser_time = pygame.time.get_ticks()
                self.laser_flag = False

        if not self.laser_flag:
            time = pygame.time.get_ticks()
            if time - self.laser_time >= PLAYER_RECHARGE:
                self.laser_flag = True

        if pygame.sprite.groupcollide(lasers,enemies,True,True):
            self.explosion_audio.play()
            self.score += 100
        
        lasers.update(screen)
        screen.blit(self.superficie,self.rect)
        