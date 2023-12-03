import sys
import functools as t

s_max_rgb_cubes = {"red": 12, "green": 13, "blue": 14 }

def is_handful_possible(handful: dict[str:bool]) -> bool:
    for color in handful:
        if handful[color] > s_max_rgb_cubes[color]:
            return False
    return True

def is_game_possible(all_trials : str) -> int:
    default_seen = {"red": False, "green": False, "blue": False}
    seen = default_seen.copy()
    handful = {}

    cube_tokens = all_trials.split(",")
    for cube_token in cube_tokens:
        (cube_count, cube_color) = cube_token.split(maxsplit = 1)
        for (color, has_been_seen) in seen.items():
            if cube_color != color:
                continue
            if has_been_seen:
                if not is_handful_possible(handful):
                    return False
                handful = {}
                seen = default_seen.copy()
            handful[cube_color] = int(cube_count)
            seen[color] = True

    return True


"""
Determine which games would have been possible if the bag had been loaded with
# only 12 red cubes, 13 green cubes, and 14 blue cubes.
# What is the sum of the IDs of those games?
"""
if __name__=="__main__":
    if len(sys.argv)>1:
        with open(sys.argv[1],'r') as f:
            game_lines = f.readlines()
    else:
        game_lines = sys.stdin.readlines()

    sum_possible_games = 0
    for i, line in enumerate(game_lines):
        tokens = line.split(":")
        if tokens[0] != f"Game {i+1}":
            print(f"Unexpected game {tokens[1]}!")
            break
        possible = False
        if is_game_possible(tokens[1]):
            possible = True
            sum_possible_games += i+1
        print(f"Game {tokens[0]} {'not ' if not possible else ''}possible")

        print(sum_possible_games)
