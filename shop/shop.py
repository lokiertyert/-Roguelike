import os
from utils.json_loader import load_json
from ui.render import display_status
from items.potions import heal_potion, big_heal_potion
from utils.input import read_key, wait_key

items_settings = load_json("data/items.json")
items = list(load_json("data/items.json"))

def display_shop(self, player_money, heal_potions):
    self.money = player_money
    while True:
        os.system("cls")
        display_status(self)
        print("\n=== МАГАЗИН ===")
        for i, item in enumerate(items_settings["heal_potion"], 1):
            print(f'{i}. {items_settings["heal_potion"]["name"]} — {items_settings["heal_potion"]["description"]}')
            print(f'Цена: {items_settings["heal_potion"]["cost"]} монет')
            print()
            break
        for j, item in enumerate(items_settings["big_heal_potion"], 2): 
            print(f'{j}. {items_settings["big_heal_potion"]["name"]} — {items_settings["big_heal_potion"]["description"]}')
            print(f'Цена: {items_settings["big_heal_potion"]["cost"]} монет')
            break

        print("\nВведите номер товара для покупки (0 — выход): ")
        key = read_key()
        if key == "0":
            return
        try:
            choice = int(key)
            if 1 <= choice <= len(items):
                selected_item = items[choice - 1]
            else:
                print("\nНеверный номер.")
                wait_key()
        
            if selected_item == items[0]:
                if self.money >= items_settings["heal_potion"]["cost"]:
                    self.money -= items_settings["heal_potion"]["cost"]
                    print(f"\nВы купили {items_settings['heal_potion']['name']}! Предмет добавлен в инвентарь. Спасибо за покупку!")
                    print(f"У вас осталось: {self.money} монет")
                    self.inventory.append (heal_potion(id=len(heal_potions) + 1))
                    print("\nНажмите любую клавишу для продолжения")
                    wait_key()
                    return
                else:
                    print("\nУ вас недостаточно монет. Возвращайтесь когда станете побогаче")
                    wait_key()

            elif selected_item == items[1]:
                if self.money >= items_settings["big_heal_potion"]["cost"]:
                    self.money -= items_settings["big_heal_potion"]["cost"]
                    print(f"\nВы купили {items_settings['big_heal_potion']['name']}! Предмет добавлен в инвентарь. Спасибо за вашу покупку!")
                    print(f"У вас осталось: {self.money} монет")
                    self.inventory.append (big_heal_potion(id=len(heal_potions) + 1))
                    print("\nНажмите любую клавишу для продолжения")
                    wait_key()
                    return
                else:
                    print("\nУ вас недостаточно монет. Возвращайтесь когда станете побогаче")
                    wait_key()
        except ValueError:
            print("\nВведите число.")
            wait_key()