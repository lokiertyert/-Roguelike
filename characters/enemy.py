from .base import Person

class Enemy(Person):
    def __init__(self, id=0, pos=None, damage=10, hp=50, icon="🐯"):
        super().__init__(pos, damage, hp)
        self.id = id
        self.icon = icon

    def move(self, input_key, pole, player, enemies):
        if (input_key == "w" or input_key == "ц") and self.pos.y > 0:
            if pole.matrix[self.pos.y - 1][self.pos.x] != "◻ ":
                if not (player.pos.x == self.pos.x and player.pos.y == self.pos.y - 1):
                    if not any(friend.pos.x == self.pos.x and friend.pos.y == self.pos.y - 1 for friend in enemies):
                        self.pos.y -= 1
                    
        elif (input_key == "s" or input_key == "ы") and self.pos.y < pole.height - 1:
            if pole.matrix[self.pos.y + 1][self.pos.x] != "◻ ":
                if not (player.pos.x == self.pos.x and player.pos.y == self.pos.y + 1):
                    if not any(friend.pos.x == self.pos.x and friend.pos.y == self.pos.y - 1 for friend in enemies):
                        self.pos.y += 1
                    
        elif (input_key == "a" or input_key == "ф") and self.pos.x > 0:
            if pole.matrix[self.pos.y][self.pos.x - 1] != "◻ ":
                if not (player.pos.x == self.pos.x - 1 and player.pos.y == self.pos.y):
                       if not any(friend.pos.x == self.pos.x - 1 and friend.pos.y == self.pos.y for friend in enemies):
                            self.pos.x -= 1
                    
        elif (input_key == "d" or input_key == "в") and self.pos.x < pole.width - 1:
            if pole.matrix[self.pos.y][self.pos.x + 1] != "◻ ":
                if not (player.pos.x == self.pos.x + 1 and player.pos.y == self.pos.y):
                    if not any(friend.pos.x == self.pos.x + 1 and friend.pos.y == self.pos.y for friend in enemies):
                        self.pos.x += 1

    def attack_player(self, player):
        player.take_damage(self.damage)
        print(f"Враг нанёс вам {self.damage} урона! У вас осталось {player.hp:.0f} HP.")