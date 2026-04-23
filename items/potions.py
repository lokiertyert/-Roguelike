from .base import items

from utils.json_loader import load_json

items_settings = load_json("data/items.json")
potion_settings = items_settings["heal_potion"]
big_potion_settings = items_settings["big_heal_potion"]

class heal_potion(items):
    def __init__(self, pos=None, id=0):
        self.pos = pos
        self.id = id
        super().__init__(
            name=potion_settings["name"],
            description=potion_settings["description"],
            icon=potion_settings["icon"],
        )

    def use(self, target):
        heal_amount = target.max_hp * potion_settings["heal_percent"]
        target.hp = min(target.hp + heal_amount, target.max_hp)
        return heal_amount

class big_heal_potion(items):
    def __init__(self, id=0):
        self.id = id
        super().__init__(
            name=big_potion_settings["name"],
            description=big_potion_settings["description"],
            icon=big_potion_settings["icon"],
        )
    
    def use(self, target):
        heal_amount = target.max_hp * big_potion_settings["heal_percent"]
        target.hp = min(target.hp + heal_amount, target.max_hp)
        return heal_amount