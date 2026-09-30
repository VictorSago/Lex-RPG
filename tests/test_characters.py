
import unittest

from rpg.characters import Character, Hero, Enemy
from rpg.items import Potion, Weapon
from rpg.locations import Location

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
    
    def test_effective_attack_power_defaults_to_attack_power(self):
        c = Character("Test", max_health=10, attack_power=6)
        self.assertEqual(c.effective_attack_power(), 6)


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
    
    def test_equip_sets_equipped_weapon(self):
        hero = Hero("Test", max_health=20, attack_power=5)
        sword = Weapon("Sword", damage_bonus=3)
        hero.equip(sword)
        self.assertIs(hero.equipped_weapon, sword)

    def test_effective_attack_power_includes_weapon_bonus(self):
        hero = Hero("Test", max_health=20, attack_power=5)
        hero.equip(Weapon("Sword", damage_bonus=3))
        self.assertEqual(hero.effective_attack_power(), 8)
        self.assertEqual(hero.attack_power, 5)      # base stays untouched
        
    def test_equipping_same_weapon_again_does_not_stack(self):
        hero = Hero("Test", max_health=20, attack_power=5)
        sword = Weapon("Sword", damage_bonus=3)
        hero.equip(sword)
        hero.equip(sword)
        self.assertEqual(hero.effective_attack_power(), 8)
            
    def test_equipping_a_different_weapon_replaces_the_bonus(self):
        hero = Hero("Test", max_health=20, attack_power=5)
        rusty = Weapon("Rusty Sword", damage_bonus=3)
        steel = Weapon("Steel Sword", damage_bonus=10)
        hero.equip(rusty)
        hero.equip(steel)
        self.assertEqual(hero.effective_attack_power(), 15)
        self.assertIs(hero.equipped_weapon, steel)
    
    def test_attack_uses_effective_attack_power(self):
        hero = Hero("Test", max_health=20, attack_power=5)
        hero.equip(Weapon("Sword", damage_bonus=3))
        target = Character("Target", max_health=20, attack_power=1)
        hero.attack(target)
        self.assertEqual(target.current_health, 12)     # 20 - (5 base + 3 bonus)
    
    def test_move_to_sets_location(self):
        hero = Hero("Link", max_health=20, attack_power=5)
        cave = Location("Cave", "A dark cave.")
        hero.move_to(cave)
        self.assertIs(hero.location, cave)


if __name__ == "__main__":
    unittest.main()
