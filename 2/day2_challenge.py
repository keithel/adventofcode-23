import sys
import functools as t
from os.path import exists

default_input_filepath = "2/input.txt"
s_max_rgb_cubes = {"red": 12, "green": 13, "blue": 14 }

def is_handful_possible(handful: list[str]) -> bool:
    for color_count in handful:
        (cube_count, cube_color) = color_count.split(maxsplit=1)
        if int(cube_count) > s_max_rgb_cubes[cube_color]:
            return False
    return True


def is_game_possible(all_handfuls : str) -> int:
    default_seen = {"red": False, "green": False, "blue": False}
    seen = default_seen.copy()

    handfuls = all_handfuls.split(';')
    for handful in handfuls:
        cube_tokens = handful.strip().split(',')
        if not is_handful_possible(cube_tokens):
            return False
    return True

def minimum_cubes(all_handfuls: str):
    min_rgb_cubes = {"red": 0, "green": 0, "blue": 0}
    handfuls = all_handfuls.split(';')
    for handful in handfuls:
        cube_tokens = handful.strip().split(',')
        color_counts = {cube_token.split()[1]: int(cube_token.split()[0]) for cube_token in cube_tokens}
        for color in color_counts:
            if color_counts[color] > min_rgb_cubes[color]:
                min_rgb_cubes[color] = color_counts[color]
    return min_rgb_cubes.values()


def game_power(min_rgb_cubes : list[int]) -> int:
    return t.reduce(lambda a,b: a*b, min_rgb_cubes)

"""
Part 1:
Determine which games would have been possible if the bag had been loaded with
only 12 red cubes, 13 green cubes, and 14 blue cubes.
What is the sum of the IDs of those games?

Part 2:
For each game, find the minimum set of cubes that must have been present.
What is the sum of the power of these sets?

The power of a set of cubes is equal to the numbers of red, green, and blue
cubes multiplied together.
"""
if __name__=="__main__":
    game_lines = []
    input_filepath = sys.argv[1] if len(sys.argv) > 1 else default_input_filepath if exists(default_input_filepath) else None

    if input_filepath:
        with open(input_filepath, 'r') as f:
            game_lines = f.readlines()
    else:
        game_lines = sys.stdin.readlines()

    sum_possible_games = 0
    sum_game_powers = 0
    for i, line in enumerate(game_lines):
        tokens = line.split(":")
        if tokens[0] != f"Game {i+1}":
            print(f"Unexpected game {tokens[1]}!")
            break
        possible = False
        if is_game_possible(tokens[1]):
            possible = True
            sum_possible_games += i+1

        # Part 2
        sum_game_powers += game_power(minimum_cubes(tokens[1]))

    print(sum_possible_games)
    print(sum_game_powers)
