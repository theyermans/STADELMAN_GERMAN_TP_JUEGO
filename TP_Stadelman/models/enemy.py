
import pygame as pg
from constantes import CONFIG_FILE_PATH, GRAVITY, ConfigManager
from pygame.sprite import Sprite


class Enemy(Sprite):
    
    def __init__(self, pos, speed, constraint,facingDirection=pg.Vector2(1,0),stage_name="stage_1"):
        super().__init__()
        # self.__configs = open_configs().get(stage_name)
        self.__configs = ConfigManager.load_configs(self,CONFIG_FILE_PATH)
        # print(self.__configs)
        self.configs_stage = self.__configs.get(stage_name,"stage_1")
        #esto voy a tener que hacer una variable globar que se llame stage seleccionado
        # Atributos de movimiento
        self.pos: pg.Vector2 = pos
        self.speed = speed-100 #lo que se mueve en x por parametro a pasar a json
        self.constrains: pg.Vector2 = constraint #restriccion en vector es una tupla (x,y)
        self.movement = pg.Vector2(1, 0)
        self.gravity_speed = GRAVITY
        self.on_ground: bool = False
        self.facingDirection: pg.Vector2 = facingDirection
        self.images = {}
        self.rect : pg.Rect
 
        self.state : str = ""
        
        self.frame_duration_ms = 1000 / 30
        self.frame_elapsed_time = self.frame_duration_ms    
        self.current_frame = 0
        
        self.hp_enemy :int
    
        self.hp_enemy = self.__configs.get("hp_enemy",50)
        self.damage = self.__configs.get("hp_enemy",50)
        
    def draw(self, screen,delta_ms: float):
        if(self.current_frame >= len(self.images[self.state])):
            self.current_frame = 0
        screen.blit(self.images[self.state][self.current_frame], (self.rect.topleft))
         # Dibujar la hitbox en rojo para mejor visibilidad
        pg.draw.rect(screen, (255, 0, 0), self.rect, 2)
        
        
    def move(self, delta_ms):
        self.pos += self.facingDirection * self.speed * (delta_ms / 1000)   
        if(not self.on_ground):
            self.movement.y += self.gravity_speed
        else:
            self.movement.y = 0
        #Aca ajustamos las hitbox para que siempre sigan al bbaat en la posicion correcta
        self.rect.topleft = (self.pos.x, self.pos.y)
        if self.pos.x >= self.constrains.x - 64:
            self.facingDirection.x = -1
        if self.pos.x <= 0 :
            self.facingDirection.x = 1

    def update(self, delta_ms, player=None):
        self.update_frame(delta_ms)
        self.move(delta_ms)
    def update_frame(self, delta_ms):
            self.frame_elapsed_time -= delta_ms
            if(self.frame_elapsed_time <= 0):
                self.frame_elapsed_time = self.frame_duration_ms
                self.current_frame += 1
                if(len(self.images[self.state]) <= self.current_frame):
                    self.current_frame = 0