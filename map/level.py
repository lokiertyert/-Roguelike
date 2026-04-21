from utils.json_loader import load_json
from .pole import Pole, brick_swap
settings = load_json("data/settings.json")

class Level:
    def __init__(self, number):
        self.number = number
        self.enemies_count = 4 + number

    def create_level(self):
        pole = Pole(settings['map_width'], settings['map_height'])
        brick_swap(pole)
        return pole