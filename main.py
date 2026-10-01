
import argparse

from rpg.game import Game
from rpg.characters import Hero, Enemy
from rpg.items import Weapon, Potion
from rpg.locations import Location
from rpg.quests import Quest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lex-RPG - a small text adventure.")
    parser.add_argument("-d", "--demo", action="store_true", dest="demo",
                        help="run the automatic demo instead of interactive play")
    return parser.parse_args()


def build_locations() -> list[Location]:
    village = Location("Village Outskirts", "A quiet path leads out of the village.")
    forest = Location("Dark Forest", "Twisted trees block most of the light. Paths lead off in several directions.")
    cave = Location("Goblin Cave", "A damp cave, littered with bones.")
    bridge = Location("Old Bridge", "A rickety bridge creaks underfoot.")
    mill = Location("Abandoned Mill", "Broken machinery looms in the dark.")
    
    village.add_exit("north", forest, reciprocal="south")
    forest.add_exit("north", cave, reciprocal="south")
    forest.add_exit("east", bridge, reciprocal="west")
    bridge.add_exit("east", mill, reciprocal="west")
    
    cave.add_enemy(Enemy("Goblin", max_health=15, attack_power=4, 
                         reward=Weapon("Rusty Sword", damage_bonus=3)))
    mill.add_enemy(Enemy("Bandit", max_health=12, attack_power=6, 
                         reward=Weapon("Steel Sword", damage_bonus=6)))
    
    return [village, forest, cave, bridge, mill]


def build_game(interactive: bool) -> Game:
    hero = Hero("Arthur Dent", max_health=30, attack_power=5)
    hero.pick_up(Potion("Health Potion", heal_amount=10))
    locations = build_locations()
    hero.move_to(locations[0])
    quest = Quest("Goblin Threat", "Defeat the goblin threatening the village")
    
    return Game(hero, locations, quest, interactive=interactive)


def main() -> None:
    print(f"Running {__name__} game...")
    args = parse_args()
    game = build_game(interactive=not args.demo)
    game.run()
    print(f"Finishing game({game.hero},", 
          f"{[l.name for l in game.locations]},", 
          f"{game.quest.name}, Completed: {game.quest.is_complete()})")


if __name__ == "__main__":
    main()
