from .base import Person
import random

class Enemy(Person):
    def __init__(self, id=0, pos=None, damage=0, hp=0, exp = 0, cost = 0, icon="  "):
        super().__init__(pos, damage, hp, exp)
        self.id = id
        self.icon = icon
        self.cost = cost

    def Enemies_AI(self, pole, player, enemies):
        start_x, start_y = self.pos.x, self.pos.y
        target_x, target_y = player.pos.x, player.pos.y
        queue = [(start_y, start_x)]
        visited = {(start_y, start_x): None}

        blocked = set()
        for e in enemies:
            if e != self:
                blocked.add((e.pos.y, e.pos.x))


        while queue:
            sy, sx = queue.pop(0)

            vertex = [(sx, sy-1),(sx, sy+1),(sx-1, sy),(sx+1, sy)]

            for nx, ny in vertex:
                if not(0 <= nx < pole.width and 0 <= ny < pole.height):
                    continue
                if pole.matrix[ny][nx] == "◻ ":
                    continue
                if (ny, nx) in blocked:
                    continue
                if (ny, nx) in visited:
                    continue 

                visited[(ny, nx)] = (sy, sx)

                if nx == target_x and ny == target_y:
                    path = []
                    curr = (ny, nx)
                    while curr is not None:
                        path.append(curr)
                        curr = visited[curr] 

                    if len(path) >= 2:
                        return path[-2]

                
                queue.append((ny, nx))

        return None


    def move_ai(self, pole, player, enemies):
        next_step = self.Enemies_AI(pole, player, enemies)

        if next_step is None:
            return
        
        next_y, next_x = next_step

        if not (0 <= next_x < pole.width and 0 <= next_y < pole.height):
            return
        if pole.matrix[next_y][next_x] == "◻ ":
            return
        if player.pos.x == next_x and player.pos.y == next_y:
            return
        for friend in enemies:
            if friend != self and friend.pos.x == next_x and friend.pos.y == next_y:
                return

        self.pos.x = next_x
        self.pos.y = next_y

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


def move_tw(p,b, enemies):
         for enemy in enemies:
            a = random.randint(1, 5)
            if a == 1:
                enemy.move(random.choice(["w", "a", "s", "d"]), p, b, enemies)
            else:
                enemy.move_ai(p, b, enemies)