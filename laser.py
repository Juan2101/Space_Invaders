import pygame
from constantes import *

class Laser(pygame.sprite.Sprite):
    def __init__(self,player,color,speed) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(player.x + player.width/2 - 2.5,player.y,LASER_WIDTH,LASER_HEIGHT)
        self.color = color
        self.speed = speed
    
    def update(self,screen):
        #Verifica que el laser este dentro de la ventana
        if self.rect.y <= -LASER_HEIGHT or self.rect.y >= screen.get_rect().height + LASER_HEIGHT:
            self.kill()
        self.rect.y += self.speed
        pygame.draw.rect(screen,self.color,self.rect)