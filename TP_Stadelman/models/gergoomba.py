import random
import pygame as pg
from enemy import Enemy
from auxiliares import SurfaceManager
from bullet import Bullet_Bat
from constantes import CONFIG_FILE_PATH, ConfigManager


class Gergoomba(Enemy):
    def __init__(self, pos, constraint,stage_name, stage, facingDirection=pg.Vector2(1,0)):
        Enemy.__init__(self, pos, 250, constraint,facingDirection)
        
        self.datos_json = ConfigManager.load_configs(self,CONFIG_FILE_PATH)
        #print(self.datos_json )
        #print(stage_name)
        self.datos_stage = self.datos_json.get(stage_name,"stage_1")
        #print(self.datos_stage)
        self.datos_enemy = self.datos_stage.get("enemy","")
        self.stage  = stage_name
        self.load_sprites("assets/Enemy/bat/Flying (46x30).png")
        self.state =  "flyingR"
        self.gravity_speed = 0
        #self.stage = stage
        self.rect = pg.Rect(pos.x, pos.y, self.images["flyingR"][0].get_width (), self.images["flyingR"][0].get_height () )
        self.hp_enemy = 50
        self.shoot_timer = 500
        self.shoot_cooldown = (self.datos_enemy.get("shoot_cooldown",1000))  # Intervalo de tiempo entre disparos en milisegundos
        self.stage=stage
    def shoot(self):
        #self.bullet_bat_group.add(Bullet_Bat(self.pos, pg.Vector2(0, 1)))
        self.stage.bullet_bat_group.add(Bullet_Bat(self.pos.copy(), pg.Vector2(0, 1)))
        # if self.stage is not None and hasattr(self.stage, 'bullet_bat_group'):
        #     self.stage.bullet_bat_group.add(Bullet_Bat(self.pos, pg.Vector2(0, 1)))
    
    def load_sprites(self, path):
        self.images["flyingR"] = SurfaceManager.get_surface_from_spritesheet(path, 7, 1, 1, True)
        self.images["flyingL"] = SurfaceManager.get_surface_from_spritesheet(path, 7, 1)
        
    def update(self, delta_ms,player):
        super().update(delta_ms)
        self.shoot_timer -= delta_ms
        if self.shoot_timer <=0:
            self.shoot()
            self.shoot_timer=self.shoot_cooldown
             
        if self.facingDirection.x < 0:
            self.state = "flyingL"
        else:
            self.state = "flyingR"
        
class Boss(Enemy):
    def __init__(self, pos, constraint, stage_name, stage,facingDirection=pg.Vector2(1,0)):
        super().__init__(pos, 250, constraint)
        
        self.datos_json = ConfigManager.load_configs(self, CONFIG_FILE_PATH)
        self.datos_stage = self.datos_json.get(stage_name)
        self.stage_name = stage_name
        self.images = {}  # Initialize the images attribute
        self.load_sprites("assets/Enemy/Slime/Idle-Run (44x30).png")
        self.state = "idle"
        self.gravity_speed = 0
        # print(self.datos_stage)
        self.rect = pg.Rect(pos.x, pos.y, self.images["idleL"][0].get_width() , self.images["idleL"][0].get_height())

        self.hp_enemy = 30
        self.shoot_timer = 200
        self.shoot_cooldown = 250
        self.stage = stage
    def shoot(self, player_pos: pg.Vector2):
        # Calculate the direction from the boss to the player
        direction_to_player = pg.Vector2(player_pos - self.pos).normalize()

        # Check if the player is below the boss
        if direction_to_player.y > 0:
            # If the player is below, shoot diagonally downward
            shoot_direction = pg.Vector2(random.uniform(-1, 1), random.uniform(0.5, 1)).normalize()
        else:
            # If the player is not below, shoot vertically downward
            shoot_direction = pg.Vector2(0, 1)

        # Add the bullet to the bullet group with the calculated direction in center image
        self.stage.bullet_bat_group.add(Bullet_Bat(pg.Vector2(self.pos.x + self.rect.width/2,self.pos.y + self.rect.height/2), shoot_direction))
    
    def load_sprites(self, path):
        self.images["idleL"] = SurfaceManager.get_surface_from_spritesheetx4(path, 10, 1, 1,False,8)
        self.images["idleR"] = SurfaceManager.get_surface_from_spritesheetx4(path, 10, 1, 1,True,8)
        
    def update(self, delta_ms, player_pos):
        super().update(delta_ms)
        self.shoot_timer -= delta_ms
        if self.shoot_timer <= 0:
            self.shoot(player_pos)
            self.shoot_timer = self.shoot_cooldown

        if self.facingDirection.x < 0:
            self.state = "idleL"
        else:
            self.state = "idleR"
        
