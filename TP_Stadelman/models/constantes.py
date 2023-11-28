import json

screen_h = 720
screen_w = 1280
CONFIG_FILE_PATH = './configs/config.json'
GRAVITY = 20


def open_configs() -> dict:
    with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as config:
        return json.load(config)