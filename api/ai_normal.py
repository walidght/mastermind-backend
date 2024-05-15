import itertools
import random

from game import  colors_to_string, generate_feedback, keep_possible


def play_turn(game, possible_answers):
    possible_answers = keep_possible(game, possible_answers)

    return random.choice(possible_answers)


def play_level_normal(answer):

    possible_answers = list(itertools.product("123456", repeat=4))

    game = []

    while True:
        guess = play_turn(game, possible_answers)
        # mutation
        for i in range(4):
            if random.random() <= 0.17:
                change_value = random.randint(1, 6)
                guess = list(guess)
                guess[i] = str(change_value)
                guess = tuple(guess)
        score = generate_feedback(guess, answer)
        game.append({'guess': guess, 'score': score})
        if score == (4, 0):
            break
        keep_possible(game, possible_answers)

    guesses = []
    feedbacks = []

    for turn in game:
        guesses.append(colors_to_string(turn['guess']))
        black, white = turn['score']
        new_feedback = ['black'] * black + ['white'] * white
        feedbacks.append(new_feedback)

    return guesses, feedbacks
