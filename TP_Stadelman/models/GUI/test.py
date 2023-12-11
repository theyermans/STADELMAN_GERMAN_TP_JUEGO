import pygame
import sys
from pygame.locals import *
from GUI_form_prueba import FormPrueba

pygame.init()
WIDTH = 1200
HEIGHT = 600
FPS = 60

reloj = pygame.time.Clock()
pantalla = pygame.display.set_mode((WIDTH, HEIGHT))


form_prueba = FormPrueba(pantalla,200,100, 900, 350,"black", "yellow", 5, True)


while True:
    

    pantalla.fill("Black")
    
    form_prueba.update(eventos)
    
    pygame.display.flip()