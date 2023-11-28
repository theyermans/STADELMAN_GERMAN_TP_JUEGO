import pygame as pg
from pygame.sprite import Sprite
from auxiliares import *

class Bullet(Sprite):
    def __init__ (self, pos , direction):
        super().__init__()#lo que hacemos es heredar todos su metodo init
        
        
        
        
        self.pos:pg.Vector2 = pos 
        self.direction :pg.Vector2 = direction
        self.rect : pg.Rect = pg.Rect(self.pos.x , self.pos.y, 10 , 10)
        self.speed_blade = 800
        self.path_blade = "assets/Bullet/On (38x38).png"
        
        self.hitbox : pg.Rect
        self.state : str = ""
        self.frame_duration_ms = 1000 / 30
        self.frame_elapsed_time = self.frame_duration_ms    
        self.current_frame = 0
        
            
        self.images = {}
        self.images["bullet"] = SurfaceManager.get_surface_from_spritesheet1x(self.path_blade, 8, 1, 1, True)
        #self.hitbox = pg.Rect(pos.x, pos.y, self.images["bullet"][0].get_width (), self.images["bullet"][0].get_height () )
        
        
    def update(self, delta_ms):
        self.pos += self.direction * self.speed_blade * (delta_ms / 1000)# direccion mirando multipliucado por velocidad por el tiempo en milisegundos
        self.rect.topleft = (self.pos.x,self.pos.y)
        self.frame_elapsed_time -= delta_ms #restas el tiempo transcurrido del coldown de la animacion
        
        if(self.frame_elapsed_time <= 0):#coldown del cuadro
            self.frame_elapsed_time = self.frame_duration_ms#reseteo cuando llega a 0
            self.current_frame += 1#aumento en uno el cuadro actual
            if(len(self.images["bullet"]) <= self.current_frame):#chekeo que no me paso del total de cuadros
                self.current_frame = 0#al comienzo si me pase
        
    def draw(self, screen, delta_ms: float):
        if not self.images:
            return  # Images not loaded yet

        if self.current_frame >= len(self.images["bullet"]):
            self.current_frame = 0

        screen.blit(self.images["bullet"][self.current_frame], self.rect.bottomleft)
        # pg.draw.rect(screen, "BLACK", self.rect)
        
        
    


