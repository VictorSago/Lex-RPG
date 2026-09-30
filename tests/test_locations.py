
import unittest

from rpg.locations import Location
from rpg.characters import Enemy


class TestLocation(unittest.TestCase):
    def test_stores_name_and_description(self):
        loc = Location("Cave", "A dark, damp cave.")
        self.assertEqual(loc.name, "Cave")
        self.assertEqual(loc.description, "A dark, damp cave.")

    def test_starts_with_no_exits_or_enemies(self):
        loc = Location("Cave", "A dark, damp cave.")
        self.assertEqual(loc.exits, {})
        self.assertEqual(loc.enemies, [])
    
    def test_add_enemy_appends_to_enemies(self):
        loc = Location("Cave", "A dark, damp cave.")
        goblin = Enemy("Goblin", max_health=10, attack_power=2)
        loc.add_enemy(goblin)
        self.assertIn(goblin, loc.enemies)

    def test_has_living_enemies_false_when_empty(self):
        loc = Location("Cave", "A dark, damp cave.")
        self.assertFalse(loc.has_living_enemies())

    def test_has_living_enemies_true_with_a_living_enemy(self):
        loc = Location("Cave", "A dark, damp cave.")
        loc.add_enemy(Enemy("Goblin", max_health=10, attack_power=2))
        self.assertTrue(loc.has_living_enemies())

    def test_has_living_enemies_false_when_all_dead(self):
        loc = Location("Cave", "A dark, damp cave.")
        goblin = Enemy("Goblin", max_health=10, attack_power=2)
        goblin.take_damage(999)
        loc.add_enemy(goblin)
        self.assertFalse(loc.has_living_enemies())

    def test_add_exit_sets_one_direction(self):
        a = Location("A", "...")
        b = Location("B", "...")
        a.add_exit("north", b)
        self.assertIs(a.exits["north"], b)
        self.assertNotIn("south", b.exits)

    def test_add_exit_with_reciprocal_links_both_directions(self):
        a = Location("A", "...")
        b = Location("B", "...")
        a.add_exit("north", b, reciprocal="south")
        self.assertIs(a.exits["north"], b)
        self.assertIs(b.exits["south"], a)


if __name__ == "__main__":
    unittest.main()
