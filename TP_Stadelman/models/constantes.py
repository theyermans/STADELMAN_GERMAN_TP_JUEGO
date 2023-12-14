import json
import pygame
from pygame.locals import *
# from typing import Optional
# from ._common import FileArg
screen_h = 720
screen_w = 1280
CONFIG_FILE_PATH = './configs/config.json'
GRAVITY = 25
FONT_GLOBAL = 'impact'
FPS = 120


# def open_configs() -> dict:
#     with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as config:
#         return json.load(config)
# COLOR CONSTANTS
C_RED = (255,0,0)
C_GREEN = (0,255,0)
C_BLUE = (0,0,255)
C_BLACK = (0,0,0)
C_WHITE = (255,255,255)
C_PINK = (255, 0, 160)
C_PEACH = (255, 118, 95)
C_BLUE_2 = (38, 0, 160)
C_YELLOW_2 = (255, 174, 0)
C_GREEEN_2 = (38, 137, 0)
C_ORANGE = (255, 81, 0)

# MOUSE CONSTANTS
M_STATE_NORMAL = 0
M_STATE_HOVER = 1
M_STATE_CLICK = 3
M_BRIGHT_HOVER = (32,32,32)
M_BRIGHT_CLICK = (32,32,32)  
pygame.init()
  
class ConfigManager:
    def __init__(self):
        self.configs = None
    
    def load_configs(self, path)->dict:
        with open(path, 'r', encoding='utf-8') as config:
            self.configs = json.load(config)
        return self.configs
    
    def get_configs(self):
        return self.configs
    
    
    
class Music_Controller:
    def __init__(self, volume):
        self.volume = volume

    @staticmethod
    def adjust_volume(new_volume):
        pygame.mixer.music.set_volume(new_volume)

    @staticmethod
    def play_collision_sound():
        sound_collision = pygame.mixer.Sound("Recursos/sounds/laser_hit.wav")
        sound_collision.play()

    @staticmethod
    def play_background_music():
        pygame.mixer.music.load(r"Recursos/Vengeance (Loopable).wav")
        pygame.mixer.music.play(-1)
