import os
import random
import sys

from shop.shop import display_shop
from utils.json_loader import load_json
from characters import Enemy, Position
from items import heal_potion
from map import Level
from ui.render import draw, display_inventory, display_status
from utils.input import read_key, wait_key
from .combat import enemies_attack_nearby, find_closest_enemy


settings = load_json("data/settings.json")
enemies_settings = load_json("data/enemies.json")
items_settings = load_json("data/items.json")

def run(level_number, b):
    current_level = Level(level_number)
    p = current_level.create_level()
    enemies = []
    while len(enemies) < settings["start_enemies_count"] + level_number:
        y1 = random.randint(1, p.height - 2)
        x1 = random.randint(1, p.width - 2)
        if p.matrix[y1][x1] == "  ":
            enemies.append(Enemy(hp = 40 + (10 * level_number), damage = 10 + (5 * level_number), pos=Position(x1, y1), id=len(enemies) + 1, cost = enemies_settings["tiger"]["cost"], exp = enemies_settings["tiger"]["exp"]))

    heal_potions = []
    while len(heal_potions) != settings["potions_count"]:
        y1 = random.randint(1, p.height - 2)
        x1 = random.randint(1, p.width - 2)
        if p.matrix[y1][x1] == "  ":
            heal_potions.append(heal_potion(pos=Position(x1, y1), id=len(heal_potions) + 1))
    while True:
        yy = random.randint(1, p.height - 2)
        xx = random.randint(1, p.width - 2)
        if p.matrix[yy][xx] == "  ":
            b.pos.x = xx
            b.pos.y = yy
            break
    
    display_status(b)
    print(f"Этаж: {level_number}")
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
            display_inventory(b)
            os.system("cls")
            display_status(b)
            print(f"Этаж: {level_number}")
            print()
            draw(p, b, enemies, heal_potions)
            continue

        elif key in ("q", "й"):
            print("\n" + "= " * 30)
            display_shop(b, b.money, heal_potions)
            os.system("cls")
            display_status(b)
            print(f"Этаж: {level_number}")
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
                    b.money += closest.cost
                    b.exp += closest.exp
                    if b.exp >= b.exp_need:
                        b.lvl += 1
                        b.exp_need = b.exp_need + b.exp_need // 3
                        b.exp = 0
                        b.max_hp += 10
                        b.hp += 10
                        b.damage += 10
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
            display_status(b)
            print(f"Этаж: {level_number}")
            print()
            draw(p, b, enemies, heal_potions)
            continue

        b.move(key, p, heal_potions, enemies)
        
        for enemy in enemies:
            enemy.move(p, b, enemies)

        if not enemies_attack_nearby(b, enemies):
            print("\nВы нафидонили бомжу на этой локации. Последняя надежда канула в лету")
            sys.exit()
            
        os.system("cls")
        display_status(b)
        print(f"Этаж: {level_number}")
        print()
        draw(p, b, enemies, heal_potions)
    
        if key in ("z", "я"):
            if len(enemies) == 0:
                level_number += 1
                os.system("cls")
                run(level_number, b)
            else:
                print('Вы не можете переместиться на следуюший уровень, есть еще враги!')
                wait_key()
