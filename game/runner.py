import os
import random
import sys

from utils.json_loader import load_json
from characters import Enemy, Player, Position
from items import heal_potion
from map import Level
from ui import draw
from utils.input import read_key, wait_key
from .combat import enemies_attack_nearby, find_closest_enemy

settings = load_json("data/settings.json")
enemies_settings = load_json("data/enemies.json")
items_settings = load_json("data/items.json")

def run(level_number):
    current_level = Level(level_number)
    p = current_level.create_level()
    
    enemies = []
    while len(enemies) < settings["start_enemies_count"] + level_number:
        y1 = random.randint(1, p.height - 2)
        x1 = random.randint(1, p.width - 2)
        if p.matrix[y1][x1] != "◻":
            enemies.append(Enemy(hp = 40 + (10 * level_number), damage = 10 * level_number, pos=Position(x1, y1), id=len(enemies) + 1))

    heal_potions = []
    while len(heal_potions) < settings["potions_count"]:
        y1 = random.randint(1, p.height - 2)
        x1 = random.randint(1, p.width - 2)
        if p.matrix[y1][x1] != "◻" and not any(e.pos.x == x1 and e.pos.y == y1 for e in enemies):
            heal_potions.append(heal_potion(pos=Position(x1, y1), id=len(heal_potions) + 1))

    b = Player()
    b.pos = Position(1, 1)
    b.name = settings["player"]["name"]
    b.money = settings["player"]["money"]
    b.max_hp = settings["player"]["hp"]
    b.hp = settings["player"]["hp"]
    b.damage = settings["player"]["damage"]
    
    b.display_status()
    print(f"LEVEL: {level_number}")
    draw(p, b, enemies, heal_potions)

    while True:
        try:
            key = read_key()
            if key == "\x1b":
                print("Игра завершена.")
                break
        except:
            continue

        if key in ("e", "у"):
            print("\n" + "= " * 30)
            b.display_inventory()
            os.system("cls")
            b.display_status()
            print(f"LEVEL: {level_number}")
            print()
            draw(p, b, enemies, heal_potions)
            continue

        elif key in ("f", "а"):
            closest, dist = find_closest_enemy(b, enemies)
            if closest is None:
                print("На поле нет врагов! Для перехода не следующий этаж нажмите z")
            if dist == 1:
                print(f"\nТы атакуешь врага! Нанесено {b.damage} дамага.")
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
                        sys.exit()
            else:
                print("Зачем ты попросту мечом машешь?...")
            print("\nНажмите любую клавишу для продолжения...")
            wait_key()
            os.system("cls")
            b.display_status()
            print(f"LEVEL: {level_number}")
            print()
            draw(p, b, enemies, heal_potions)
            continue

        b.move(key, p, heal_potions, enemies)
        
        for enemy in enemies:
            enemy.move(random.choice(["w", "a", "s", "d"]), p, b, enemies)

        if not enemies_attack_nearby(b, enemies):
            print("\nВы нафидонили бомжу на этой локации. Последняя надежда канула в лету")
            break

        os.system("cls")
        b.display_status()
        print(f"LEVEL: {level_number}")
        print()
        draw(p, b, enemies, heal_potions)

        if key in ("z", "я"):
            if len(enemies) == 0:
                level_number += 1
                os.system("cls")
                run(level_number)
            else:
                print('Вы не можете переместиться на следуюший уровень, есть еще враги!')
                wait_key()
