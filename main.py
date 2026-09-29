
import argparse

from rpg.game import Game
from rpg.characters import Hero, Enemy
from rpg.items import Weapon, Potion
from rpg.quests import Quest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lex-RPG - a small text adventure.")
    parser.add_argument("-d", "--demo", action="store_true", dest="demo",
                        help="run the automatic demo instead of interactive play")
    return parser.parse_args()


def build_game(interactive: bool) -> Game:
    hero = Hero("Arthur Dent", max_health=30, attack_power=5)
    hero.pick_up(Potion("Health Potion", heal_amount=10))
    goblin = Enemy("Goblin", max_health=15, attack_power=4, 
                   reward=Weapon("Rusty Sword", damage_bonus=3))
    quest = Quest("Defeat the goblin threatening the village")
    
    return Game(hero, [goblin], quest, interactive=interactive)


def main() -> None:
    print(f"Running {__name__} game...")
    args = parse_args()
    game = build_game(interactive=not args.demo)
    game.run()
    print(f"Finishing game({game.hero},", 
          f"{[str(e) for e in game.enemies]},", 
          f"{game.quest.description[:20]}..., Completed: {game.quest.is_complete()})")


if __name__ == "__main__":
    main()
