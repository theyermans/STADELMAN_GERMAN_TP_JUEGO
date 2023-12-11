import time
import pygame
import sys
import button
from stopwatch import Stopwatch
from stage import Stage
from constantes import (FPS, screen_h, screen_w)
from GUI.GUI_form_prueba import FormPrueba
from estadisticas import Estadisticas


#from GUI.UI.GUI_textbox import TextBox


class Game:

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((screen_w, screen_h))
        self.clock = pygame.time.Clock()
        self.game_paused = False

        
        self.stage = None
    def start(self):
        stage_seleccionado = ""
        screen = pygame.display.set_mode((screen_w, screen_h))
        clock = pygame.time.Clock()
        back_img = pygame.image.load("assets/recopilado/sky.png")
        back_img = pygame.transform.scale(back_img, (screen_w, screen_h))
        form_prueba = FormPrueba(screen,200,100,900,350,(0, 0, 0),"red",5,True)
        eventos = pygame.event.get()
        nombre_stage = ""
        estadisticas = Estadisticas()
        # # Suponiendo que tu clase Game tiene un método start y se llama game_instance
        # game_instance = Game()  # Crea una instancia de tu clase Game
        # stage_instance = Stage(screen, limit_w, limit_h, game_instance, stage_name="stage_1")
        # Crear una instancia de la clase Game
        game_instance = Game()
        # Crear una instancia de la clase Stage con la instancia de Game como argumento
        stage_instance = Stage(screen, screen_w, screen_h, game_instance, stage_name="stage_1")

        while stage_seleccionado == "":
            clock.tick(FPS)
            eventos = pygame.event.get()
            for event in eventos:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            screen.blit(back_img, back_img.get_rect())
            # Obtener el texto ingresado en el cuadro de texto
            texto_ingresado = form_prueba.txt_nombre.get_text()

            stage_seleccionado = form_prueba.update(eventos)
            pygame.display.flip()
            
           
            #print(estadisticas_actualizadas)
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
        resume_button = button.Button(500, 150, resume_img, 1,)
        options_button = button.Button(495, 250, options_img, 1)
        quit_button = button.Button(520, 350, quit_img, 1)
        video_button = button.Button(226, 75, video_img, 1)
        audio_button = button.Button(225, 200, audio_img, 1)
        keys_button = button.Button(246, 325, keys_img, 1)
        back_button = button.Button(332, 450, back_img_menu, 1)

        
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
                print(stopwatch)
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
                print(stopwatch.duration) 
                
                
            else:
                stopwatch.stop()
                if stopwatch.duration>=1:
                    time_paused += stopwatch.duration
                stopwatch.restart()
                screen.blit(back_img, back_img.get_rect())  # relleno fondo
                delta_ms = clock.tick(60)
                game.run(delta_ms,time_paused)

            pygame.display.flip()
