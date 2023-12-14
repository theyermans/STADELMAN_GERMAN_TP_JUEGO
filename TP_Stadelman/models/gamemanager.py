import sys
import pygame
from pygame import*
from constantes import*
from gui_form_menu_A import FormMenuA
from gui_form import*
class GameManager:
    
    
    def __init__(self):
        pygame.init()
        flags = DOUBLEBUF
        self.screen = pygame.display.set_mode((screen_w, screen_h), flags, 16)
        self.clock = pygame.time.Clock()

        # Crear instancias de formularios
        self.form_menu_A = FormMenuA(name="form_menu_A", master_surface=self.screen, x=300, y=200, w=500, h=400,
                                     color_background=(255, 255, 0), color_border=(255, 0, 255), active=True)
        # ... crea otros formularios ...
        self.boton3 = Button(master=self,x=20,y=140,w=140,h=50,color_background=None,color_border=None,image_background="images/gui/set_gui_01/Comic_Border/Buttons/Button_M_02.png",on_click=self.on_click_boton3,on_click_param="form_game_L1",text="JUGAR",font="Verdana",font_size=30,font_color=C_WHITE)
    def run(self):
        while True:
            lista_eventos = pygame.event.get()
            for event in lista_eventos:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            delta_ms = self.clock.tick(FPS)

            aux_form_active = Form.get_active()
            if aux_form_active is not None:
                aux_form_active.update(lista_eventos, keys, delta_ms)
                aux_form_active.draw()

            pygame.display.flip()

if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.run()