from .base import items
from utils.json_loader import load_json

items_settings = load_json("data/items.json")
max_hp_settings = items_settings["max_hp_boost"]

class max_hp_plus(items):
    def __init__(self):
        super().__init__(
            name=max_hp_settings["name"],
            description=max_hp_settings["description"],
            cost=max_hp_settings["cost"]
        )
    
    def use(self, target):
        heal_amount = target.max_hp + max_hp_settings["plus"]
        return heal_amount