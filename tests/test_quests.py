
import unittest

from rpg.quests import Quest


class TestQuest(unittest.TestCase):
    def test_stores_name(self):
        quest = Quest("Goblin Threat", "Defeat the goblin")
        self.assertEqual(quest.name, "Goblin Threat")

    def test_stores_description(self):
        quest = Quest("Goblin Threat", "Defeat the goblin")
        self.assertEqual(quest.description, "Defeat the goblin")

    def test_starts_incomplete(self):
        quest = Quest("Goblin Threat", "Defeat the goblin")
        self.assertFalse(quest.is_complete())

    def test_complete_marks_it_complete(self):
        quest = Quest("Goblin Threat", "Defeat the goblin")
        quest.complete()
        self.assertTrue(quest.is_complete())

    def test_complete_twice_stays_complete(self):
        quest = Quest("Goblin Threat", "Defeat the goblin")
        quest.complete()
        quest.complete()
        self.assertTrue(quest.is_complete())


if __name__ == "__main__":
    unittest.main()
