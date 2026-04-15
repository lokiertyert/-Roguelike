import random


class Pole:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = []
        for i in range(width):
            row = []
            for j in range(height):
                if i == 0 or j == 0 or i == width - 1 or j == height - 1:
                    row.append("◻ ")
                else:
                    row.append("  ")
            self.matrix.append(row)


def brick_swap(current_pole):
    t_width = current_pole.width
    t_height = current_pole.height
    quality_swaps = t_width * t_height // 4
    for i in range(quality_swaps):
        x1 = random.randint(1, t_width - 2)
        y1 = random.randint(1, t_height - 2)
        current_pole.matrix[x1][y1] = "◻ "
