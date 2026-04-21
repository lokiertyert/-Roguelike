import os
from characters.base import Person
from utils.input import read_key, wait_key
from characters.player import Player

def draw(current_pole, player, enemies, heal_potions):
    for i in range(current_pole.height):
        for j in range(current_pole.width):
            if player.pos.x == j and player.pos.y == i:
                print(player.icon, end="")
            elif any(enemy.pos.x == j and enemy.pos.y == i for enemy in enemies):
                for enemy in enemies:
                    if enemy.pos.x == j and enemy.pos.y == i:
                        print(enemy.icon, end="")
                        break
            elif any(potion.pos.x == j and potion.pos.y == i for potion in heal_potions):
                for potion in heal_potions:
                    if potion.pos.x == j and potion.pos.y == i and current_pole.matrix[i][j] != "◻ ":
                        print(potion.icon, end="")
                        break
                    elif (potion.pos.x == j and potion.pos.y == i) and (current_pole.matrix[i][j] == "◻ "):
                        print("◻ ", end="")
            else:
                print(current_pole.matrix[i][j], end="")
        print()

def display_status(self): 
        print(f"Игрок: {self.name} Уровень: {self.lvl} Опыт: {self.exp} из {self.exp_need}")
        print(f"HP: {self.hp:.0f}/{self.max_hp}")
        print(f"Урон: {self.damage}")
        print(f"Деньги: {self.money}")
        print("Инвентарь (Нажмите e чтобы открыть)")
        print("Атаковать ближайшего врага (Нажмите f)")

def display_inventory(self):
    if not self.inventory:
        print("Инвентарь пуст")
        print("\nНажмите любую клавишу для продолжения")

        wait_key()
        return
    
    while True:
        os.system("cls")
        display_status(self)
        print("\n=== ИНВЕНТАРЬ ===")
        for i, potion in enumerate(self.inventory, 1):
            print(f"{i}. {potion.name} — {potion.description}")

        print("\nВведите номер зелья для использования (0 — выход): ")
        key = read_key()
        if key == "0":
            return
        try:
            choice = int(key)
            if 1 <= choice <= len(self.inventory):
                selected_potion = self.inventory[choice - 1]
                healed_amount = selected_potion.use(self)
                self.inventory.pop(choice - 1)
                print(f"\nИспользовано: {selected_potion.name}")
                print(f"Восстановлено {healed_amount:.0f} HP!")
                print(f"Текущее HP: {self.hp:.0f}/{self.max_hp}")
                print("\nНажмите любую клавишу для продолжения")
                wait_key()
                return
            else:
                print("\nНеверный номер.")
                wait_key()
        except ValueError:
            print("\nВведите число.")
            wait_key()