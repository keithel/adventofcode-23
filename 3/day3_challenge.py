import sys
from os.path import exists
from typing import Optional
import string
import functools

default_input_filepath = "3/input.txt"

def find_parts(lines: list[str]):
    if (len(lines) != 2):
        raise ValueError(f"lines does not have a length of 2: {len(lines)} \nlines:{lines}")

    parts: list[int] = []
    number_start_idx: Optional[int] = None
    cur_number = ""
    cur_number_is_part = False

    def reset_num(add_part: bool = False):
        nonlocal cur_number, number_start_idx, cur_number_is_part
        # if add_part and int(cur_number) not in parts:
        if add_part:
            parts.append(int(cur_number))
        number_start_idx = None
        cur_number = ""
        cur_number_is_part = False

    nonspecial_chars = string.digits + '.'

    for i, c in enumerate(lines[1]):
        match c:
            case '0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9':
                cur_number += c
                if not number_start_idx:
                    number_start_idx = i
                    # look behind cur char to see if special char.
                    # Mark num as part if so.
                    if lines[1][i-1] not in (nonspecial_chars):
                        cur_number_is_part = True

            case '.':
                if cur_number:
                    if cur_number_is_part:
                        reset_num(True)
                    else:
                        # Look in prior line to see if it is a part
                        is_part = False
                        for pc in lines[0][number_start_idx-1:number_start_idx+len(cur_number)+1]:
                            if pc not in nonspecial_chars:
                                is_part = True
                                break
                        reset_num(is_part)
            case _:
                if cur_number:
                    reset_num(True)
                else:
                    if lines[1][i+1] in string.digits:
                        # The next char coming up is a number and the current char is a special
                        # char, so indicate that the next number will be a part.
                        cur_number_is_part = True
                    # Look in prior line to see if there are any adjacent numbers, add them as parts.
                    for j, pc in enumerate(lines[0][i-1:i+2]):
                        j += i-1
                        if pc in string.digits:
                            cur_number = pc
                            for k in range(j-1, -1, -1):
                                if not lines[0][k] in string.digits:
                                    break
                                cur_number = lines[0][k] + cur_number
                            for k in range(j+1, len(lines[0])):
                                if not lines[0][k] in string.digits:
                                    break
                                cur_number += lines[0][k]
                        if cur_number:
                            reset_num(True)
                            break
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

    parts_lists = [ find_parts(game_lines[i:i+2]) for i in range(0, len(game_lines)-1)]
    parts = [ part for line_parts in parts_lists for part in line_parts]
    #parts = { part : None for line_parts in parts_lists for part in line_parts}

    show_lines = (len(game_lines)-2, len(game_lines))
    for i in range(len(game_lines)):
        print(f"Game line {i}: {game_lines[i]}")
        print(f"Game line {i} parts: {parts_lists[i-1]}")

    sum_parts = functools.reduce(lambda a,b: a+b, parts)
    print(f"Sum of parts: {sum_parts}")
