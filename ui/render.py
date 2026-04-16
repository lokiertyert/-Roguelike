def draw(current_pole, player, enemies, heal_potions):
    for i in range(current_pole.height):
        for j in range(current_pole.width):
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
