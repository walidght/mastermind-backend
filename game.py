import itertools
import random


def generate_feedback(guess, answer):
    black, white = (0, 0)
    wrong_guess_pegs = []
    wrong_answer_pegs = []

    for guess_peg, answer_peg in zip(guess, answer):
        if guess_peg == answer_peg:
            black += 1
        else:
            wrong_guess_pegs.append(guess_peg)
            wrong_answer_pegs.append(answer_peg)

    for peg in wrong_guess_pegs:
        if peg in wrong_answer_pegs:
            wrong_answer_pegs.remove(peg)
            white += 1

    return black, white


def generate_code():
    return tuple(random.choice("123456") for _ in range(4))


def keep_possible(game, possible_answers=None):
    if possible_answers is None:
        possible_answers = list(itertools.product("123456", repeat=4))
    for turn in game:
        for possible in possible_answers:
            if generate_feedback(turn['guess'], possible) != turn['score']:
                possible_answers.remove(possible)

    return possible_answers


def color_to_string(color):
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
    return COLORS[color]


def color_to_index_string(color):
    COLORS = {'green': '1', 'yellow': '2', 'blue': '3',
              'red': '4', 'black': '5', 'white': '6'}
    return COLORS[color]


def colors_to_string(colors):
    return [color_to_string(color) for color in colors]


def colors_to_index_string(colors):
    return [color_to_index_string(color) for color in colors]
