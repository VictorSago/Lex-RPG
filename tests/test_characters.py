
import unittest

from rpg.characters import Character, Hero, Enemy
from rpg.items import Potion, Weapon

class TestCharacter(unittest.TestCase):
    def test_take_damage_reduces_current_health(self):
        c = Character("Test", max_health=20, attack_power=5)
        c.take_damage(6)
        self.assertEqual(c.current_health, 14)

    def test_take_damage_clamps_at_zero(self):
        c = Character("Test", max_health=10, attack_power=1)
        c.take_damage(999)
        self.assertEqual(c.current_health, 0)

    def test_is_alive_true_above_zero_health(self):
        c = Character("Test", max_health=10, attack_power=1)
        self.assertTrue(c.is_alive())

    def test_is_alive_false_at_zero_health(self):
        c = Character("Test", max_health=10, attack_power=1)
        c.take_damage(10)
        self.assertFalse(c.is_alive())

    def test_heal_increases_current_health(self):
        c = Character("Test", max_health=20, attack_power=1)
        c.take_damage(10)
        c.heal(4)
        self.assertEqual(c.current_health, 14)

    def test_heal_clamps_at_max_health(self):
        c = Character("Test", max_health=20, attack_power=1)
        c.take_damage(5)
        c.heal(999)
        self.assertEqual(c.current_health, 20)

    def test_attack_damages_target_by_attack_power(self):
        attacker = Character("Attacker", max_health=10, attack_power=7)
        target = Character("Target", max_health=20, attack_power=1)
        attacker.attack(target)
        self.assertEqual(target.current_health, 13)


class TestHero(unittest.TestCase):
    def test_starts_with_empty_inventory(self):
        hero = Hero("Link", max_health=20, attack_power=5)
        self.assertEqual(hero.inventory, [])

    def test_pick_up_adds_item_to_inventory(self):
        hero = Hero("Link", max_health=20, attack_power=5)
        potion = Potion("Health Potion", heal_amount=5)
        hero.pick_up(potion)
        self.assertIn(potion, hero.inventory)

    def test_use_item_not_in_inventory_raises(self):
        hero = Hero("Link", max_health=20, attack_power=5)
        potion = Potion("Health Potion", heal_amount=5)
        with self.assertRaises(ValueError):
            hero.use_item(potion)

    def test_use_item_removes_consumable(self):
        hero = Hero("Link", max_health=20, attack_power=5)
        potion = Potion("Health Potion", heal_amount=5)
        hero.pick_up(potion)
        hero.use_item(potion)
        self.assertNotIn(potion, hero.inventory)

    def test_use_item_keeps_non_consumable(self):
        hero = Hero("Link", max_health=20, attack_power=5)
        sword = Weapon("Sword", damage_bonus=3)
        hero.pick_up(sword)
        hero.use_item(sword)
        self.assertIn(sword, hero.inventory)


if __name__ == "__main__":
    unittest.main()
