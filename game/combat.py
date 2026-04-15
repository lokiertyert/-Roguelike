def find_closest_enemy(player, enemies):
    if not enemies:
        return None, None
    closest = None
    min_dist = float("inf")
    for enemy in enemies:
        dist = abs(enemy.pos.x - player.pos.x) + abs(enemy.pos.y - player.pos.y)
        if dist < min_dist:
            min_dist = dist
            closest = enemy
    return closest, min_dist


def enemies_attack_nearby(player, enemies):
    for enemy in enemies:
        dx = abs(enemy.pos.x - player.pos.x)
        dy = abs(enemy.pos.y - player.pos.y)
        if (dx == 1 and dy == 0) or (dx == 0 and dy == 1):
            enemy.attack_player(player)
            if player.hp <= 0:
                return False
    return True
