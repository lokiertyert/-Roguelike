import os
import random

from utils.json_loader import load_json 

from characters import Enemy, Player, Position
from items import heal_potion
from map import Pole, brick_swap
from ui import draw
from utils.input import read_key, wait_key

from .combat import enemies_attack_nearby, find_closest_enemy


settings = load_json("data/settings.json")
enemies_settings = load_json("data/enemies.json")

def run():
    p = Pole(settings["map_width"], settings["map_height"])
    brick_swap(p)

    enemies = []
    for i in range(settings["enemies_count"]):
        enemies.append(Enemy(pos=Position(random.randint(1, p.width - 2), random.randint(1, p.height - 2)), id=i + 1))

    heal_potions = []
    for i in range(settings["potions_count"]):
        heal_potions.append(heal_potion(pos=Position(random.randint(1, p.width - 2), random.randint(1, p.height - 2)), id=i + 1))

    b = Player()
    b.pos = Position(1, 1)
    b.name = settings["player"]["name"]
    b.money = settings["player"]["money"]
    b.max_hp = settings["player"]["hp"]
    b.hp = settings["player"]["hp"]
    b.damage = settings["player"]["damage"]
    draw(p, b, enemies, heal_potions)

    while True:
        try:
            key = read_key()

            if key == "\x1b":  # Выход через эскейп
                print("Игра завершена.")
                break
        except:
            continue

        if key == "e" or key == "у":
            print("\n" + "=" * 30)
            b.display_inventory(heal_potions)
            os.system("cls")
            b.display_status()
            print()
            draw(p, b, enemies, heal_potions)
            continue

        # АТАКА
        elif key == "f" or key == "а":
            closest, dist = find_closest_enemy(b, enemies)
            if closest is None:
                print("На поле нет врагов! Вы победили!")
                break
            if dist == 1:
                print(f"\n Ты атакуешь врага! Нанесено {b.damage} дамага.")
                enemy_died = not closest.take_damage(b.damage)
                print(f"У энеми осталось {closest.hp:.0f} HP.")
                if enemy_died:
                    print("Туда бомжа!")
                    enemies.remove(closest)
                else:
                    print(f"Враг не стерпел и наносит {closest.damage} урона.")
                    player_died = not b.take_damage(closest.damage)
                    print(f"У тя осталось {b.hp:.0f} HP.")
                    if player_died:
                        print("как ты проиграл ваще...")
                        break
            else:
                print(f"Зачем ты попросту мечом машешь?...")
            print("\nНажмите любую клавишу для продолжения...")
            wait_key()
            os.system("cls")
            b.display_status()
            print()
            draw(p, b, enemies, heal_potions)
            continue

        b.move(key, p, heal_potions)

        for enemy in enemies:
            enemy.move(random.choice(["w", "a", "s", "d"]), p)

        if not enemies_attack_nearby(b, enemies):
            print("\nВы нафидонили бомжу на этой локации. Последняя надежда канула в лету")
            break

        os.system("cls")
        b.display_status()
        print()
        draw(p, b, enemies, heal_potions)
