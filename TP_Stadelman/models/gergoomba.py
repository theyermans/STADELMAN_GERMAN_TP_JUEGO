import pygame as pg
from enemy import Enemy
from auxiliares import SurfaceManager

class Gergoomba(Enemy):
    def __init__(self, pos, constraint):
        Enemy.__init__(self, pos, 250, constraint)
        
        self.load_sprites("assets/Enemy/bat/Flying (46x30).png")
        self.state =  "flyingR"
        self.gravity_speed = 0
        
        self.rect = pg.Rect(pos.x, pos.y, self.images["flyingR"][0].get_width (), self.images["flyingR"][0].get_height () )
        
    def load_sprites(self, path):
        self.images["flyingR"] = SurfaceManager.get_surface_from_spritesheet(path, 7, 1, 1, True)
        self.images["flyingL"] = SurfaceManager.get_surface_from_spritesheet(path, 7, 1)
        
    def update(self, delta_ms,player):
        super().update(delta_ms)
        if self.facingDirection.x < 0:
            self.state = "flyingL"
        else:
            self.state = "flyingR"
        # Check for collision with the player
        if self.check_collision_with_player(player):
            # Handle collision with the player (e.g., decrease player's health)
            player.receive_damage()
            
    