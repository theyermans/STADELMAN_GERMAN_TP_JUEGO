import pygame.sprite

from auxiliares import SurfaceManager

class Items(pygame.sprite.Sprite):
    def __init__(self, x ,y, item_type):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type  # monedas hongo
        self.images = {}
        self.images["coin"] = SurfaceManager.get_surface_from_spritesheet("./assets/coin_.png", 12, 1)
        self.heart_image_path ="./assets/Player/hi_overlay_variant_hearts_x1_1_png_1354840444.png"
        self.images["heart"] =   SurfaceManager.get_surface_from_spritesheet(self.heart_image_path,1,1)
        self.frame_duration_ms = 1000 / 30
        self.frame_elapsed_time = self.frame_duration_ms
        self.current_frame = 0
        self.image = None  # Nuevo atributo image
        self.x =x
        self.y=y
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        

                
    def update_frame(self, delta_ms):
        
        self.frame_elapsed_time -= delta_ms
        if self.frame_elapsed_time <= 0:
            self.frame_elapsed_time = self.frame_duration_ms
            self.current_frame += 1
            if self.current_frame >= len(self.images[self.item_type]):
                self.current_frame = 0
            self.image = self.images[self.item_type][self.current_frame]
            
            
    def draw(self, screen, delta_ms: float):
        if self.current_frame >= len(self.images[self.item_type]):
            self.current_frame = 0
        screen.blit(self.images[self.item_type][self.current_frame], self.rect.topleft)#pygame.Vector2(self.x + self.rect.width/2,self.pos.y + self.rect.height/2)
        #pygame.draw.rect(screen, (255, 0, 0), self.rect,2)
        

