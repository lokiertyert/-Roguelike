from .base import items


class heal_potion(items):
    def __init__(self, pos=None, id=0):
        self.pos = pos
        self.id = id
        super().__init__(
            name="Зелье здоровья",
            description="Восстанавливает 25% от максимального здоровья",
            icon="💗"
        )

    def use(self, target):
        heal_amount = target.max_hp * 0.25
        target.hp = min(target.hp + heal_amount, target.max_hp)
        return heal_amount
