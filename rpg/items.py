
class Item:
    def __init__(self, name):
        pass
    
    def use(self, user):
        pass


class Weapon(Item):
    def __init__(self, name, damage_bonus):
        super().__init__(name)
        pass
    
    def use(self, user):
        pass


class Potion(Item):
    def __init__(self, name, heal_amount):
        super().__init__(name)
        pass
    
    def use(self, user):
        pass
