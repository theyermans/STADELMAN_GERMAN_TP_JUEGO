
import pygame
from pygame.locals import *

from constantes import *
from estadisticas import Estadisticas
from GUI.GUI_form_stages import Stages
from background import Background


from UI.GUI_button import *
from UI.GUI_slider import *
from UI.GUI_textbox import *
from UI.GUI_label import *
from UI.GUI_form import *
from UI.GUI_button_image import *
from GUI.GUI_form_menu_score import *




  
class StartApp(Form):
    
    def __init__(self, screen: pygame.Surface, x: int, y: int, w: int, h: int, color_background=None, color_border=None, border_size: int = -1, active=True, game_instance=None):
        super().__init__(screen, x, y, w, h, color_background, color_border, border_size, active)
        self._x
        self._y
        
        self.stage_seleccionado = False
        self.nombre_stage_seleccionado = ""
        self.flag_play = True
        self.estadisticas = Estadisticas()
        self.volumen = 0.2
        self.screen = screen
        self.game_instance = game_instance
        path_background = "Recursos/bg.png"#json
        #path_background = "./Recursos/table2.png"
        self.static_background = Background(x=0,y=0,width=w,height=h,path=path_background)

        #self.btn_jugar = Button(self, 0, 0, 200, 50, C_GREEN, C_RED, 2, True, None, None, "Jugar", "Arial", 14, C_BLUE, self.btn_jugar_click)
        self.btn_label_nombre = Label(self._slave,x/2,y-160,w/2 ,h/4, "STADEL GAME","Arial",35 , C_BLACK, "Recursos/btn.png")
        
        path_button_stages = "./Recursos/play.png"
        self.btn_jugar = Button_Image(self._slave, x, y, w/2 - 35,h/2 - 25, 75, 75, path_button_stages, 
                                      self.btn_jugar_click, self.btn_home_click,True)
        # (self._slave
        #                               ,x,y, 200, 50, w, h,
        #                               path_button_stages,
        #                             self.btn_jugar_click,self.btn_home_click
        #                             ,True,"Jugar","Arial",12,"Black",(255,0,0))
        
        self.lista_widgets.append(self.btn_jugar)
        self.lista_widgets.append(self.btn_label_nombre)
        #print(self.lista_widgets)
          
    def render(self):
        super().draw()
        self.static_background.draw(self._slave)
        #self._slave.fill(self._color_background)
        #self._slave.fill((52, 78, 91))
        # back_img = pygame.image.load("Recursos/game_background_2.png")
        # back_img = pygame.transform.scale(back_img, (self._x, self._y))
        # self.screen.blit(back_img, self.slave_rect)
        
    def update(self, lista_eventos):
        
        stage_seleccionado = ""

        if self.verificar_dialog_result():
            if self.active:
                self.draw()
                self.render()
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)
                    #print(widget)
                    #print(lista_eventos)
                if self.hijo:
                    stage_seleccionado = self.hijo.update(lista_eventos)
                
        else:
            stage_seleccionado = self.hijo.update(lista_eventos)

        return stage_seleccionado

    def btn_jugar_click(self, param):
        #print("Button Jugar Clicked")
        nuevo_form = Stages(self.screen, self._x, self._y, self._w, self._h)
        """ ,'red' , 5,True """
        #self.show_dialog(nuevo_form)
        if self.verificar_dialog_result():
            if self.active:
                self.show_dialog(nuevo_form)
                self.draw()
                # for widget in self.lista_widgets:
                #     widget.update(lista_eventos)
        else:
            self.hijo.update()
        
    def btn_home_click(self, parametro):
        self.end_dialog()
        
    
        
 
    
                       
    