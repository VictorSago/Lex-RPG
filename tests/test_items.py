
import unittest

from rpg.characters import Character, Hero
from rpg.items import Weapon, Potion


class TestWeapon(unittest.TestCase):
    def test_is_not_consumable(self):
        sword = Weapon("Sword", damage_bonus=3)
        self.assertFalse(sword.consumable)

    def test_healing_value_is_zero(self):
        sword = Weapon("Sword", damage_bonus=3)
        self.assertEqual(sword.healing_value(), 0)
    
    def test_use_increases_heros_attack_power(self):
        hero = Hero("Test", max_health=20, attack_power=5)
        sword = Weapon("Sword", damage_bonus=3)
        sword.use(hero)
        self.assertEqual(hero.effective_attack_power(), 8)
    
    def test_use_on_a_plain_character_does_nothing(self):
        # Confirms the harmless default: a Character that can't equip is unaffected.
        character = Character("Test", max_health=20, attack_power=5)
        sword = Weapon("Sword", damage_bonus=3)
        sword.use(character)
        self.assertEqual(character.effective_attack_power(), 5)


class TestPotion(unittest.TestCase):
    def test_use_heals_user(self):
        user = Character("Test", max_health=20, attack_power=1)
        user.take_damage(10)
        potion = Potion("Health Potion", heal_amount=6)
        potion.use(user)
        self.assertEqual(user.current_health, 16)
    
    def test_use_does_not_heal_beyond_max_health(self):
        user = Character("Test", max_health=20, attack_power=1)
        user.take_damage(3)  # at 17/20
        potion = Potion("Health Potion", heal_amount=999)
        potion.use(user)
        self.assertEqual(user.current_health, 20)

    def test_is_consumable(self):
        potion = Potion("Health Potion", heal_amount=6)
        self.assertTrue(potion.consumable)

    def test_healing_value_matches_heal_amount(self):
        potion = Potion("Health Potion", heal_amount=6)
        self.assertEqual(potion.healing_value(), 6)


if __name__ == "__main__":
    unittest.main()
