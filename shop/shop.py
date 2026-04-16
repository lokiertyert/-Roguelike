class Shop:
    def __init__(self):
        self.items = [
            {"name": "Зелье здоровья (x3)", "price": 50, "type": "heal_potion", "quantity": 3},
            {"name": "Усиление атаки (+5)", "price": 75, "type": "damage_boost", "value": 5},
            {"name": "Увеличение макс. HP (+20)", "price": 100, "type": "max_hp_boost", "value": 20},
        ]