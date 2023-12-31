from __future__ import annotations
import sys
from os.path import exists
from typing import Optional, Union
import string
import functools

DEBUG: bool = False
default_input_filepath: str = "3/input.txt"

class Schematic_Item:
    def __init__(self, row: int, col: int, item: Union[int, str]) -> None:
        self._row: int = row
        self._col: int = col
        self._number: Optional[int] = None
        self._symbol: Optional[str] = None

        try:
            self._number = int(item)
        except ValueError as e:
            if not "invalid literal" in str(e):
                raise
            self._symbol = item
        self._part = False

    def row(self) -> int:
        return self._row

    def col(self) -> int:
        return self._col

    def number(self) -> Optional[int]:
        return self._number

    def symbol(self) -> Optional[str]:
        return self._symbol

    def isnumber(self) -> bool:
        return bool(self._number)

    def issymbol(self) -> bool:
        return bool(self._symbol)

    def ispart(self) -> bool:
        return self._part

    def len(self) -> int:
        if self._symbol:
            return 1
        return len(str(self._number))

    def __str__(self) -> str:
        return f"SchematicItem: ({self._row},{self._col}) {'' if self.issymbol() else 'part' if self.ispart() else 'number'} {self._number if self.isnumber() else self._symbol}"

    def __repr__(self) -> str:
        return self.__str__()

    def part_number(self) -> Optional[int]:
        return self._number if self._part else None

    def gear_ratio(self, prev_to_next_line_item_dicts: list[dict[tuple[int, int], Schematic_Item]]) -> int:
        num_items: list[int] = []
        for r in range(3):
            for c in range(self._col + 2):
                try:
                    item = prev_to_next_line_item_dicts[r][(self._row-1+r,c)]
                    if not item.isnumber():
                        continue
                    for d in range(self._row-1, self._row+2):
                        if d >= item.col() and d < item.col() + item.len():
                            num_items.append(item.number())
                except KeyError:
                    # We will get this if the row+column entry in the dict doesn't exist
                    # in that case we just want to continue on to the next.
                    pass
                except IndexError:
                    # We will get this when subscripting prev_.. with r==3 at the end of the file/data.
                    # It's ok to just skip this.
                    pass

        # Return 0 if there aren't exactly 2 adjacent numbers, otherwise return the two multiplied together.
        return num_items[0] * num_items[1] if len(num_items) == 2 else 0

    def mark_as_part(self, value: bool = True) -> None:
        if self._symbol:
            raise AttributeError(f"Cannot mark a symbol as a part: ({self._row}, {self._col}) symbol {self._symbol}")
        self._part = True


def find_parts(prev_line_num: int, prev_line: str, line:str) -> dict[tuple[int, int], Schematic_Item]:
    line_num: int = prev_line_num+1

    items: dict[tuple[int, int], Schematic_Item] = {}
    parts: dict[tuple[int, int], int] = {}
    number_start_idx: Optional[int] = None
    cur_number = ""

    def mark_part_and_reset(mp_line_num: int):
        nonlocal items, number_start_idx, cur_number
        items[(mp_line_num, number_start_idx)].mark_as_part()
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
            items[(line_num, number_start_idx)] = Schematic_Item(line_num, number_start_idx, cur_number)
            # look behind num start char and after num end char to see if
            # there is a special char. Add num as a part.
            if (line[number_start_idx-1] not in nonspecial_chars
                or line[i] not in nonspecial_chars):
                mark_part_and_reset(line_num)
                continue
            # Look in prior line to see if it is a part
            for pc in prev_line[number_start_idx-1:number_start_idx+len(cur_number)+1]:
                if pc not in nonspecial_chars:
                    items[(line_num, number_start_idx)] = Schematic_Item(line_num, number_start_idx, cur_number)
                    mark_part_and_reset(line_num)
                    break
            i -= 1
        elif line[i] != '.':
            items[(line_num, i)] = Schematic_Item(line_num, i, line[i])
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
                    items[(prev_line_num, number_start_idx)] = Schematic_Item(prev_line_num, number_start_idx, cur_number)
                    mark_part_and_reset(prev_line_num)
                j += 1
        i += 1
    return items

def get_solutions(infile : str):
    solutions: list[int] = []
    solution_fnsuffix: str = ".solution"
    solution_filepath: Optional[str] = input_filepath + solution_fnsuffix if exists(str(input_filepath) + ".solution") else None
    if solution_filepath:
        with open(solution_filepath, 'r') as f:
            solution_lines: list[str] = f.readlines()
            expected_solfile_content_msg = (
                 "            Only 1 or 2 lines expected, with single integer solution on each line.\n"
                 "            A '# comment' after the solution on each line is also acceptable.")

            if len(solution_lines) < 1 or len(solution_lines) > 2:
                raise ValueError(f"Solutions file {solution_filepath} does not look like a solution file.\n"
                    f"{expected_solfile_content_msg}")
            for lineno, solutionLine in enumerate(solution_lines):
                tokens: list[str] = solutionLine.split(maxsplit=1)
                if len(tokens) > 1 and tokens[1][0] != "#":
                    raise ValueError(f"Solutions file {solution_filepath} line {lineno} has unexpected content.\n"
                        f"{expected_solfile_content_msg}")
                solutions.append(int(tokens[0]))
    return solutions

def find_stars(line_item_dicts: list[dict[tuple[int, int], Schematic_Item]]) -> list[Schematic_Item]:
    #star_items: list[Schematic_Item] = []
    #for l, item_dict in enumerate(line_item_dicts):
    #    print(f"line {l} stars: {[item for item in item_dict.values() if item.symbol() == '*']}")
    star_items: list[Schematic_Item] = [item for item_dict in line_item_dicts for item in item_dict.values() if item.symbol() == "*"]
    return star_items

def sum_gear_ratios(line_item_dicts: list[dict[tuple[int, int], Schematic_Item]]): # -> int:
    def sum_gears(a: Union[Schematic_Item, int], b: Union[Schematic_Item, int]) -> int:
        gear_ratios: list[int] = []
        for n in [a, b]:
            gear_ratio = 0
            if type(n) == Schematic_Item:
                gear_ratio = n.gear_ratio(line_item_dicts[n.row()-1:n.row()+2])
            else:
                gear_ratio = n
            gear_ratios.append(gear_ratio)
        return functools.reduce(lambda a,b:a+b, gear_ratios)

    stars: list[Schematic_Item] = find_stars(line_item_dicts)
    print(f"stars: {stars}")
    gear_sum = [functools.reduce(sum_gears, stars)]
    return gear_sum

"""
Part 1:
What is the sum of all of the part numbers in the engine schematic?
any number adjacent to a symbol, even diagonally, is a "part number" and should
be included in your sum. (Periods (.) do not count as a symbol.)
"""
if __name__=="__main__":
    game_lines: list[str] = []
    input_filepath: Optional[str] = sys.argv[1] if len(sys.argv) > 1 else default_input_filepath if exists(default_input_filepath) else None

    if input_filepath:
        with open(input_filepath, 'r') as f:
            game_lines = f.readlines()
    else:
        game_lines = sys.stdin.readlines()

    solutions: list[int] = get_solutions(input_filepath)

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

    schematicitems_dicts: list[dict[tuple[int, int], Schematic_Item]] = [ find_parts(i, game_lines[i], game_lines[i+1]) for i in range(0, len(game_lines)-1)]
    schematicitems_dict: dict[tuple[int, int], int] = functools.reduce(lambda a,b: a|b, schematicitems_dicts)
    schematicitems: list[Schematic_Item] = schematicitems_dict.values()

    if DEBUG:
        for i in range(len(game_lines)):
            print(f"Game line {str(i).zfill(3)}: {game_lines[i]}")
            if i > 0:
                line_item_dict = schematicitems_dicts[i-1]
                print(f"Game line {i} parts: {[item.part_number() for item in line_item_dict.values() if item.ispart()]}")

    def add_list_SchematicItem_by_part_number(a: Union[Schematic_Item, int],
                                              b: Union[Schematic_Item, int]):
        partnums: list[int] = []
        for n in [a, b]:
            part_number = 0
            if type(n) == Schematic_Item:
                part_number = n.number() if n.ispart() else 0
            else:
                part_number = n
            partnums.append(part_number)
        return functools.reduce(lambda a,b:a+b, partnums)

    if DEBUG:
        print(f"schematicitems parts: {[schematicitem.part_number() for schematicitem in schematicitems if schematicitem.ispart()]}")
    sum_parts = functools.reduce(add_list_SchematicItem_by_part_number, schematicitems)

    print(f"Sum of parts: {sum_parts}")
    if solutions and solutions[0]:
        assert(sum_parts == solutions[0])
        print(f"Expected solution is {solutions[0]}, solution verified.")

    print(f"Part 2, sum of gear ratios")
    print(f"Sum of all gear ratios: {sum_gear_ratios(schematicitems_dicts)}")
    # Not the answer: 5386663