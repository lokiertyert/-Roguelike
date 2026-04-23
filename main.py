from game.runner import run
from characters.player import Player
from characters.base import Position
from utils.json_loader import load_json
from utils.input import read_key
import os


if __name__ == "__main__":
    while True:
        print("Если желаете начать, нажмите 'E'")
        print("Если хотите выйти, нажмите другую клавишу...")
        key = read_key()
        os.system("cls")
        if key == "e" or key == "у":
            settings = load_json("data/settings.json")
            player = Player()
            player.pos = Position(1, 1)
            player.name = settings["player"]["name"]
            player.money = settings["player"]["money"]
            player.max_hp = settings["player"]["hp"]
            player.hp = settings["player"]["hp"]
            player.damage = settings["player"]["damage"]
            run(1, player)
        else:
            break