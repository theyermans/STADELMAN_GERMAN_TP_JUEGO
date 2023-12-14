

import math
import pygame as pg

from auxiliares import SurfaceManager


class Platform (pg.sprite.Sprite) :
    def __init__(self,rect:pg.Rect,texture_path:str):
        
        self.rect:pg.Rect = rect
        self.texture:pg.image = pg.image.load(texture_path)
        self.tilesX = math.ceil(self.rect.width / self.texture.get_width())
        self.tilesY = math.ceil(self.rect.height / self.texture.get_height())#para manejar siempre sumero redondos
    
   
        
        
    def draw(self,screen:pg.surface.Surface):
        for x in range(self.tilesX):
            for y in range(self.tilesY):
                
                screen.blit(self.texture, (self.rect.left + x * self.texture.get_width(),self.rect.top + y *self.texture.get_height()))#donde, tamaño

class Tramp(Platform):
    def __init__(self, rect: pg.Rect, time_per_state: int):
        super().__init__(rect, "assets/Off.png")  # Inicializar con la imagen "off"
        self.images = {}
        # Path hardcodeado para el estado "on"
        self.images["on"] = SurfaceManager.get_surface_from_spritesheet("assets/On (16x32).png", 3, 1)
        self.state = "on"
        self.time_per_state = 1000 / 15
        self.elapsed_time = self.time_per_state   # Agrega esta línea
        self.current_frame = 0
        self.texture_trap = self.images[self.state][self.current_frame]

        # Set hitbox size based on the texture
        self.rect.width = self.texture_trap.get_width()
        self.rect.height = self.texture_trap.get_height()
    def update(self, screen, delta_ms: int):
        self.elapsed_time += delta_ms
        # Cambiar de estado si ha pasado el tiempo necesario
        if self.elapsed_time >= self.time_per_state:
            self.elapsed_time = 0
            self.current_frame += 1

            # Si se llega al final de los frames del estado actual, reiniciar
            if self.current_frame >= len(self.images[self.state]):
                self.current_frame = 0
            # Actualizar la textura actual en función del estado y el frame
            self.texture_trap = self.images[self.state][self.current_frame]

    def draw(self, screen, delta_ms: float):
        pg.draw.rect(screen, (255, 0, 0), self.rect, 2)
        # Repetir la textura en una cuadrícula
        for x in range(self.tilesX):
            for y in range(self.tilesY):
                screen.blit(self.texture_trap, (self.rect.left + x * self.texture_trap.get_width(), self.rect.top + y * self.texture_trap.get_height()))
                # Dibujar la hitbox para cada repetición
                hitbox_rect = self.rect.move(x * self.texture_trap.get_width(), y * self.texture_trap.get_height())
                pg.draw.rect(screen, (255, 0, 0), hitbox_rect, 2)
        
        
"""class Tramp(Platform):
    def __init__(self, rect: pg.Rect, time_per_state: int):
        super().__init__(rect, "assets/Off.png")  # Inicializar con la imagen "off"
        
        # # Paths hardcodeados para cada estado
        # self.images = {
        #     "off": "assets/Off.png",
        #     "turn": "assets/Hit (16x32).png",
        #     "on": "assets/On (16x32).png",
        # }

        # for key, path in self.images.items():
        #     print(key)
        #     if path:
        #         if key in {"off", "turn", "on"}:
        #             if key == "off":
        #                 self.images[key] = SurfaceManager.get_surface_from_spritesheet(path, 1, 1)
        #             if key == "turn":
        #                 self.images[key] = SurfaceManager.get_surface_from_spritesheet(path, 4, 1)
        #             if key == "on":
        #                 self.images[key] = SurfaceManager.get_surface_from_spritesheet(path, 3, 1)
        # self.states = list(self.images.keys())
        # self.current_state = 0
        # self.current_frame = 0  # Agregar esta línea
        # self.time_per_state = time_per_state
        # self.elapsed_time = 100

        # self.state = "off"
        # self.texture_trap = self.images[self.state]
        
        # Paths hardcodeados para cada estado
        self.images = {
            "off": SurfaceManager.get_surface_from_spritesheet("assets/Off.png", 1, 1),
            "turn": SurfaceManager.get_surface_from_spritesheet("assets/Hit (16x32).png", 4, 1),
            "on": SurfaceManager.get_surface_from_spritesheet("assets/On (16x32).png", 3, 1),
        }

        self.states = list(self.images.keys())
        self.current_state = 0
        self.current_frame = 0
        self.time_per_state = time_per_state
        self.elapsed_time = 0

        self.state = "off"
        self.texture_trap = self.images[self.state]
        
   
    def update(self, screen, delta_ms: int):
        self.elapsed_time += delta_ms

        # Cambiar de estado si ha pasado el tiempo necesario
        if self.elapsed_time >= self.time_per_state:
            self.elapsed_time = 0
            self.current_state = (self.current_state + 1) % len(self.states)
            self.state = self.states[self.current_state]
            print(f"Changing state to {self.state}")
            self.texture_trap = self.images[self.state]

    def draw(self, screen, delta_ms: float):
        # Dibujar la superficie actual
        screen.blit(self.texture_trap, self.rect.topleft)
        
    # def update(self, screen, delta_ms: int):
        
        
    #     self.elapsed_time += delta_ms
        

        
     
            
    # def draw(self, screen,delta_ms: float):
        
            
    #     if(self.current_frame >= len(self.images[self.state])):
    #         self.current_frame = 0
    #     screen.blit(self.images[self.state][self.current_frame], self.rect.topleft)
        
        """