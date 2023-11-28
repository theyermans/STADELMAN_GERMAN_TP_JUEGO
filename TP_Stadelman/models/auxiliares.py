import pygame as pg
import pygame.font
class SurfaceManager:

    @staticmethod
    def get_surface_from_spritesheet(img_path: str, cols: int, rows: int, step = 1, flip: bool = False) -> list[pg.surface.Surface]:
        sprites_list = list()
        surface_img = pg.transform.scale2x(pg.image.load(img_path))
        frame_width = int(surface_img.get_width()/cols)
        frame_height = int(surface_img.get_height()/rows)
        
        for row in range(rows):

            for column in range(0, cols, step):
                x_axis = column * frame_width
                y_axis = row * frame_height

                frame_surface = surface_img.subsurface(
                    x_axis, y_axis, frame_width, frame_height
                )

                if flip:
                    frame_surface = pg.transform.flip(frame_surface, True, False)
                sprites_list.append(frame_surface)
        return sprites_list
    
    @staticmethod
    def get_surface_from_spritesheet1x(img_path: str, cols: int, rows: int, step = 1, flip: bool = False) -> list[pg.surface.Surface]:
        sprites_list = list()
        surface_img = pg.image.load(img_path)
        frame_width = int(surface_img.get_width()/cols)
        frame_height = int(surface_img.get_height()/rows)
        
        for row in range(rows):

            for column in range(0, cols, step):
                x_axis = column * frame_width
                y_axis = row * frame_height

                frame_surface = surface_img.subsurface(
                    x_axis, y_axis, frame_width, frame_height
                )

                if flip:
                    frame_surface = pg.transform.flip(frame_surface, True, False)
                sprites_list.append(frame_surface)
        return sprites_list
    
class TablaPuntajes:
    def __init__(self,screen, score):
        self.screen = screen
        self.score = score
        self.color_texto = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()
        
    def prep_score(self):
        self.score_str = str(self.score)
        self.score_imagen = self.font.render(self.score_str, True, self.color_texto, None)
        
        self.score_rect = self.score_imagen.get_rect()
        self.screen_rect = self.screen.get_rect()
        
        # Use screen_rect instead of self.screen_rect
        self.score_rect = self.score_imagen.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        
    def muestra_score(self):
        self.screen.blit(self.score_imagen, self.score_rect)
        
        
        