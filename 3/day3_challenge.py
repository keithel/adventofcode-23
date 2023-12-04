import sys
from os.path import exists
from typing import Optional
import functools

default_input_filepath = "3/input.txt"


def line_symbol_indices(line: str) -> list[int]:
    line = line.strip()
    sym_poses: list[int] = [pos for pos, c in enumerate(line) if c != "." and not c.isdigit()]
    return sym_poses

"""
Arguments:
    prior_line_symbol_indices: The indices of symbols in the prior line
    prior_line_numbers: A list of tuples of:
        A number in the prior line that was not detected to be a part,
        The start index (inclusive) of the number,
        The end index (exclusive) of the number
    line: A line in the schematic

Returns a tuple of:
    A list of symbol indices
    A list of optional tuples that contain a non-part number in the current line and the number
        start (inclusive) and end (exclusive) indices
    A list of part numbers (successfully identified as parts)
"""
def line_parts(prior_line_symbol_indices: list[int],
               prior_line_numbers: list[Optional[tuple[int, int, int]]],
               line: str) -> tuple[list[int],
                                   list[Optional[tuple[int, int, int]]],
                                   list[int]]:
    parts: list[int] = []
    number_start_idx: Optional[int] = None
    #number_end_idx: Optional[int] = None
    cur_number: str = ""
    symbol_indices: list[int] = []
    line_numbers: list[Optional[tuple[int,int,int]]] = []

    def reset_cur_number():
        nonlocal number_start_idx, cur_number
        number_start_idx = None
        #number_end_idx = None
        cur_number = ""

    line = line.strip()
    for pos, c in enumerate(line):
        if c.isdigit():
            if not number_start_idx:
                number_start_idx = pos
            cur_number += c
        elif number_start_idx: # c not a digit and a number is being recognized
            if c != ".":
                parts.append(int(cur_number))
            else: # c == '.'
                # If we are at the end of the number and this isn't a symbol,
                for prior_line_symbol_index in prior_line_symbol_indices:
                    # -1 and +1 account for the diagonal positions.
                    if prior_line_symbol_index >= number_start_idx-1 and prior_line_symbol_index < pos+1:
                        parts.append(int(cur_number))
                        reset_cur_number()
                if symbol_indices and symbol_indices[-1] == number_start_idx-1:
                    parts.append(int(cur_number))
                    reset_cur_number()
            # if a number is still in progress (has not been reset), keep it in a list of
            # numbers in this line that have not yet been recognized as parts.
            if number_start_idx:
                line_numbers.append((int(cur_number), number_start_idx, pos))
                reset_cur_number()
        else: # c not a digit, no number in progress.
            # determine if any prior line numbers are parts.
            for i, prior in enumerate(prior_line_numbers):
                if not prior:
                    continue
                (prior_num, prior_start, prior_end) = prior
                for symbol_idx in symbol_indices:
                    if symbol_idx >= prior_start-1 and symbol_idx < prior_end+1:
                        parts.append(prior_num)
                        prior_line_numbers[i] = None
    return (symbol_indices, line_numbers, parts)


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

    parts: list[int] = []
    cur_parts: list[int] = []
    prior_line_symbol_indices: list[int] = []
    prior_line_numbers: list[Optional[tuple[int,int,int]]] = []
    for line in game_lines:
        (prior_line_symbol_indices, prior_line_numbers, cur_parts) = line_parts(prior_line_symbol_indices, prior_line_numbers, line)
        parts += cur_parts

    print(f"Parts: {parts}")
    print(f"Sum of all part numbers: {functools.reduce(lambda a,b: a+b, parts)}")
