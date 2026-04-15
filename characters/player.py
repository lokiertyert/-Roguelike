import os

from .base import Person
from utils.input import read_key, wait_key


class Player(Person):
    def __init__(self, name=None, pos=None, damage=25, hp=100, money=0, icon="🐥"):
        super().__init__(pos, damage, hp)
        self.name = name
        self.money = money
        self.icon = icon
        self.inventory = []

    def move(self, input_key, pole, heal_potions):
        old_x, old_y = self.pos.x, self.pos.y

        if (input_key == "w" or input_key == "ц") and pole.matrix[self.pos.y - 1][self.pos.x] != "◻ " and pole.matrix[self.pos.y - 1][self.pos.x] != "🐯":
            self.pos.y -= 1
        elif (input_key == "s" or input_key == "ы") and pole.matrix[self.pos.y + 1][self.pos.x] != "◻ " and pole.matrix[self.pos.y + 1][self.pos.x] != "🐯":
            self.pos.y += 1
        elif (input_key == "a" or input_key == "ф") and pole.matrix[self.pos.y][self.pos.x - 1] != "◻ " and pole.matrix[self.pos.y][self.pos.x - 1] != "🐯":
            self.pos.x -= 1
        elif (input_key == "d" or input_key == "в") and pole.matrix[self.pos.y][self.pos.x + 1] != "◻ " and pole.matrix[self.pos.y][self.pos.x + 1] != "🐯":
            self.pos.x += 1

        # Сбор зелий
        collected_potions = []
        for potion in heal_potions:
            if potion.pos.x == self.pos.x and potion.pos.y == self.pos.y:
                self.inventory.append(potion)
                collected_potions.append(potion)
        for potion in collected_potions:
            heal_potions.remove(potion)

    def display_status(self):
        print(f"Игрок: {self.name}")
        print(f"HP: {self.hp:.0f}/{self.max_hp}")
        print(f"Деньги: {self.money}")
        print("Инвентарь (Нажмите e чтобы открыть)")
        print("Атаковать ближайшего врага (Нажмите f)")

    def display_inventory(self, heal_potions):
        if not self.inventory:
            print("Инвентарь пуст")
            print("\nНажмите любую клавишу для продолжения")
            wait_key()
            return
        while True:
            os.system("cls")
            self.display_status()
            print()
            print("\n=== ИНВЕНТАРЬ ===")
            for i, potion in enumerate(self.inventory, 1):
                print(f"{i}. {potion.name} — {potion.description}")

            print("\nВведите номер зелья для использования (0 — выход):")
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
                    print("\nНеверный номер. Нажмите любую клавишу")
                    wait_key()
            except ValueError:
                print("\nВведите число. Нажмите любую клавишу")
                wait_key()
