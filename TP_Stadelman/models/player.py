
import pygame as pg
from auxiliares import SurfaceManager
from constantes import CONFIG_FILE_PATH, ConfigManager
from platforms import Platform
from bullet import Bullet





class Player(pg.sprite.Sprite):
    def __init__(self, pos: pg.Vector2, constraint : pg.Vector2, speed , gravity_speed, stage_dict_configs: dict):
        super().__init__()
        #json
                
       
        self.__configs = ConfigManager.load_configs(self,CONFIG_FILE_PATH)
        # print(self.__configs)
        self.configs_stage = self.__configs.get("stage_1",{})
        self.images = {}
        self.__player_configs:dict = self.configs_stage.get("player",{})
        self.images:dict = self.__player_configs.get("player_img", {})
        #self.key = self.images.get("idleRight",{})
        #self.rect = pg.Rect(pos.x, self.constrains.y - pos.y, 64, 64)# esos 64 son el anchoi alto jugador paraa que no se pase del constrain desde el piunto donde dibuja a player
        
        # Atributos de movimiento
        self.pos: pg.Vector2 = pos
        self.speed = speed #lo que se mueve en x por parametro a pasar a json
        self.constrains: pg.Vector2 = constraint #restriccion en vector es una tupla (x,y)
        self.movement = pg.Vector2(0, 0)
        self.gravity_speed = gravity_speed
        self.on_ground: bool = False
        #control de tiempo
        self.frame_duration_ms = 1000 / 30
        self.frame_elapsed_time = self.frame_duration_ms    
        self.current_frame = 0
        #triple hitbox para detectar mejor las colisiomnes
        self.botom_hitbox:pg.Rect = pg.Rect(self.pos.x, self.pos.y + 64 , 30, 1) #mas 64 porque es el ancho de pileles del personaje en la parte derecha del mismo
        self.left_hitbox:pg.Rect = pg.Rect(self.pos.x - 1 , self.pos.y , 1, 40) #-1 porq es la parte izquierda
        self.right_hitbox:pg.Rect = pg.Rect(self.pos.x + 64 , self.pos.y, 1, 40) #+64 porq es la parte de abajo del personaje por su cantidad de pixees
        
        # Mostrar sprite del jugador
        
        self.images  # Use the first frame of the 'idleRight' animation as the default image
        path:str
        for key,path in self.images.items():

            if path:
                #self.images[key] = SurfaceManager.get_surface_from_spritesheet(path, 11, 1)  # Adjust the parameters as needed                
                if key == "idleRight":
                    self.images[key] = SurfaceManager.get_surface_from_spritesheet(path, 11, 1)
                if key == "idleLeft":
                    self.images[key] = SurfaceManager.get_surface_from_spritesheet(path, 11, 1, 1, True)
                elif key == "runningRight":
                    self.images[key] = SurfaceManager.get_surface_from_spritesheet(path,12, 1,)
                elif key == "runningLeft":
                    self.images[key] = SurfaceManager.get_surface_from_spritesheet(path, 12, 1, 1, True)
                elif key == "playerDamagedIfRight":
                    self.images[key] = SurfaceManager.get_surface_from_spritesheet(path, 7,1,1)
                elif key == "playerDamagedIfLeft":
                    self.images[key] = SurfaceManager.get_surface_from_spritesheet(path, 7, 1, 1, True)
                elif key == "up":
                    self.images[key] = SurfaceManager.get_surface_from_spritesheet1x(path, 8, 1, 1, True)
        self.state = "playerDamagedIfRight"


        # Atributos para disparar y recargar
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 200#json
        self.bullet_group : pg.sprite.Group()  = pg.sprite.Group()
        self.puntaje = 0
        #recibiendo danmio
        self.damage_cooldown = 2500 
        self.damage_cooldown_elapsed_time = 0
        self.state_damage = False
        
        #registro de datos
        self.player_hp = 3#json
        
        self.rect = pg.Rect(self.pos.x, self.constrains.y - self.pos.y - self.images[self.state][self.current_frame].get_height(), self.images[self.state][self.current_frame].get_width(), self.images[self.state][self.current_frame].get_height())
        
    
                
    def seleccionar_avatar(self):
        avatar_key = ("idleRight")
        return avatar_key
    def surface_heart(self)    :
        heart_image_path = ".assets/Player/Coração-Cristal-Pulso.png"
        hearth_image_list = SurfaceManager.get_surface_from_spritesheet(heart_image_path, 2, 2)
        return hearth_image_list
    
    
    def receive_damage(self,enemy_damage=1):
       if not self.state_damage:
            self.player_hp -= enemy_damage  # Adjust this based on your game logic
            self.state_damage = True
            self.damage_cooldown_elapsed_time = 0  # Reset the damage cooldown timer
            # Cambiar el estado a "Damage"
            if self.player_hp > 0:
                if self.movement.x > 0:
                    self.state = "playerDamagedIfRight"
                    self.damage_cooldown_elapsed_time += self.damage_cooldown 
                else:
                    self.state = "playerDamagedIfLeft"
                    self.damage_cooldown_elapsed_time += self.damage_cooldown 
                    
            if self.player_hp <= 0:
                self.game_over()

    def game_over(self):
        print("personaje muerto de vuelta al GUI")
        return True
         
        
            
    def move(self, delta_ms):
        self.pos += self.movement * (delta_ms / 1000)   

        if(not self.on_ground):
            self.movement.y += self.gravity_speed
            
        else:
            self.movement.y = 0   

    def manejar_eventos_teclado(self):  # Eventos del jugador
        """notas para interfaz y generalizacion
        esto deberia de estar en stage
        por eemplo en stage vamos a tgener updaate
        """
        self.movement = pg.Vector2(0,self.movement.y)       
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:  # movimiento sobre eje x
            self.movement.x -= self.speed            
        elif keys[pg.K_d]:
            self.movement.x += self.speed       
        if keys[pg.K_SPACE] and self.on_ground:
            self.movement.y -= 700
            self.on_ground = False 
        if keys[pg.K_j] and self.laser_time <= 0 :
            self.shoot()
            
    def shoot(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]: 
            self.bullet_group.add(Bullet(self.pos.copy(), pg.Vector2(0, -1)))  # Cambiado a -1 para disparar hacia arriba
            self.laser_time = self.laser_cooldown
                       
        elif "Right" in self.state:
            self.bullet_group.add(Bullet(self.pos.copy(), pg.Vector2(1, 0)))
            self.laser_time = self.laser_cooldown 
                   
        else:
            self.bullet_group.add(Bullet(self.pos.copy(), pg.Vector2(-1, 0)))
            self.laser_time = self.laser_cooldown
            
    def checkearHitboxes(self, listaPlataformas):
        """respecto a laa clase plataforma"""
        p:Platform
        self.on_ground = False
        for p  in listaPlataformas:
            if p.rect.colliderect(self.left_hitbox) and self.movement.x < 0 :
                self.movement.x = 0               
                
            if p.rect.colliderect(self.right_hitbox) and self.movement.x > 0:
                self.movement.x = 0 
                
            if p.rect.colliderect(self.botom_hitbox) and self.movement.y > 0:
                self.pos.y -= self.botom_hitbox.top - p.rect.top
                self.movement.y = 0
                self.on_ground = True
                
                
                    
    def check_state(self, delta_ms):
        if(self.movement.x != 0):
            if(self.movement.x > 0):
                self.state = "runningRight"
                if self.state_damage:
                    self.state = "playerDamagedIfRight"
            else:
                self.state = "runningLeft"
                if self.state_damage:
                    self.state = "playerDamagedIfLeft"
        elif((self.state.__contains__("running") or self.state.__contains__("Damage")) and not self.state_damage ):#aca empece a sufirir 
            if(self.state.__contains__("Right")):
                self.state = "idleRight"
            else:
                self.state = "idleLeft"
        # Update the cooldown timer
        if self.damage_cooldown_elapsed_time > 0 and self.state_damage:
            self.damage_cooldown_elapsed_time -= delta_ms
        else:
            self.damage_cooldown_elapsed_time = self.damage_cooldown
            self.state_damage = False
    def update_frame(self, delta_ms):
       
        self.frame_elapsed_time -= delta_ms
        if(self.frame_elapsed_time <= 0):
            self.frame_elapsed_time = self.frame_duration_ms
            self.current_frame += 1
            if(len(self.images[self.state]) <= self.current_frame):
                self.current_frame = 0
        #La sujeción se refiere a limitar un valor dentro de un rango. Cuando un valor excede un rango, se cambia al valor más grande posible, y si el valor supera un rango, se cambia al valor más pequeño posible.
        self.pos.x = pg.math.clamp(self.pos.x, 0, self.constrains.x - 64)
        self.pos.y = pg.math.clamp(self.pos.y, 0, self.constrains.y)
        self.rect.topleft = self.pos
        
        #Aca ajustamos las hitbox para que siempre sigan al personaje en la posicion correcta
        self.botom_hitbox.topleft = (self.pos.x + 17, self.pos.y + 64)
        self.left_hitbox.topleft = (self.pos.x - 1, self.pos.y + 12)
        self.right_hitbox.topleft = (self.pos.x + 64, self.pos.y + 12)
        
    def update(self, delta_ms:float , listaPlataformas):
        self.manejar_eventos_teclado()        
        self.checkearHitboxes(listaPlataformas)
        self.move(delta_ms)
        #Aca checkeamos que animacion corresponde
        self.check_state(delta_ms)
        #Aca avanzamos la animacion
        self.update_frame(delta_ms)        
        if(self.pos.y == self.constrains.y):
            self.on_ground = True
        #aca las balas se updatean
        for v in self.bullet_group:
            v.update(delta_ms)
        self.laser_time -= delta_ms
        for bullet in self.bullet_group:
            bullet.update(delta_ms)
            # Check if the bullet reaches the upper limit (constraint)
            if bullet.rect.bottom <= 0 or bullet.rect.right <= 0 or bullet.rect.left >= self.constrains.x:
                self.bullet_group.remove(bullet)
        
       
        
            
    def draw(self, screen,delta_ms: float):
        if self.state not in self.images:
            self.state = "idleRight"
            
        if(self.current_frame >= len(self.images[self.state])):
            self.current_frame = 0
        screen.blit(self.images[self.state][self.current_frame], self.rect.topleft)
        
        pg.draw.rect(screen, (255, 0, 0), self.botom_hitbox, 2)
        pg.draw.rect(screen, (255, 0, 0), self.left_hitbox, 2)
        pg.draw.rect(screen, (255, 0, 0), self.right_hitbox, 2)
        for v in self.bullet_group.sprites():
            v.draw(screen,delta_ms)
            
    
    
        