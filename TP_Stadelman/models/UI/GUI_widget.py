import pygame
class Widget:
    def __init__(self, screen: pygame.Surface, x: int, y: int, w: int, h:int, color_background = None, color_border = "Red", 
                 border_size: int = -1):
        
        self._master = screen
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._color_background = color_background
        self._color_border = color_border
        self._slave = None
        self.slave_rect = None
        self.border_size = border_size
        
       
    
    def render(self):
        self.slave_surface = pygame.Surface((self.w,self.h), pygame.SRCALPHA)
        self.slave_rect = self.slave_surface.get_rect()
        self.slave_rect.x = self.x
        self.slave_rect.y = self.y
        self.slave_rect_collide = pygame.Rect(self.slave_rect)
        self.slave_rect_collide.x += self._master.x
        self.slave_rect_collide.y += self._master.y

        if self._color_background:
            self.slave_surface.fill(self._color_background)
       
        
        
        # if self.image_background:
        #     self.slave_surface.blit(self.image_background,(0,0))
        
        # if(self._text != None):
        #     image_text = self._font_sys.render(self._text,True,self._font_color,self.color_background)
        #     self.slave_surface.blit(image_text,[
        #         self.slave_rect.width/2 - image_text.get_rect().width/2,
        #         self.slave_rect.height/2 - image_text.get_rect().height/2
        #     ])
            
        # if self.color_border:
        #     pygame.draw.rect(self.slave_surface, self.color_border, self.slave_surface.get_rect(), 2)
    
    def update(self, lista_eventos):
        pass
    
    def draw(self):
        self._master.blit(self._slave,self.slave_rect)
        #pygame.draw.rect(self._master, self._color_border, self.slave_rect, self.border_size)
        