import random
import os
import msvcrt

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Person:
    def __init__(self, pos=None, damage=0, hp=0):
        self.pos = pos
        self.damage = damage
        self.hp = hp
        self.max_hp = hp

    def take_damage(self, amount):
        """Получить урон. Возвращает True, если персонаж ещё жив."""
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        return self.hp > 0

class items:
    def __init__(self, name, description, icon=""):
        self.name = name
        self.description = description
        self.icon = icon

class heal_potion(items):
    def __init__(self, pos=None, id=0):
        self.pos = pos
        self.id = id
        super().__init__(
            name="Зелье здоровья",
            description="Восстанавливает 25% от максимального здоровья",
            icon="💗"
        )

    def use(self, target):
        heal_amount = target.max_hp * 0.25
        target.hp = min(target.hp + heal_amount, target.max_hp)
        return heal_amount

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
            msvcrt.getch()
            return
        while True:
            os.system("cls")
            self.display_status()
            print()
            print("\n=== ИНВЕНТАРЬ ===")
            for i, potion in enumerate(self.inventory, 1):
                print(f"{i}. {potion.name} — {potion.description}")

            print("\nВведите номер зелья для использования (0 — выход):")
            key = msvcrt.getch().decode("utf-8").lower()
            if key == '0':
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
                    msvcrt.getch()
                    return
                else:
                    print("\nНеверный номер. Нажмите любую клавишу")
                    msvcrt.getch()
            except ValueError:
                print("\nВведите число. Нажмите любую клавишу")
                msvcrt.getch()

class Enemy(Person):
    def __init__(self, id=0, pos=None, damage=10, hp=50, icon="🐯"):
        super().__init__(pos, damage, hp)
        self.id = id
        self.icon = icon

    def move(self, input_key, pole):
        if (input_key == "w" or input_key == "ц") and pole.matrix[self.pos.y - 1][self.pos.x] != "◻ " and pole.matrix[self.pos.y - 1][self.pos.x] != "🐥":
            self.pos.y -= 1
        elif (input_key == "s" or input_key == "ы") and pole.matrix[self.pos.y + 1][self.pos.x] != "◻ " and pole.matrix[self.pos.y + 1][self.pos.x] != "🐥":
            self.pos.y += 1
        elif (input_key == "a" or input_key == "ф") and pole.matrix[self.pos.y][self.pos.x - 1] != "◻ " and pole.matrix[self.pos.y][self.pos.x - 1] != "🐥":
            self.pos.x -= 1
        elif (input_key == "d" or input_key == "в") and pole.matrix[self.pos.y][self.pos.x + 1] != "◻ " and pole.matrix[self.pos.y][self.pos.x + 1] != "🐥":
            self.pos.x += 1

    def attack_player(self, player):
        player.take_damage(self.damage)
        print(f"Враг нанёс вам {self.damage} урона! У вас осталось {player.hp:.0f} HP.")

class Pole:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = []
        for i in range(width):
            row = []
            for j in range(height):
                if i == 0 or j == 0 or i == width-1 or j == height-1:
                    row.append("◻ ")
                else:
                    row.append("  ")
            self.matrix.append(row)

def brick_swap(current_pole):
    t_width = current_pole.width
    t_height = current_pole.height
    quality_swaps = t_width * t_height // 4
    for i in range(quality_swaps):
        x1 = random.randint(1, t_width-2)
        y1 = random.randint(1, t_height-2)
        current_pole.matrix[x1][y1] = "◻ "

def draw(current_pole, player, enemies, heal_potions):
    for i in range(current_pole.width):
        for j in range(current_pole.height):
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

def find_closest_enemy(player, enemies):
    if not enemies:
        return None, None
    closest = None
    min_dist = float('inf')
    for enemy in enemies:
        dist = abs(enemy.pos.x - player.pos.x) + abs(enemy.pos.y - player.pos.y)
        if dist < min_dist:
            min_dist = dist
            closest = enemy
    return closest, min_dist

def enemies_attack_nearby(player, enemies):
    for enemy in enemies:
        dx = abs(enemy.pos.x - player.pos.x)
        dy = abs(enemy.pos.y - player.pos.y)
        if (dx == 1 and dy == 0) or (dx == 0 and dy == 1):
            enemy.attack_player(player)
            if player.hp <= 0:
                return False
    return True

p = Pole(15, 50)
brick_swap(p)

enemies = []
for i in range(5):
    enemies.append(Enemy(pos=Position(random.randint(1, p.height-2), random.randint(1, p.width-2)), id=i+1))

heal_potions = []
for i in range(5):
    heal_potions.append(heal_potion(pos=Position(random.randint(1, p.height-2), random.randint(1, p.width-2)), id=i+1))

b = Player()
b.pos = Position(1, 1)
b.name = "IlyaRub"
b.money = 67
b.max_hp = 100
b.hp = 100
b.damage = 25
draw(p, b, enemies, heal_potions)

while True:
    try:
        key = msvcrt.getch()
        
        if key == b'\x1b':  # Escape
            print("Игра завершена.")
            break
        
        key = key.decode("cp1251").lower()
    except:
        continue

    if key == 'e' or key == 'у':
        print("\n" + "="*30)
        b.display_inventory(heal_potions)
        os.system("cls")
        b.display_status()
        print()
        draw(p, b, enemies, heal_potions)
        continue

    # АТАКА
    elif key == 'f' or key == 'а':
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
        msvcrt.getch()
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