class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Person:
    def __init__(self, pos=None, damage=0, hp=0):
        self.pos = pos
        self.damage = damage
        self.hp = hp
        self.max_hp = hp

    def take_damage(self, amount):
        """РџРѕР»СѓС‡РёС‚СЊ СѓСЂРѕРЅ. Р’РѕР·РІСЂР°С‰Р°РµС‚ True, РµСЃР»Рё РїРµСЂСЃРѕРЅР°Р¶ РµС‰С‘ Р¶РёРІ."""
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        return self.hp > 0
