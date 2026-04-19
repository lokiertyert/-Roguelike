import random


class Pole:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = []
        for i in range(height):
            row = []
            for j in range(width):
                if i == 0 or j == 0 or i == height - 1 or j == width - 1:
                    row.append("◻ ")
                else:
                    row.append("  ")
            self.matrix.append(row)


def brick_swap(current_pole):
    t_width = current_pole.width
    t_height = current_pole.height
    
    for x1 in range(1, t_width):
        quality_swaps = 0
        for y1 in range(1, t_height):
            if x1%2 == 0 and y1%2==0 and random.randint(1,2) == 2:
               current_pole.matrix[y1][x1] = "◻ "
               quality_swaps += 1
        for y1 in range(1, t_height-1):
            if current_pole.matrix[y1-1][x1] == "◻ " and current_pole.matrix[y1][x1] == "  " and current_pole.matrix[y1+1][x1] == "◻ ":
                current_pole.matrix[y1][x1] = "◻ "
                quality_swaps += 1
        if quality_swaps == t_height-2:
            r_dig = random.randint(1,t_height-2)
            current_pole.matrix[r_dig][x1] = "  "
        