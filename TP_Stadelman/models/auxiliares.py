import pygame as pg
import pygame.font
from constantes import FONT_GLOBAL
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
    
    def get_surface_from_spritesheet_with_scale(img_path: str, cols: int, rows: int, step=1, flip: bool = False, scale: int = 4) -> list[pg.surface.Surface]:
        sprites_list = list()
        surface_img = pg.transform.scale(pg.image.load(img_path), (scale * pg.image.load(img_path).get_width(), scale * pg.image.load(img_path).get_height()))
        frame_width = int(surface_img.get_width() / (cols * scale))
        frame_height = int(surface_img.get_height() / (rows * scale))

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
    def get_surface_from_spritesheetx4(img_path: str, cols: int, rows: int, step = 1, flip: bool = False,scale=4) -> list[pg.surface.Surface]:
        sprites_list = list()
        
        surface_img = pg.transform.scale2x(pg.image.load(img_path))
        surface_img = pg.transform.scale(pg.image.load(img_path),(scale * pg.image.load(img_path).get_width(), scale * pg.image.load(img_path).get_height()))
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
        self.color_texto = ("white")
        self.font = pygame.font.SysFont(FONT_GLOBAL, 48)
        self.prep_score()

    def prep_score(self):
        self.score_str = str(self.score)
        self.score_txt = self.font.render(self.score_str, True, self.color_texto, None)
        self.score_rect = self.score_txt.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
            
    
        
    #recive score desde stage y lo renderiza
    def muestra_score(self, score=None):
        if score is not None:
            self.score = score
            
        self.score_str = str(self.score)
        self.score_str = f"{self.score:06}"
        self.score_txt = self.font.render(self.score_str, True, self.color_texto, None)
        
        self.score_rect.topright = (self.screen.get_width() - 150, 10)

        self.screen.blit(self.score_txt, self.score_rect)
        
        
        