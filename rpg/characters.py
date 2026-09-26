
class Character:
    def __init__(self, name, max_health, attack_power):
        pass
    
    def take_damage(self, amount):
        pass
    
    def attack(self, target):
        pass
    
    def is_alive(self):
        return True


class Hero(Character):
    def __init__(self, name, max_health, attack_power):
        super().__init__(name, max_health, attack_power)
    
    def use_item(self, item):
        pass


class Enemy(Character):
    def __init__(self, name, max_health, attack_power, reward=None):
        super().__init__(name, max_health, attack_power)
        pass
