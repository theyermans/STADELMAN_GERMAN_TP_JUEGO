import random
import pygame as pg
from constantes import GRAVITY
from pygame.sprite import Sprite


class Enemy(Sprite):
    
    def __init__(self, pos, speed, constraint):
        super().__init__()
        
        # Atributos de movimiento
        self.pos: pg.Vector2 = pos
        self.speed = speed #lo que se mueve en x por parametro a pasar a json
        self.constrains: pg.Vector2 = constraint #restriccion en vector es una tupla (x,y)
        self.movement = pg.Vector2(0, 0)
        self.gravity_speed = GRAVITY
        self.on_ground: bool = False
        self.facingDirection: pg.Vector2 = pg.Vector2(1,0)
        self.images = {}
        self.rect : pg.Rect
        
        
        #self.botom_hitbox:pg.Rect = pg.Rect(self.pos.x, self.pos.y + 64 , 30, 1) #mas 64 porque es el ancho de pileles del personaje en la parte derecha del mismo
        #self.left_hitbox:pg.Rect = pg.Rect(self.pos.x - 1 , self.pos.y , 1, 40) #-1 porq es la parte izquierda
        #self.right_hitbox:pg.Rect = pg.Rect(self.pos.x + 64 , self.pos.y, 1, 40) #+64 porq es la parte de abajo del personaje por su cantidad de pixees
        #self.__player_configs = stage_dict_configs.get('player')
        # Mostrar sprite del jugador
        self.state : str = ""
        
        self.frame_duration_ms = 1000 / 30
        self.frame_elapsed_time = self.frame_duration_ms    
        self.current_frame = 0
        
        
        
    def draw(self, screen,delta_ms: float):
        if(self.current_frame >= len(self.images[self.state])):
            self.current_frame = 0
        screen.blit(self.images[self.state][self.current_frame], self.rect.bottomleft)
        
    def move(self, delta_ms):
        self.pos += self.facingDirection * self.speed * (delta_ms / 1000)   
        
        if(not self.on_ground):
            self.movement.y += self.gravity_speed
            
        else:
            self.movement.y = 0

        #Aca nos aseguramos que el personaje se mantenga dentro de la pantalla
        self.pos.x = pg.math.clamp(self.pos.x, 0, self.constrains.x - 64)
        self.pos.y = pg.math.clamp(self.pos.y, 0, self.constrains.y)
        
        #Aca ajustamos las hitbox para que siempre sigan al personaje en la posicion correcta
        self.rect.topleft = (self.pos.x, self.pos.y)
        if self.pos.x == self.constrains.x - 64:
            self.facingDirection.x = -1
        if self.pos.x == 0 :
            self.facingDirection.x = 1
            
    def shoot (self):
        pass
    
    def check_collision_with_player(self, player):
        return self.rect.colliderect(player.rect)
    
    def update(self, delta_ms, player=None):
        self.update_frame(delta_ms)
        self.move(delta_ms)
        if player is not None:
            # Check for collision with the player
            if self.check_collision_with_player(player):
                # Handle collision with the player (e.g., decrease player's health)
                player.receive_damage()
        
        
        
        
        
    def update_frame(self, delta_ms):
            self.frame_elapsed_time -= delta_ms
            if(self.frame_elapsed_time <= 0):
                self.frame_elapsed_time = self.frame_duration_ms
                self.current_frame += 1
                if(len(self.images[self.state]) <= self.current_frame):
                    self.current_frame = 0