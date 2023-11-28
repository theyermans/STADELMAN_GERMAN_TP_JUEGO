
import pygame as pg
from auxiliares import SurfaceManager
from platforms import Platform
from bullet import Bullet




class Player(pg.sprite.Sprite):
    def __init__(self, pos: pg.Vector2, constraint : pg.Vector2, speed , gravity_speed):
        super().__init__()
        
        # Atributos de movimiento
        self.pos: pg.Vector2 = pos
        self.speed = speed #lo que se mueve en x por parametro a pasar a json
        self.constrains: pg.Vector2 = constraint #restriccion en vector es una tupla (x,y)
        self.movement = pg.Vector2(0, 0)
        self.gravity_speed = gravity_speed
        self.on_ground: bool = False
        #triple hitbox para detectar mejor las colisiomnes
        self.botom_hitbox:pg.Rect = pg.Rect(self.pos.x, self.pos.y + 64 , 30, 1) #mas 64 porque es el ancho de pileles del personaje en la parte derecha del mismo
        self.left_hitbox:pg.Rect = pg.Rect(self.pos.x - 1 , self.pos.y , 1, 40) #-1 porq es la parte izquierda
        self.right_hitbox:pg.Rect = pg.Rect(self.pos.x + 64 , self.pos.y, 1, 40) #+64 porq es la parte de abajo del personaje por su cantidad de pixees
        
        # Mostrar sprite del jugador
        self.state = "idleRight"        
        self.images = {}
        self.images["idleRight"] = SurfaceManager.get_surface_from_spritesheet("./assets/Player/Idle (32x32).png", 11, 1)
        self.images["idleLeft"] = SurfaceManager.get_surface_from_spritesheet("./assets/Player/Idle (32x32).png", 11, 1, 1, True)
        
        self.images["runningRight"] = SurfaceManager.get_surface_from_spritesheet("./assets/Player/Run (32x32).png", 12, 1)
        self.images["runningLeft"] = SurfaceManager.get_surface_from_spritesheet("./assets/Player/Run (32x32).png", 12, 1, 1, True)
        
        self.images["playerDamagedIfRight"] = SurfaceManager.get_surface_from_spritesheet("assets/Player/Hit (32x32).png",7,1,1)
        self.images["playerDamagedIfLeft"] = SurfaceManager.get_surface_from_spritesheet("assets/Player/Hit (32x32).png",7,1,1, True)
        
        self.rect = pg.Rect(pos.x, self.constrains.y - pos.y, 64, 64)
        
        #control de tiempo
        self.frame_duration_ms = 1000 / 30
        self.frame_elapsed_time = self.frame_duration_ms    
        self.current_frame = 0


        # Atributos para disparar y recargar
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600
        self.bullet_group : pg.sprite.Group()  = pg.sprite.Group()
        self.puntaje = 0
        #jugando con los states
        self.damage_cooldown = 6  # Adjust the cooldown duration in milliseconds
        self.damage_cooldown_elapsed_time = 0
        self.state_damage = False
        
        #registro de datos
        self.player_hp =100
        
        
    def current_hp(self):
        
        print(self.player_hp)
        
    def receive_damage(self):
       
        self.player_hp -= 1  # Adjust this based on your game logic
        print("Damaage")
        self.state_damage = True

        if self.player_hp <= 0:
            # Implement game over logic
            self.game_over()

    def game_over(self):
        # Implement the logic for what happens when the game is over
        print("Game Over")  # Adjust this based on your game logic
        
        
    def shoot(self):
        #comparativa = ("runningRight","idleRight")
        if self.state.__contains__("Right") :
            self.bullet_group.add(Bullet(self.pos.copy(),pg.Vector2(1,0)))
            self.laser_time = self.laser_cooldown
        else:
            self.bullet_group.add(Bullet(self.pos.copy(),pg.Vector2(-1,0)))
            self.laser_time = self.laser_cooldown
    def move(self, delta_ms):
        self.pos += self.movement * (delta_ms / 1000)   

        if(not self.on_ground):
            self.movement.y += self.gravity_speed
            
        else:
            self.movement.y = 0   

    def manejar_eventos_teclado(self):  # Eventos del jugador
       
        self.movement = pg.Vector2(0,self.movement.y)
        
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:  # movimiento sobre eje x
            self.movement.x -= self.speed
            
        elif keys[pg.K_d]:
            self.movement.x += self.speed

        if keys[pg.K_SPACE] and self.on_ground:
            self.movement.y -= 700
            self.on_ground = False
        if keys[pg.K_j] and self.laser_time < 0 :
            self.shoot()
            
    def checkearHitboxes(self, listaPlataformas):
        p:Platform
        self.on_ground = False
        for p  in listaPlataformas:
            if p.rect.colliderect(self.left_hitbox) and self.movement.x < 0 :
                self.movement.x = 0               
            
            if p.rect.colliderect(self.right_hitbox) and self.movement.x > 0:
                self.movement.x = 0 
            
            if p.rect.colliderect(self.botom_hitbox) and self.movement.y > 0:
                self.movement.y = 0
                self.on_ground = True
                
                
                    
    def check_state(self, delta_ms):
        if(self.movement.x != 0):
            if(self.movement.x > 0):
                self.state = "runningRight"
                
                if self.state_damage:
                    self.state = "playerDamagedIfRight"
                    print("danio miraando hacia la derecha")
                    
            else:
                self.state = "runningLeft"
                if self.state_damage:
                    self.state = "playerDamagedIfLeft"
                    print("danio miraando hacia la izquierda")
            # Start the cooldown timer
            
                
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
        print(self.damage_cooldown_elapsed_time)
            
        
            

                
    # def check_state(self):
    #     if self.player_hp <= 0:
    #         # Player is damaged, set the damaged state
    #         if self.movement.x > 0:
    #             self.state = "playerDamagedIfRight"
    #         else:
    #             self.state = "playerDamagedIfLeft"
    #     elif self.movement.x != 0:
    #         # Player is moving
    #         if self.movement.x > 0:
    #             self.state = "runningRight"
    #         else:
    #             self.state = "runningLeft"
    #     else:
    #         # Player is idle
    #         if self.state.__contains__("running"):
    #             if self.state.__contains__("Right"):
    #                 self.state = "idleRight"
    #             else:
    #                 self.state = "idleLeft"
        
        
    def update_frame(self, delta_ms):
        self.frame_elapsed_time -= delta_ms
        if(self.frame_elapsed_time <= 0):
            self.frame_elapsed_time = self.frame_duration_ms
            self.current_frame += 1
            if(len(self.images[self.state]) <= self.current_frame):
                self.current_frame = 0
                
        self.pos.x = pg.math.clamp(self.pos.x, 0, self.constrains.x - 64)
        self.pos.y = pg.math.clamp(self.pos.y, 0, self.constrains.y)
        self.rect.bottomleft = self.pos
        
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
        for bullet in self.bullet_group.copy():
            bullet.update(delta_ms)

            # Check if the bullet reaches the upper limit (constraint)
            if bullet.rect.bottom <= 0 or bullet.rect.right <= 0 or bullet.rect.left >= self.constrains.x:
                self.bullet_group.remove(bullet)
                print("Bala eliminada ********************")
        
            
    def draw(self, screen,delta_ms: float):
        if(self.current_frame >= len(self.images[self.state])):
            self.current_frame = 0
        screen.blit(self.images[self.state][self.current_frame], self.rect.bottomleft)
        for v in self.bullet_group.sprites():
            v.draw(screen,delta_ms)
    
        