from .base import items

from utils.json_loader import load_json

items_settings = load_json("data/items.json")
potion_settings = items_settings["heal_potion"]

class heal_potion(items):
    def __init__(self, pos=None, id=0):
        self.pos = pos
        self.id = id
        super().__init__(
            name=potion_settings["name"],
            description=potion_settings["description"],
            icon=potion_settings["icon"],
            # потом цену прикрутим
        )

    def use(self, target):
        heal_amount = target.max_hp * potion_settings["heal_percent"]
        target.hp = min(target.hp + heal_amount, target.max_hp)
        return heal_amount
