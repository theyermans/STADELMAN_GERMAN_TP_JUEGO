import time
import pygame
import sys
import button
from GUI.GUI_form_start_app import StartApp
from GUI.GUI_form_stages import Stages
from stopwatch import Stopwatch
from stage import Stage
from constantes import (FPS, screen_h, screen_w)
#from GUI.GUI_form_stages import Stages
from estadisticas import Estadisticas


#from GUI.UI.GUI_textbox import TextBox


class Game:

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((screen_w, screen_h))
        self.clock = pygame.time.Clock()
        self.game_paused = False

        
        self.stage = None
    def start(self):
        pygame.init()
        stage_seleccionado = ""
        screen = pygame.display.set_mode((screen_w, screen_h))
        clock = pygame.time.Clock()
        back_img = pygame.image.load("Recursos/game_background_2.png")
        back_img = pygame.transform.scale(back_img, (screen_w, screen_h))
        #cambiar por StartApp
        start_app = StartApp(screen,(screen_w/2) - (screen_w/4) ,(screen_h/2) - (screen_h/4),screen_w/2,screen_h/2,None,"red",5,True)
        
        nombre_stage = ""
        estadisticas = Estadisticas()
       
        game_instance = Game()
        # Crear una instancia de la clase Stage con la instancia de Game como argumento
        stage_instance = Stage(screen, (screen_w/2) - (screen_w/4) , (screen_h/2) - (screen_h/4), game_instance, stage_name="stage_1")
        lista_niveles=["stage_1", "stage_2", "stage_3"]

        while stage_seleccionado not in lista_niveles:
        #hile stage_seleccionado != "stage_1":
            clock.tick(FPS)
            eventos = pygame.event.get()
            for event in eventos:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            screen.blit(back_img, back_img.get_rect())
            stage_seleccionado = start_app.update(eventos)
            #print(eventos)
            if stage_seleccionado != "":
                print("Hola")
            
            pygame.display.flip()
    
            #screen.blit(back_img, back_img.get_rect())
            # Obtener el texto ingresado en el cuadro de texto
            #texto_ingresado = start_app.txt_nombre.get_text()
            #aca tengo que ciclar los eventos
            #stage_seleccionado = Stages.update(eventos)
            #pygame.display.flip()
            
           
            
        
        Game.run_stage(stage_seleccionado)  
         
           
    def run_stage(stage_name: str ):
        pygame.init()
        time_paused=0
        back_img = pygame.image.load("graphics/game_background_4.png")
        back_img = pygame.transform.scale(back_img, (screen_w, screen_h))
        game_instance = Game()
        screen = pygame.display.set_mode((screen_w, screen_h))
        clock = pygame.time.Clock()
        game = Stage(screen, screen_w, screen_h,game_instance, stage_name)  # instancia de la clase
        stopwatch = Stopwatch()
        stopwatch.stop()
        #menu escape
        # Game variables
        game_paused = False#con respecto al menu
        menu_state = "main"       
        #define backgraund menu
        screen_menu = pygame.display.set_mode((screen_w, screen_h))
        
        
        
        
        
        # Load button images
        resume_img = pygame.image.load("assets/images_menu/button_resume.png ").convert_alpha()
        options_img = pygame.image.load("assets/images_menu/button_options.png").convert_alpha()
        quit_img = pygame.image.load("assets/images_menu/button_quit.png").convert_alpha()
        video_img = pygame.image.load('assets/images_menu/button_video.png').convert_alpha()
        audio_img = pygame.image.load('assets/images_menu/button_audio.png').convert_alpha()
        keys_img = pygame.image.load('assets/images_menu/button_keys.png').convert_alpha()
        back_img_menu = pygame.image.load('assets/images_menu/button_back.png').convert_alpha()
    
        # Create button instances
        resume_button = button.Button(screen_h/2+150, 150, resume_img, 1,)
        options_button = button.Button(screen_h/2+150, 250, options_img, 1)
        quit_button = button.Button(screen_h/2+150, 350, quit_img, 1)
        video_button = button.Button(screen_h/2+150, 75, video_img, 1)
        audio_button = button.Button(screen_h/2+150, 200, audio_img, 1)
        keys_button = button.Button(screen_h/2+150, 325, keys_img, 1)
        back_button = button.Button(screen_h/+150, 450, back_img_menu, 1)

        
        running = True
        while running:
            clock.tick(FPS)
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    running=False
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        game_paused = not game_paused
                # elif evento.type  == 
            
            
            
            
            if game_paused:
                stopwatch.start()
                #print(stopwatch)
                # Verificar el estado del menú
                screen_menu.fill((52, 78, 91))
                if menu_state == "main":
                    # Dibujar botones de menú
                    if resume_button.draw(screen):
                        game_paused = False
                        pygame.time.wait
                        running=True
                        
                    if options_button.draw(screen):
                        menu_state = "options"
                    if quit_button.draw(screen):
                        pygame.quit()
                        sys.exit()
                elif menu_state == "options":
                    # Dibujar botones de opciones
                    # Agrega aquí el código para los botones de opciones
                    if video_button.draw(screen):
                        print("Video Settings")
                    if audio_button.draw(screen):
                        print("Audio Settings")
                    if keys_button.draw(screen):
                        print("Change Key Bindings")
                    if back_button.draw(screen):
                        menu_state = "main"
                #print(stopwatch.duration) 
                
                
            else:
                stopwatch.stop()
                if stopwatch.duration>=1:
                    time_paused += stopwatch.duration
                stopwatch.restart()
                screen.blit(back_img, back_img.get_rect())  # relleno fondo
                delta_ms = clock.tick(60)
                game.run(delta_ms,time_paused)

            pygame.display.flip()
