import os
import random
import sys

from shop.shop import display_shop
from utils.json_loader import load_json
from characters import Enemy, Player, Position
from characters.enemy import move_tw
from items import heal_potion
from map import Level
from ui.render import draw, display_inventory, display_status, draw_tg
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
        if p.matrix[y1][x1] == "  " and level_number >= 3:
            rr = random.randint(1, 10)
            if rr in range(1,3):
                enemies.append(
                    Enemy(
                        hp = enemies_settings["rabit"]["hp"] + (10 * level_number),
                        damage = enemies_settings["rabit"]["damage"] + (5 * level_number),
                        pos=Position(x1, y1), id=len(enemies) + 1, 
                        cost = enemies_settings["rabit"]["cost"], 
                        exp = enemies_settings["rabit"]["exp"], 
                        icon = enemies_settings["rabit"]["icon"]
                        )
                    )
            else:
                enemies.append(
                    Enemy(
                        hp = enemies_settings["tiger"]["hp"] + (10 * level_number),
                        damage = enemies_settings["tiger"]["damage"] + (5 * level_number),
                        pos=Position(x1, y1), id=len(enemies) + 1, 
                        cost = enemies_settings["tiger"]["cost"], 
                        exp = enemies_settings["tiger"]["exp"], 
                        icon = enemies_settings["tiger"]["icon"]
                        )
                    )
        elif p.matrix[y1][x1] == "  " and level_number < 3:
            rr = random.randint(1, 10)
            if rr in range(1,7):
                enemies.append(
                    Enemy(
                        hp = enemies_settings["rabit"]["hp"] + (10 * level_number),
                        damage = enemies_settings["rabit"]["damage"] + (5 * level_number),
                        pos=Position(x1, y1), id=len(enemies) + 1, 
                        cost = enemies_settings["rabit"]["cost"], 
                        exp = enemies_settings["rabit"]["exp"], 
                        icon = enemies_settings["rabit"]["icon"]
                        )
                    )
            else:
                enemies.append(
                    Enemy(
                        hp = enemies_settings["tiger"]["hp"] + (10 * level_number),
                        damage = enemies_settings["tiger"]["damage"] + (5 * level_number),
                        pos=Position(x1, y1), id=len(enemies) + 1, 
                        cost = enemies_settings["tiger"]["cost"], 
                        exp = enemies_settings["tiger"]["exp"], 
                        icon = enemies_settings["tiger"]["icon"]
                        )
                    )


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
    
    draw_tg(p, b, enemies, heal_potions, current_level.number)

    while True:
        try:
            key = read_key()
            if key == "\x1b":
                print("Игра завершена.")
                break
        except:
            continue

        b.move(key, p, heal_potions, enemies)
        
        move_tw(p, b, enemies)
        os.system("cls")
        draw_tg(p, b, enemies, heal_potions, current_level.number)

        if key in ("e", "у"):
            display_inventory(b)
            os.system("cls")
            draw_tg(p, b, enemies, heal_potions, current_level.number)
            continue

        elif key in ("q", "й"):
            print("\n" + "= " * 30)
            display_shop(b, b.money, heal_potions)
            os.system("cls")
            draw_tg(p, b, enemies, heal_potions, current_level.number)
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
                        b.exp = b.exp - b.exp_need
                        b.exp_need = b.exp_need + b.exp_need // 3
                        b.max_hp += 25
                        b.hp += b.max_hp//2
                        b.damage += 10
                    enemies.remove(closest)
                else:
                    os.system("cls")
                    print(f"Враг не стерпел и наносит {closest.damage} урона.")
                    player_died = not b.take_damage(closest.damage)
                    print(f"У тя осталось {b.hp:.0f} HP.")
                    draw_tg(p, b, enemies, heal_potions, current_level.number)
                    if player_died:
                        print("как ты проиграл ваще...")
                        return
                
            else:
                move_tw(p,b,enemies)
                os.system("cls")
                draw_tg(p, b, enemies, heal_potions, current_level.number)
                print("Зачем ты попросту мечом машешь?...")


            print("\nНажмите любую клавишу для продолжения...")
            wait_key()
            os.system("cls")
            draw_tg(p, b, enemies, heal_potions, current_level.number)
            continue     

        if not enemies_attack_nearby(b, enemies):
            b.icon = "❌"
            draw_tg(p, b, enemies, heal_potions, current_level.number)
            print("\nВы нафидонили бомжу на этой локации. Последняя надежда канула в лету")
            return
    
        if key in ("z", "я"):
            if len(enemies) == 0:
                level_number += 1
                os.system("cls")
                run(level_number, b)
                return
            else:
                print('Вы не можете переместиться на следуюший уровень, есть еще враги!')
                wait_key()
