

import math
import pygame as pg


class Platform (pg.sprite.Sprite) :
    def __init__(self,rect:pg.Rect,texture_path:str,):
        
        self.rect:pg.Rect = rect
        self.texture:pg.image = pg.image.load(texture_path)
        self.tilesX = math.ceil(self.rect.
        width / self.texture.get_width())
        self.tilesY = math.ceil(self.rect.height / self.texture.get_height())
    
   
        
        
    def draw(self,screen:pg.surface.Surface):
        """
        The function draws a texture on the screen by iterating over the tiles and blitting the texture
        at each tile's position.
        
        :param screen: The "screen" parameter is the surface object representing the game window or
        screen on which you want to draw the textures
        """
        for x in range(self.tilesX):
            for y in range(self.tilesY):
                
                screen.blit(self.texture, (self.rect.left + x * self.texture.get_width(),self.rect.top + y *self.texture.get_height()))#donde, tamaño
             
        
        

