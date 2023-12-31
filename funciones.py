import pygame
import sqlite3

#Crea la base de datos si no existe
def crear_bd():
    with sqlite3.connect("db/bd_ranking.db") as conexion:
        try:
            sentencia = ''' create table ranking
                            (
                                id integer primary key autoincrement,
                                name text,
                                score integer
                            )
                        '''
            conexion.execute(sentencia)
            print("Se creo la tabla ranking")
        except sqlite3.OperationalError:
            print("La tabla ranking ya existe")

#Agrega un nuevo puntaje a la base de datos
def update_bd(name,score):
        with sqlite3.connect("db/bd_ranking.db") as conexion:
            try:
                conexion.execute("insert into ranking(name,score) values (?,?)",(name,score))
                conexion.commit()
            except:
                print("Error")

#detecta si se hace click en un rectangulo pasado por parametro
def click(rect)->bool:
    mouse = pygame.mouse.get_pos()
    if rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
        return True