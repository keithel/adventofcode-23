import sys
from os.path import exists

default_input_filepath = "3/input.txt"

"""
Part 1:
What is the sum of all of the part numbers in the engine schematic?
any number adjacent to a symbol, even diagonally, is a "part number" and should
be included in your sum. (Periods (.) do not count as a symbol.)
"""
if __name__=="__main__":
    game_lines = []
    input_filepath = sys.argv[1] if len(sys.argv) > 1 else default_input_filepath if exists(default_input_filepath) else None

    if input_filepath:
        with open(input_filepath, 'r') as f:
            game_lines = f.readlines()
    else:
        game_lines = sys.stdin.readlines()
