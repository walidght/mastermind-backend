import itertools
import random

from game import generate_feedback


# the [index] position is [color]
# the [index] position is not [color]
# there is [color] in the code
# there is not [color] in the code
# there are [number] times the color [color]

GREEN = 0
YELLOW = 1
BLUE = 2
RED = 3
BLACK = 4
WHITE = 5

COLORS = {
    "1": 'green',
    "2": 'yellow',
    "3": 'blue',
    "4": 'red',
    "5": 'black',
    "6": 'white',
    0: 'green',
    1: 'yellow',
    2: 'blue',
    3: 'red',
    4: 'black',
    5: 'white'
}


def get_complementary(possibles):
    complementary = set()
    for color in ['1', '2', '3', '4', '5', '6']:
        if color not in possibles:
            complementary.add(color)

    return complementary


def count_frequency(code, color):
    count = 0
    for i in code:
        if i == color:
            count += 1
    return count


def get_hints_in_nl(born_inf, born_sup, possibles_per_position):
    hints = []
    for i, (born_i, born_s) in enumerate(zip(born_inf, born_sup)):
        if born_i == born_s and born_s != 0:
            hints.append(f"2there is exactly {born_i} {COLORS[i]}")
            continue
        if born_i > 0:
            hints.append(f"6there is at least {born_i} {COLORS[i]}")
        if born_s == 0:
            hints.append(f"5there is no {COLORS[i]}")
        elif born_s < 4:
            hints.append(f"7there is at most {born_s} {COLORS[i]}")
    for position in range(4):
        if len(possibles_per_position[position]) == 6:
            continue
        elif len(possibles_per_position[position]) == 1:
            hints.append(
                f"1position {position + 1} is {COLORS[possibles_per_position[position].pop()]}")
        elif len(possibles_per_position[position]) > 3:
            hints.append(
                f"4position {position + 1} is not {', '.join([COLORS[color] for color in get_complementary(possibles_per_position[position])])}")
        else:
            hints.append(
                f"3position {position + 1} can be {', '.join([COLORS[color] for color in possibles_per_position[position]])}")
            
    return [hint[1:] for hint in sorted(hints)]


def print_hints(born_inf, born_sup, possibles_per_position):
    for i, (born_i, born_s) in enumerate(zip(born_inf, born_sup)):
        if born_i == born_s and born_s != 0:
            print(f"there is exactly {born_i} {COLORS[i]}")
            continue
        if born_i > 0:
            print(f"there is at least {born_i} {COLORS[i]}")
        if born_s == 0:
            print(f"there is no {COLORS[i]}")
        elif born_s < 4:
            print(f"there is at most {born_s} {COLORS[i]}")
    for position in range(4):
        if len(possibles_per_position[position]) == 6:
            continue
        elif len(possibles_per_position[position]) == 1:
            print(
                f"position {position + 1} is {COLORS[possibles_per_position[position].pop()]}")
        elif len(possibles_per_position[position]) > 3:
            print(
                f"position {position + 1} is not {', '.join([COLORS[color] for color in get_complementary(possibles_per_position[position])])}")
        else:
            print(
                f"position {position + 1} can be {', '.join([COLORS[color] for color in possibles_per_position[position]])}")

    pass


def generate_hints(possible_codes):
    born_inf = [4, 4, 4, 4, 4, 4]
    born_sup = [0, 0, 0, 0, 0, 0]
    possibles_per_position = [set(), set(), set(), set()]

    colors = ["1", "2", "3", "4", "5", "6"]

    for code in possible_codes:
        for i in range(4):
            possibles_per_position[i].add(code[i])
        for color in colors:
            born_inf[int(color) - 1] = min(born_inf[int(color) - 1],
                                           count_frequency(code, color))
            born_sup[int(color) - 1] = max(born_sup[int(color) - 1],
                                           count_frequency(code, color))

    return get_hints_in_nl(born_inf, born_sup, possibles_per_position)
