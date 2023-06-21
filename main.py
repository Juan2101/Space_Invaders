import pygame
import sqlite3
from player import Player
from enemy import Enemy
from funciones import *
from constantes import *

pygame.init()

screen = pygame.display.set_mode([SCREEN_X,SCREEN_Y])
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
font = pygame.font.Font("font/Pixeled.ttf",20)
music = pygame.mixer.Sound("audio/music.wav")
music.set_volume(0.2)
music.play(loops = -1)  
crear_bd()

fondo = pygame.image.load("img/fondo.png").convert()
player = Player(screen)
enemies = pygame.sprite.Group()
name = ""

#Variables para el manejo de las pantallas
run = True
playing_screen = False
game_over_screen = False
ranking_screen = False

#Evento para agregar enemigos
enemies_spawn = pygame.USEREVENT + 0
pygame.time.set_timer(enemies_spawn,2000)

#--------------------- Superficies estaticas ---------------------------------
title_font = font.render("Space Invaders",False,COLOR_WHITE)
title_rect = title_font.get_rect(center = (300,170))

start_button_superficie = pygame.image.load("img/start_button.png").convert_alpha()
start_button_rect = start_button_superficie.get_rect(center = (300,300))

ranking_button_font = font.render("Ranking",False,COLOR_WHITE,)
ranking_button_rect = ranking_button_font.get_rect(center = (300,430))

game_over_font = font.render("Game Over",False,COLOR_WHITE)
game_over_rect = game_over_font.get_rect(center = (300,250))

continue_button_superficie = font.render("continue",False,COLOR_RED)
continue_button_rect = continue_button_superficie.get_rect(center = (300,500))

ranking_font = font.render("Ranking",False,COLOR_RED,)
ranking_rect = ranking_font.get_rect(center = (300,100))

back_button_superficie = font.render("back",False,COLOR_WHITE,)
back_button_rect = back_button_superficie.get_rect(bottomright = (590,590))

#Muestra la pantalla de inicio
def display_home():
    screen.blit(title_font,title_rect)
    screen.blit(start_button_superficie,start_button_rect)
    screen.blit(ranking_button_font,ranking_button_rect)

#Muestra el juego
def display_game():
    player.update(screen,enemies)
    player.display_score(screen,font)
    player.display_health(screen,font,enemies)
    enemies.update(screen)

#Muesta la pantalla de fin del juego con el puntaje
def display_game_over(name,score):
    final_score_font = font.render(f"Score: {score}",False,COLOR_WHITE)
    final_score_rect = final_score_font.get_rect(center = (300,300))

    name_font = font.render(f"name: {name}",False,COLOR_WHITE)
    name_rect = name_font.get_rect(center = (300, 400))
    
    screen.blit(continue_button_superficie,continue_button_rect)
    screen.blit(name_font,name_rect)
    screen.blit(game_over_font,game_over_rect)
    screen.blit(final_score_font,final_score_rect)  

#Muesta la pantalla de puntuaciones con las 5 mas altas
def display_ranking():
    with sqlite3.connect("db/bd_ranking.db") as conexion:
        cursor = conexion.execute("SELECT name,score FROM ranking order by score desc limit 5")
        separador = 200 #se ultiliza para tener un espacio entre los puntajes
        posicion = 1
        for i in cursor:
            rankig_info_superficie = font.render(f"{posicion} - {i[0]} {i[1]}",False,COLOR_WHITE)
            ranking_info_rect = rankig_info_superficie.get_rect(center = (300,separador))
            posicion += 1
            separador += 50
            screen.blit(rankig_info_superficie,ranking_info_rect)
    
    screen.blit(ranking_font,ranking_rect)
    screen.blit(back_button_superficie,back_button_rect)

#--------------------- loop principal ----------------------------------
while run:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
        if i.type == enemies_spawn and playing_screen:
            if len(enemies) < 5: #Solo pude haber 5 enemigos en pantalla
                enemies.add(Enemy(screen))
        #Tipeo del nombre del jugador
        if i.type == pygame.KEYDOWN and game_over_screen:
            if i.key == pygame.K_BACKSPACE:
                name = name[0:-1]
            elif i.key == pygame.K_RETURN:
                    #Setea las variables para una nueva partina y vuelve a la pantalla de inicio
                    update_bd(name,player.score)
                    player = Player(screen)
                    enemies = pygame.sprite.Group()
                    name = ""
                    playing_screen = False
                    game_over_screen = False
            elif len(name) <= 10:
                name += i.unicode

    screen.blit(fondo,(0,0))

    #Manejo de las distintas pantallas
    if playing_screen:
        if not game_over_screen:
            #pantalla del juego
            display_game()
            if player.health == 0:
                game_over_screen = True
        elif game_over_screen:
            #pantalla de fin del juego
            display_game_over(name,player.score)
            if click(continue_button_rect):
                #Setea las variables para una nueva partina y vuelve a la pantalla de inicio
                update_bd(name,player.score)
                player = Player(screen)
                enemies = pygame.sprite.Group()
                name = ""
                playing_screen = False
                game_over_screen = False
    elif ranking_screen:
        #pantalla de puntuaciones
        display_ranking()
        if click(back_button_rect):
            ranking_screen = False
    else:
        #pantalla de inicio
        display_home()
        playing_screen = click(start_button_rect)
        ranking_screen = click(ranking_button_rect)
    
    clock.tick(60)
    pygame.display.flip()

pygame.quit()