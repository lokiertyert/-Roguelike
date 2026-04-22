import os
from utils.json_loader import load_json
from ui.render import display_status
from items.potions import heal_potion, big_heal_potion
from utils.input import read_key, wait_key
from characters.player import Player

items_settings = load_json("data/items.json")
settings = load_json("data/settings.json")

b = Player()
b.money = settings["player"]["money"]
print(b.money - items_settings["heal_potion"]['cost'])