import pygame
from pygame.locals import *

from UI.GUI_button import *
from UI.GUI_slider import *
from UI.GUI_textbox import *
from UI.GUI_label import *
from UI.GUI_form import *
from UI.GUI_button_image import *
from GUI.GUI_form_menu_score import *

from estadisticas import Estadisticas
from background import Background
from constantes import *

    
class Stages(Form):
    
    #self,master,x=0,y=0,w=200,h=50,color_background=C_GREEN,color_border=C_RED,image_background=None,text="Button",font="Arial",font_size=14,font_color=C_BLUE,on_click=None,on_click_param=None): 
    def __init__(self, screen: pygame.Surface, x: int, y: int, w:int, h: int, color_background=None, color_border =None, border_size: int = -1, active = True):
    
        super().__init__(screen, x,y,w,h,color_background, color_border, border_size, active)
        
        self.stage_seleccionado= False
        self.nombre_stage_seleccionado=""
        self.estadisticas = Estadisticas()
        path_background = "Recursos/bg.png"#json
        #path_background = "./Recursos/table2.png"
        self.static_background = Background(x=0,y=0,width=w,height=h,path=path_background)
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.flag_play = True
        self.volumen = 0.2
                
        pygame.mixer.init()    
        Music_Controller.play_background_music 
        # Crear una instancia de Music_Controller con volumen inicial
        self.music_controller = Music_Controller(self.volumen)   
        #pygame.mixer.music.load(r"Recursos/Vengeance (Loopable).wav")        
        Music_Controller.adjust_volume(self.volumen)
        #pygame.mixer.music.set_volume(self.volumen)        
        #pygame.mixer.music.play(-1)    
        #nombre para score
        self.txt_nombre = TextBox(self._slave, x, y, 
                                  100, 10, 150, 30, 
                                  "gray","white","red","blue",2,
                                  "Comic Sans MS", 15, "black")
        #stage 1
        path_stage_1 = "./Recursos/1.png"#w/2 - 25 , h/2h/2 - 25,
        self.btn_play = Button_Image(self._slave, x, y, w/2 -300 ,h/2 - 10, 100, 50, path_stage_1, 
                                      self.btn_play_click,"stage_1")
        #stage 2
        path_stage_2 = "./Recursos/2.png"
        self.btn_play_2 = Button_Image(self._slave, x, y, w/2 -250 ,h/2 - 10,100, 50, path_stage_2, 
                                      self.btn_play_click,"stage_2")
        #stage 3
        path_stage_3 = "./Recursos/3.png"
        self.btn_play_3 = Button_Image(self._slave, x, y,  w/2 -190 ,h/2 - 10, 100, 50, path_stage_3, 
                                      self.btn_play_click,"stage_3")
        
        self.slider_volumen = Slider(self._slave, x, y,  w/2 -200 ,h/2 + 70, 500, 15, self.volumen, 
                                     C_BLACK, "white")
        porcentaje_volumen = f"{self.volumen * 100}%"
        self.label_volumen = Label(self._slave,w/2 -300 ,h/2 + 60, 100, 40, porcentaje_volumen,
                                   "Comic Sans MS", 15,"white", "Recursos\Table.png")
        
        # tabla de punttajes
        self.btn_tabla = Button_Image(self._slave, x, y, w/2 +100 ,h/2-20, 75, 75, "Recursos/prize.png", 
                                      self.btn_tabla_click, self.txt_nombre.get_text(),True)#el ultimo true es para que escalee
        #Crear boton home
        self.boton_home = Button_Image(screen = self._slave,
                                       master_x=x,
                                       master_y=y,
                                       x = w-70,
                                       y = h-70,
                                       w = 50,
                                       h = 50,
                                       path_image = "Recursos/wall_button__x1.png", 
                                       onclick = self.btn_home_click,
                                       onclick_param = "")

        
        
        self.lista_widgets.append(self.txt_nombre)#TAKE NAME FOR ESTADISTICAAS
        self.lista_widgets.append(self.btn_play)#START STAGE1
        self.lista_widgets.append(self.btn_play_2)#START STAGE2
        self.lista_widgets.append(self.btn_play_3)#START STAGE3
        self.lista_widgets.append(self.slider_volumen)#SETTINGS MUSIC IN MENU STAAGES FOR NOW...
        self.lista_widgets.append(self.label_volumen)
        self.lista_widgets.append(self.btn_tabla)#SHOW TABLE CHECKING ESTADISTICAS
        
        self.lista_widgets.append(self.boton_home)#RETURN
        
    
    def render(self):
        super().draw()
        #self._slave.fill(self._color_background)
        self.static_background.draw(self._slave)

    def update(self, lista_eventos):
        
        for evento in lista_eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Manejar el evento de clic del ratón
                print("Mouse Clicked in Stages")
                
            
        if self.verificar_dialog_result():
            if self.active:
                self.draw()
                self.render()
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)#POLIMORFISMO
                self.update_volumen(lista_eventos)
                
        else:
            self.hijo.update(lista_eventos)
        
        if self.nombre_stage_seleccionado != "":
            
            return self.nombre_stage_seleccionado
        return ""

    def update_volumen(self, lista_eventos):
        # self.volumen = self.slider_volumen.value
        # self.label_volumen.update(lista_eventos)
        # self.label_volumen.set_text(f"{round(self.volumen * 100)}%")
        # #pygame.mixer.music.set_volume(self.volumen)
        # Music_Controller.adjust_volume(self.volumen)
          # Obtener el nuevo volumen desde el slider u otra fuente
        self.volumen = self.slider_volumen.value

        # Actualizar la etiqueta con el nuevo volumen
        self.label_volumen.update(lista_eventos)
        self.label_volumen.set_text(f"{round(self.volumen * 100)}%")

        # Ajustar el volumen utilizando el controlador de música
        self.music_controller.adjust_volume(self.volumen)
        
    
    def btn_play_click(self, param):
        
        
        # if self.flag_play:
        #    pygame.mixer.music.pause()
        #    self.btn_play._color_background = "blue"
           
        #    self.btn_play.set_text("Play")
        # else:
            
        #     pygame.mixer.music.unpause()
        #     self.btn_play._color_background = "red"
        #     self.btn_play.set_text("Pause")
          
        self.stage_seleccionado = True
        self.nombre_stage_seleccionado = param
        self.flag_play = not self.flag_play
    #RETURN
    def btn_home_click(self,parametro):
        self.end_dialog()
        
    def btn_music_click(self, param):
        if self.flag_play:
           pygame.mixer.music.pause()
           self.btn_play._color_background = "blue"
           
           self.btn_play.set_text("Play")
        else:
            
            pygame.mixer.music.unpause()
            self.btn_play._color_background = "red"
            self.btn_play.set_text("Pause")
        self.flag_play = not self.flag_play
        
    def btn_tabla_click(self, param):
        puntuaciones = self.estadisticas.obtener_puntuaciones()
        print("entre")
        nombre_jugador = param
        jugador_actual = {"Jugador": nombre_jugador, "Score": 0}
        
        #print(puntuaciones)
        diccionario = [{"Jugador": "Mario", "Score": 100},
                       {"Jugador": "Gio", "Score": 150},
                       ]
        diccionario.append(jugador_actual)
        
        
        nuevo_form = FormMenuScore(screen = self._master,
                                   x = self._x  ,
                                   y = self._y-100,
                                   w = self._w,
                                   h = self._h+100,
                                   color_background = "green",
                                   color_border = "gold",
                                   active = True,
                                   path_image = "Recursos/table2.png",
                                   scoreboard = diccionario,
                                   margen_x = 10,
                                   margen_y = 100,
                                   espacio = 10
                                   ,)

        self.show_dialog(nuevo_form)#Modal
"""diccionario = [{"Jugador": "Mario", "Score": 100},
                       {"Jugador": "Gio", "Score": 150},
                       {"Jugador": "Uriel", "Score": 250}]"""
                       
    