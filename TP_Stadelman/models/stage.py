import pygame
import pygame.font

import time 
import random


from items import Items
from auxiliares import TablaPuntajes
from estadisticas import Estadisticas 
from platforms import Platform, Tramp
from player import Player
from constantes import FONT_GLOBAL, GRAVITY,CONFIG_FILE_PATH, ConfigManager, Music_Controller
from gergoomba import Gergoomba,Boss






# The Stage class represents a stage in a game and contains information about the player, enemies, and
# platforms in that stage.
class Stage:
    def __init__(self, screen: pygame.surface.Surface, limit_w, limit_h,game_instance, stage_name="stage_1"):
        
        # Jugador
        self.__configs = ConfigManager.load_configs(self,CONFIG_FILE_PATH)
        # print(self.__configs)
        self.configs_stage = self.__configs.get(stage_name,"stage_1")
        
        self.stage_name = stage_name
        self.game_instance:object = game_instance
        self.gravity_speed = self.configs_stage.get("gravity_speed", 300)
        self.damage_blade = self.configs_stage.get("damage_bulet_p", 25)
        self.platforms_data = self.configs_stage.get("platforms_data", [])
        self.game_duration = self.configs_stage.get("game_duration", 60)  # Set the game duration in seconds
        # Game timer variables
        self.game_start_time = time.time()   
        #pantalla
        self.__player_win = False
        self.__limit_w = limit_w
        self.__limit_h = limit_h
        self.main_screen = screen
        self.my_surface_rect = self.main_screen.get_rect()
        self.constraint=pygame.Vector2(limit_w, limit_h)
        self.player = Player(pygame.Vector2(limit_w / 2, limit_h /2), self.constraint, self.gravity_speed , GRAVITY, self.__configs)
        
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)
        #items        
        self.items: pygame.sprite.Group() = pygame.sprite.Group()
        self.items.add(Items(50, 100, "coin"))
        #self.items.add(Items(350,450,"heart"))
        #plataformas
        self.plataformas = []
        # Crear una instancia de la plataforma
        for data in self.platforms_data:
            rect = pygame.Rect(data["left"], data["top"], data["width"], data["height"])
            self.plataformas.append(Platform(rect, data["image_path"]))
        tramp_rect = pygame.Rect(250, 600, 50, 32)  # Ajusta la posición y dimensiones según tu escenario
        #"left": 0, "top": 650, "width": 1280, "height": 100
        time_per_state = 1000  # Ajusta el tiempo entre estados según sea necesario
        self.tramp_platform = Tramp(tramp_rect, time_per_state)
        
        self.pos_enemy_bat = {}
        pygame.font.init()
        self.timer_font = pygame.font.SysFont(FONT_GLOBAL, 48)  # Choose a font and size for the timer        
        #estadisticas        
        self.score:int = 0
        self.tabla = TablaPuntajes(self.main_screen, self.score)
        self.contador_bat_kill = 0
        self.suma_bat_score = self.configs_stage.get("suma_bat_score",1)
        self.tabla.muestra_score(self.score)
        estadisticas = Estadisticas()
        self.estadisticas = Estadisticas()
        self.probando = estadisticas.agregar_puntuacion(self.score)
        #enemi y da;o bullet
        self.enemies : pygame.sprite.Group() = pygame.sprite.Group()
               
        self.max_enemies = self.configs_stage.get("max_enemies",4)  # Set the maximum number of enemies
        self.spawn_timer = self.configs_stage.get("spawn_timer",100)
        self.spawn_timer_min = self.configs_stage.get(("spawn_timer_min"),0)
        self.spawn_timer_max = self.configs_stage.get(("spawn_timer_max"),2500)
        self.width_of_enemy = 64  # ajusta esto al ancho real de tu enemigo pixels
        self.height_of_enemy = 64 
        
        self.bullet_bat_group: pygame.sprite.Group()  = pygame.sprite.Group()
        
        for enemy_data in self.pos_enemy_bat.get("enemy_pos", {}).items():
            position = pygame.Vector2([enemy_data[1]["pos1_x"], enemy_data[1]["pos1_y"]])
            self.enemies.add(Gergoomba(position, self.constraint, self.stage_name, self, pygame.Vector2(random.choice((1,-1)),0)))
        self.spike_cooldown = 100
        #control de balla fuera de pantalla
        for bullet in self.player.bullet_group:
            if bullet.rect.right <= 0:
                self.player.bullet_group.remove(bullet)
        #boss
        self.boss = pygame.sprite.GroupSingle() 
        self.boss.add(Boss(pygame.Vector2(300, 100), self.constraint, self.stage_name,self, pygame.Vector2(random.choice((1,-1)),0)))  # Adjust the position as needed
        
    def generar_items_random(self, cantidad_items):
        items_faltantes = cantidad_items - len(self.items)
        if items_faltantes > 0:
            for _ in range(items_faltantes):
                pos_random_x = random.randint(10, 1150)
                pos_random_y = random.randint(400, 500)

                # Verificar que la posición generada no colisiona con ninguna plataforma
                colision_plataformas = any(platform.rect.collidepoint(pos_random_x, pos_random_y) for platform in self.plataformas)
                
                # Si hay colisión, intentar generar nuevas posiciones hasta encontrar una válida
                while colision_plataformas:
                    pos_random_x = random.randint(350, 550)
                    pos_random_y = random.randint(400, 550)
                    colision_plataformas = any(platform.rect.collidepoint(pos_random_x, pos_random_y) for platform in self.plataformas)

                # Agregar el nuevo elemento a la lista
                self.items.add(Items(pos_random_x, pos_random_y, "coin"))
    def generar_item_hearth(self,delta_ms,cantidad_items):
        items_faltantes = cantidad_items - len(self.items)
        
        if items_faltantes > 0:
            for _ in range(items_faltantes):
                pos_random_x = random.randint(10, 1150)
                pos_random_y = random.randint(100, 500)

                # Verificar que la posición generada no colisiona con ninguna plataforma
                colision_plataformas = any(platform.rect.collidepoint(pos_random_x, pos_random_y) for platform in self.plataformas)

                # Si hay colisión, intentar generar nuevas posiciones hasta encontrar una válida
                while colision_plataformas:
                    pos_random_x = random.randint(10, 1150)
                    pos_random_y = random.randint(100, 500)
                    colision_plataformas = any(platform.rect.collidepoint(pos_random_x, pos_random_y) for platform in self.plataformas)

            # Agregar el nuevo elemento a la lista
                self.items.add(Items(pos_random_x, pos_random_y, "heart"))
        #self.items.add(Items(50,580,"heart"))
    def spawn_left_enemy_bat(self,delta_ms):
        if len(self.enemies) < self.max_enemies:
            valid_spawn = False
            while not valid_spawn:
                pos_y = random.randint(100,400)
                direction = random.choice([1, -1])
                if direction >= 0:
                    pos_x = -100
                else:
                    pos_x = 1200
                new_enemy_rect = pygame.Rect(pos_x, pos_y, self.width_of_enemy, self.height_of_enemy)
                # Verificar que el nuevo enemigo no colisione con ninguna plataforma
                colision_plataformas = any(platform.rect.colliderect(new_enemy_rect) for platform in self.plataformas)
                # Si hay colisión, intentar generar nuevas posiciones hasta encontrar una válida
                valid_spawn = not colision_plataformas
            new_enemy = Gergoomba(pygame.Vector2(pos_x, pos_y), self.constraint,self.stage_name, self, pygame.Vector2(direction, 0))
            #new_enemy = Gergoomba(pygame.Vector2(pos_x, pos_y), pygame.Vector2(self.__limit_w, self.__limit_h),self.stage_name, pygame.Vector2(direction, 0))
            new_enemy.shoot_timer = random.randint(1000, 3000)  # Configura el temporizador aqu
            self.enemies.add(new_enemy)
    def play_background_music(self):
        # Asegúrate de tener una instancia de Music_Controller creada
        Music_Controller.play_background_music(self.volumen)
    def status_hp_player(self,screen,x,y,hp)  :
        heart_image_path = "assets/Player/hi_overlay_variant_hearts_x1_1_png_1354840444.png"
        heart_image = pygame.transform.scale2x(pygame.image.load(heart_image_path))
        heart_separation_x = 64  # Ancho de cada corazón
        hearts_to_draw = hp 
        for i in range(hearts_to_draw):
            screen.blit(heart_image, (x + i * heart_separation_x, y))
        if hp < 0:
            hp = 0
    def update_bullets(self, delta_ms):
            for bullet in self.bullet_bat_group:
                bullet.update(delta_ms)
                bullet.draw(self.main_screen, delta_ms)
                 
                # Check if the bullet reaches the upper limit (constraint)
                if bullet.rect.bottom <= 0 or bullet.rect.right <= 0 or bullet.rect.left >= self.__limit_w:
                    self.bullet_bat_group.remove(bullet)
    def handle_bullet_enemy_collisions(self):
        """controla colisiones de enemigos vs balas player"""
        colission_bat_bullet_player = pygame.sprite.groupcollide(self.enemies, self.player.bullet_group, False, True)
        
        for enemy, bullets_hit in colission_bat_bullet_player.items():
            for bullet in bullets_hit:
                # Deduct life points from the specific enemy hit by the bullet
                enemy.hp_enemy -= self.damage_blade
                Music_Controller.play_collision_sound()
                if enemy.hp_enemy <= 0:
                    enemy.kill()#este es un magico de sprite
                    self.contador_bat_kill += 1
                    self.score += self.suma_bat_score
                    
                    
    def handle_bullet_player_boss_collisions(self):
        """Controla colisiones entre las balas del jugador y el boss"""
        colision_bullets_player_boss = pygame.sprite.groupcollide(self.player.bullet_group, self.boss, True, False)
        
        for bullet, bosses_hit in colision_bullets_player_boss.items():
            for boss in bosses_hit:
                # Deduct life points from the boss hit by the player's bullet
                boss.hp_enemy -= self.damage_blade
                if boss.hp_enemy <= 0:
                    boss.kill()  
                    self.score += self.suma_bat_score*100
                    self.game_instance.start()
                    

        
    def run(self, delta_ms,time_paused):
        """ Actualizar todos los grupos de sprites
         Dibujar todos los grupos de sprites
         Actualizar y Dibujar Jugador
         es una mezcla de update/draw/run
         """
        
        p:Platform
        for p in self.plataformas:
            p.draw(self.main_screen)
        # Colisiones entre el jugador y la plataforma
        if self.stage_name == "stage_2":
            colision_player_platform = pygame.sprite.spritecollide(self.player, [self.tramp_platform], False)
            if colision_player_platform:            
                self.player.receive_damage()   
            # Actualizar y dibujar la plataforma
            
            self.tramp_platform.update(self.main_screen,delta_ms)
            self.tramp_platform.draw(self.main_screen,delta_ms)    
        #player
        self.player.update(delta_ms, self.plataformas)
        colisiones_player_bat_bullet = pygame.sprite.groupcollide(self.player_group, self.bullet_bat_group, False, True)
        if self.stage_name == "stage_2":
           
            if colisiones_player_bat_bullet:
                for jojo, b_bat_hit in colisiones_player_bat_bullet.items():
                    for b_bat in b_bat_hit:
                        self.player.receive_damage()
        
                    
                    
        pygame.draw.rect(self.main_screen, (255, 0, 0), self.player.rect, 2)            
        self.player.draw(self.main_screen, delta_ms)
        #item heart and boss
        if self.stage_name == "stage_3":
            boss: Boss
            for boss in self.boss:
                boss.update(delta_ms, self.player.pos)
                boss.draw(self.main_screen, delta_ms)
            self.handle_bullet_player_boss_collisions()
            #items
            
        
        item:Items        
        for item in self.items:
            item.update_frame(delta_ms)
            item.draw(self.main_screen, delta_ms)
        self.generar_items_random(10)#mandar al json
        self.generar_item_hearth(delta_ms,1)#json
        colisiones_player_items = pygame.sprite.groupcollide(self.player_group, self.items, False, True)
        if colisiones_player_items:
            for player, items_hit in colisiones_player_items.items():
                for item in items_hit:
                    # Acciones a realizar cuando hay una colisión
                    if item.item_type == "coin":
                        # Aumenta la puntuación o realiza otras acciones
                        self.score += (5 )
                    if item.item_type == "heart":
                        self.player.player_hp += 1
        
        e:Gergoomba
        #spawn update y draw
        self.spawn_timer -= delta_ms
        
        
        #draw and update enemy
        for e in self.enemies:
            e.update(delta_ms, self.player)
            e.draw(self.main_screen, delta_ms)
        self.update_bullets(delta_ms)
        self.handle_bullet_enemy_collisions() 
            
        if self.stage_name != "stage_3":    
            if self.spawn_timer <= 0 and len(self.enemies) < self.max_enemies:
                        self.spawn_left_enemy_bat(delta_ms)
                        self.spawn_timer = random.randint(self.spawn_timer_min, self.spawn_timer_max)
        
                        
        # Calculate remaining game time
        elapsed_time = time.time() - self.game_start_time
       
        remaining_time = max(0, self.game_duration - elapsed_time + time_paused)
        #finish and return menu
        if remaining_time <= 0:
            print("Tiempo agotado, regresando a la pantalla principal")
            self.estadisticas.agregar_puntuacion(self.score)
            self.probando = self.estadisticas.obtener_puntuaciones()
            #print(self.probando)
            self.game_instance.start()
        if self.player.player_hp <= 0:
            print("Vida agotada, regresando a la pantalla principal")
            self.game_instance.start()
            
            
        # Render and display the remaining time on the screen
        timer_text = f"Time: {int(remaining_time)}s"
        timer_surface = self.timer_font.render(timer_text, True, (255, 255, 255))
        
        self.main_screen.blit(timer_surface, ((self.my_surface_rect.centerx-20), (self.my_surface_rect.top+10)))  
        self.status_hp_player(self.main_screen, self.my_surface_rect.x-100, self.my_surface_rect.top-100, self.player.player_hp)
        self.main_screen.get_rect()
        self.tabla.muestra_score(self.score)
        
        
        
        
