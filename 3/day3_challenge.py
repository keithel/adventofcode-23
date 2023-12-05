import sys
from os.path import exists
from typing import Optional
import string
import functools

default_input_filepath = "3/input.txt"

def find_parts(prev_line_num: int, prev_line: str, line:str) -> dict[tuple[int, int], int]:
    line_num: int = prev_line_num+1
    parts: dict[tuple[int, int], int] = {}
    number_start_idx: Optional[int] = None
    cur_number = ""

    def add_part_and_reset(line_num: int):
        nonlocal number_start_idx, cur_number
        parts[(line_num, number_start_idx)] = int(cur_number)
        number_start_idx = None
        cur_number = ""

    nonspecial_chars = string.digits + '.'

    i = 0
    while i < len(line):
        if line[i].isdigit():
            number_start_idx = i
            cur_number = line[i]
            i += 1
            while line[i].isdigit():
                cur_number += line[i]
                i += 1
            # look behind num start char and after num end char to see if
            # there is a special char. Add num as a part.
            if (line[number_start_idx-1] not in nonspecial_chars
                or line[i] not in nonspecial_chars):
                add_part_and_reset(line_num)
                continue
            # Look in prior line to see if it is a part
            for pc in prev_line[number_start_idx-1:number_start_idx+len(cur_number)+1]:
                if pc not in nonspecial_chars:
                    parts[(line_num, number_start_idx)] = int(cur_number)
                    add_part_and_reset(line_num)
                    break
            i -= 1
        elif line[i] != '.':
            # Look in prior line to see if there are any adjacent numbers, add them as parts.
            j = i-1
            while j < i+2:
                cur_number: str = ""
                pc = prev_line[j]
                if pc in string.digits:
                    number_start_idx: int = j
                    cur_number = pc
                    for k in range(j-1, -1, -1):
                        if not prev_line[k] in string.digits:
                            break
                        number_start_idx = k
                        cur_number = prev_line[k] + cur_number
                    for k in range(j+1, len(prev_line)):
                        if not prev_line[k] in string.digits:
                            break
                        cur_number += prev_line[k]
                        j = k
                if cur_number:
                    parts[(prev_line_num, number_start_idx)] = int(cur_number)
                    add_part_and_reset(prev_line_num)
                j += 1
        i += 1
    return parts


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
        game_lines: list[str] = sys.stdin.readlines()

    if not game_lines:
        print("0 parts")
        sys.exit(1)

    # To reduce corner cases, strip the line (get rid of newline), and add '.' to the front and
    # back, so that looking for the diagonals is easier (no need to check if diagonal would be
    # before the beginning or after the end of the prior line string)
    game_lines = ["." + line.strip() + '.' for line in game_lines]

    # To make first line processing not special cased, prepend the game_lines read in with a line
    # that contains only `.`s (so, no numbers or special characters), then start on the second line.
    game_lines.insert(0, "." * len(game_lines[0]))

    parts_dicts: list[dict[tuple[int, int], int]] = [ find_parts(i, game_lines[i], game_lines[i+1]) for i in range(0, len(game_lines)-1)]
    parts_dict: dict[tuple[int, int], int] = functools.reduce(lambda a,b: a|b, parts_dicts)
    parts = parts_dict.values()

    show_lines = (len(game_lines)-2, len(game_lines))
    for i in range(len(game_lines)):
        print(f"Game line {i}: {game_lines[i]}")
        if i > 0:
            print(f"Game line {i} parts: {parts_dicts[i-1]}")

    print(parts_dict)
    sum_parts = functools.reduce(lambda a,b: a+b, parts)

    print(f"parts_dicts[{len(parts_dicts)-1}]: {parts_dicts[len(parts_dicts)-1]}")
    print(f"Sum of parts: {sum_parts}")
