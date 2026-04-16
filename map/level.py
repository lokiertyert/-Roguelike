from .pole import Pole, brick_swap

class Level:
    def __init__(self, number, width=18, height=50):
        self.number = number
        self.width = width
        self.height = height
        self.enemies_count = 4 + number
        self.heal_potions_count = 3 + (number - 1)
        self.required_kills = 5 * number  

    def create_level(self):
        pole = Pole(self.width, self.height)
        brick_swap(pole)
        return pole