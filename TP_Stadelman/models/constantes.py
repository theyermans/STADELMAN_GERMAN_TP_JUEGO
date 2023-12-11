import json

screen_h = 720
screen_w = 1280
CONFIG_FILE_PATH = './configs/config.json'
GRAVITY = 25
FONT_GLOBAL = 'impact'
FPS = 120


# def open_configs() -> dict:
#     with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as config:
#         return json.load(config)
    
class ConfigManager:
    def __init__(self):
        self.configs = None
    
    def load_configs(self, path)->dict:
        with open(path, 'r', encoding='utf-8') as config:
            self.configs = json.load(config)
        return self.configs
    
    def get_configs(self):
        return self.configs   
