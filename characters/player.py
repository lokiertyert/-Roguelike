import os
from .base import Person
from utils.input import read_key, wait_key

class Player(Person):
    def __init__(self, name=None, pos=None, damage=25, hp=100, money=0, exp = 0, exp_need = 80, lvl = 1, icon="🐥"):
        super().__init__(pos, damage, hp, exp)
        self.name = name
        self.money = money
        self.icon = icon
        self.lvl = lvl
        self.exp_need = exp_need
        self.inventory = []

    def move(self, input_key, pole, heal_potions, enemies):
        old_x, old_y = self.pos.x, self.pos.y

        if (input_key == "w" or input_key == "ц") and self.pos.y > 0:
            if pole.matrix[self.pos.y - 1][self.pos.x] != "◻ ":
                can_move = True
                for enemy in enemies:
                    if enemy.pos.x == self.pos.x and enemy.pos.y == self.pos.y - 1:
                        can_move = False
                        break
                if can_move:
                    self.pos.y -= 1
                        
        elif (input_key == "s" or input_key == "ы") and self.pos.y < pole.height - 1:
            if pole.matrix[self.pos.y + 1][self.pos.x] != "◻ ":
                can_move = True
                for enemy in enemies:
                    if enemy.pos.x == self.pos.x and enemy.pos.y == self.pos.y + 1:
                        can_move = False
                        break
                if can_move:
                    self.pos.y += 1
                        
        elif (input_key == "a" or input_key == "ф") and self.pos.x > 0:
            if pole.matrix[self.pos.y][self.pos.x - 1] != "◻ ":
                can_move = True
                for enemy in enemies:
                    if enemy.pos.x == self.pos.x - 1 and enemy.pos.y == self.pos.y:
                        can_move = False
                        break
                if can_move:
                    self.pos.x -= 1
                        
        elif (input_key == "d" or input_key == "в") and self.pos.x < pole.width - 1:
            if pole.matrix[self.pos.y][self.pos.x + 1] != "◻ ":
                can_move = True
                for enemy in enemies:
                    if enemy.pos.x == self.pos.x + 1 and enemy.pos.y == self.pos.y:
                        can_move = False
                        break
                if can_move:
                    self.pos.x += 1


        collected_potions = []
        for potion in heal_potions[:]:
            if potion.pos.x == self.pos.x and potion.pos.y == self.pos.y:
                self.inventory.append(potion)
                collected_potions.append(potion)
        for potion in collected_potions:
            heal_potions.remove(potion)

    