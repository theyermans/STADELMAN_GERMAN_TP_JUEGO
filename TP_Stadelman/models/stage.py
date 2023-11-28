import pygame
from auxiliares import TablaPuntajes 
from platforms import Platform
from player import Player
from constantes import GRAVITY
from gergoomba import Gergoomba
import button


# The Stage class represents a stage in a game and contains information about the player, enemies, and
# platforms in that stage.
class Stage:
    def __init__(self, screen: pygame.surface.Surface, limit_w, limit_h, stage_name: str):

        # Jugador
        #self.__configs = open_configs().get(stage_name)
        self.player = Player(pygame.Vector2(limit_w / 2, limit_h /2), pygame.Vector2(limit_w, limit_h), 300 , GRAVITY)
        #self.enemy = Gergoomba(pygame.Vector2(100, 100), pygame.Vector2(limit_w, limit_h), 300 )
        
        self.__player_win = False
        self.__limit_w = limit_w
        self.__limit_h = limit_h
        self.__main_screen = screen
        
        self.enemies : pygame.sprite.Group() = pygame.sprite.Group()
        

        self.plataformas = []
        self.plataformas.append(Platform(pygame.Rect(0,650,1280,100),"assets/Tile (2).png"))
        self.plataformas.append(Platform(pygame.Rect(400,500,468,18),"assets/tile_0000.png"))
        self.plataformas.append(Platform(pygame.Rect(0,500,180,18),"assets/tile_0000.png"))
        self.plataformas.append(Platform(pygame.Rect(1100,500,180,18),"assets/tile_0000.png"))
        self.plataformas.append(Platform(pygame.Rect(250,350,792,18),"assets/tile_0000.png"))
        
        self.score = 0
        self.tabla = TablaPuntajes(self.__main_screen, self.score)
        
        for bullet in self.player.bullet_group:
            if bullet.rect.right <= 0:
                self.player.bullet_group.remove(bullet)
                
        
        self.enemies.add(Gergoomba(pygame.Vector2(100, 100) , pygame.Vector2(limit_w, limit_h) ))

        self.score = 0
        self.tabla = TablaPuntajes(self.__main_screen, self.score)
        self.tabla.muestra_score()

    def run(self, delta_ms):
        # Actualizar todos los grupos de sprites
        # Dibujar todos los grupos de sprites

        # Actualizar y Dibujar Jugador
        
        p:Platform
        for p in self.plataformas:
            p.draw(self.__main_screen)
        self.player.update(delta_ms, self.plataformas)
        self.player.draw(self.__main_screen, delta_ms)
        
        #self.enemies.update(delta_ms, self.__main_screen)
        # self.enemy.update(delta_ms, self.plataformas)
        for e in self.enemies:
            e.update(delta_ms, self.player)
            e.draw(self.__main_screen, delta_ms)
        
        
        self.tabla.muestra_score()
        
        pygame.sprite.groupcollide(self.enemies, self.player.bullet_group , True , True)
        
        
    
                    
        
        
        
        #self.enemies.draw(screen)
        
        
