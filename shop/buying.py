from items.potions import heal_potion

def buy_item(self, player, choice):
    if choice == 0:
        print("Выход из магазина.")
        return False

    if 1 <= choice <= len(self.items):
        item = self.items[choice - 1]
        if player.money >= item['price']:
            player.money -= item['price']

            # Обработка разных типов покупок
            if item['type'] == "heal_potion":
                for _ in range(item['quantity']):
                    potion = heal_potion(pos=None, id=len(player.inventory) + 1)
                    player.inventory.append(potion)
                print(f"Куплено {item['quantity']} зелий здоровья!")

            elif item['type'] == "damage_boost":
                player.damage += item['value']
                print(f"Атака увеличена на {item['value']}!")

            elif item['type'] == "max_hp_boost":
                player.max_hp += item['value']
        player.hp = player.max_hp
        print(f"Макс. HP увеличено на {item['value']} и полностью восстановлено!")