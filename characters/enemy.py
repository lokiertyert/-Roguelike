from .base import Person


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
