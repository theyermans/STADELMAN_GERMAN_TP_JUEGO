import pygame
from pygame.locals import *
from gui_widget import Widget
from constantes import *


class Button(Widget):
    def __init__(self,master,x=0,y=0,w=200,h=50,color_background=(0,255,0),color_border=(255,0,0),image_background=None,text="Button",font="Arial",font_size=14,font_color=(0,0,255),on_click=None,on_click_param=None):
        super().__init__(master,x,y,w,h,color_background,color_border,image_background,text,font,font_size,font_color)
        self.on_click = on_click
        self.on_click_param = on_click_param
        self.state = 0
        self.render()
        
    def render(self):
        super().render()
        if self.state == 1: # Se aclara la imagen
            self.slave_surface.fill((32,32,32), special_flags=pygame.BLEND_RGB_ADD) 
        elif self.state == 3: # Se oscurece la imagen
            self.slave_surface.fill((32,32,32), special_flags=pygame.BLEND_RGB_SUB) 

    def update(self,lista_eventos):
        mousePos = pygame.mouse.get_pos()
        self.state = 0
        if self.slave_rect_collide.collidepoint(mousePos):
            if(pygame.mouse.get_pressed()[0]):
                self.state = 3
            else:
                self.state = 1
              
        for evento in lista_eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if(self.slave_rect_collide.collidepoint(evento.pos)):
                    self.on_click(self.on_click_param)

        self.render()

    

