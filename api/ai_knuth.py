import collections
import itertools
import random

from game import colors_to_string, generate_feedback


class mastermind:
    def __init__(self):
        # all possible code combinations
        self.all_answers = list(itertools.product("123456", repeat=4))
        # dictionary to store the score for each possible guess - answer combination
        self.all_scores = collections.defaultdict(dict)

        # filling the dictionary with the scores
        for guess, answer in itertools.product(self.all_answers, repeat=2):
            self.all_scores[guess][answer] = generate_feedback(
                guess, answer)

    def play(self, answer):
        # initialize the number of guesses
        self.turns = 0

        # initialize the list of possible scores and possible answers
        self.possible_scores = self.all_scores.copy()
        self.possible_answers = self.all_answers

        guesses = []
        feedbacks = []

        # while less then 10 guesses
        while self.turns < 10:
            # make a guess
            self.guess = self.make_guess()

            if self.guess in self.all_answers:  # if the guess is valid
                self.turns += 1
                # calculate the guess score
                self.score = generate_feedback(self.guess, answer)

                guesses.append(self.guess)
                feedbacks.append(self.score)

                # if score is BBBB, then code broken
                if self.score == (4, 0):
                    break
        game = []
        for guess, score in zip(guesses, feedbacks):
            game.append({'guess': guess, 'score': score})

        return game

    def make_guess(self):
        # case where we already played
        if self.turns:
            # filtering the list of possible answers to keep only the answers that would give the same score for the current guess
            self.possible_answers = {
                answer for answer in self.possible_answers if self.all_scores[self.guess][answer] == self.score}

            # empty list to store potential guesses
            guesses = []
            guesses_valid = []

            # iterating over the list of possible scores
            for guess, scores_by_answer in self.possible_scores.items():
                # filtering the list of answers to keep only the answers that are possible
                scores_by_answer = {answer: score for answer, score in scores_by_answer.items(
                ) if answer in self.possible_answers}
                # updating the possible scores for the corresponding guess with the new list
                self.possible_scores[guess] = scores_by_answer
                # counting the number of possible answers for each score
                possibilities_per_score = collections.Counter(
                    scores_by_answer.values())
                # the number of appearances for the score with the most possible answers
                worst_case_possibilities = max(
                    possibilities_per_score.values())
                if guess not in self.possible_answers:
                    guesses.append((worst_case_possibilities, guess))
                else:
                    guesses_valid.append((worst_case_possibilities, guess))

            # min(guesses) returns the tuple with the minimum worst_case_possibilities
            # [-1] to return the guess from the tuple
            if guesses_valid:
                return min(guesses_valid)[-1]
            else:
                return min(guesses)[-1]

        else:  # case where this is the first guess
            return ("1", "1", "2", "2")


mm = mastermind()


def play_level_expert(answer):
    game = mm.play(answer)

    guesses = []
    feedbacks = []

    for turn in game:
        guesses.append(colors_to_string(turn['guess']))
        black, white = turn['score']
        new_feedback = ['black'] * black + ['white'] * white
        feedbacks.append(new_feedback)

    return guesses, feedbacks

