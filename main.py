from game.runner import run
from characters.player import Player
from characters.base import Position
from utils.json_loader import load_json


if __name__ == "__main__":
    settings = load_json("data/settings.json")

    b = Player()
    b.pos = Position(1, 1)
    b.name = settings["player"]["name"]
    b.money = settings["player"]["money"]
    b.max_hp = settings["player"]["hp"]
    b.hp = settings["player"]["hp"]
    b.damage = settings["player"]["damage"]
    run(1, b)



