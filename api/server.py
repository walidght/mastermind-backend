import sys
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from game import colors_to_index_string, colors_to_string, generate_code, generate_feedback
from hint import generate_hints
from game import keep_possible
from player import play
from ai_easy import play_level_easy
from ai_normal import play_level_normal
from ai_expert import play_level_expert


app = Flask(__name__, static_url_path='', static_folder='static')

# Parse command-line arguments
if '--env=development' in sys.argv:
    # Enable CORS only during development
    CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/code')
def json_response():
    data = colors_to_string(list(generate_code()))
    print("@get /code", data)
    return jsonify(data)


@app.route('/guess', methods=['POST'])
def guess():
    if request.is_json:
        data = request.json
        answer = data['answer']
        guess = data['guess']
        black, white = generate_feedback(guess, answer)
        #######################################
        # je te laisse le code pour la partie #
        # où on calcul le nombre de coup max  #
        #######################################
        # max_remaining = play(guess, (black, white))
        feedback = {"colors": ['black'] * black + ['white']
                    * white, "won": True if black == 4 else False}
        # feedback = {"colors": ['black'] * black + ['white'] * white, 
        #             "won": True if black == 4 else False,
        #             "max_remaining": max_remaining}
        print("@post /guess", data)
        print("return: ", feedback)
        return jsonify(feedback)
    else:
        return 'Request is not in JSON format.'


@app.route('/hint', methods=['POST'])
def hint():
    if request.is_json:
        data = request.json
        guesses = data['guesses']
        feedbacks = data['feedbacks']
        guesses = [tuple(colors_to_index_string(s)) for s in guesses]
        feedbacks = [(f.count('black'), f.count('white')) for f in feedbacks]
        game = []
        for (guess, score) in zip(guesses, feedbacks):
            game.append({'guess': guess, 'score': score})
        possible_codes = keep_possible(game)
        hints = generate_hints(possible_codes)
        return jsonify(hints)
    else:
        return 'Request is not in JSON format.'


@app.route('/ai', methods=['POST'])
def ai():
    if request.is_json:
        print("@post /ai")
        data = request.json
        level = data['level']
        code = data['code']
        code = tuple(colors_to_index_string(code))

        if (level == "easy"):
            guesses, feedbacks = play_level_easy(code)
            return jsonify({'guesses': guesses, 'feedbacks': feedbacks})
        elif (level == "normal"):
            guesses, feedbacks = play_level_normal(code)
            return jsonify({'guesses': guesses, 'feedbacks': feedbacks})
        elif (level == "expert"):
            guesses, feedbacks = play_level_expert(code)
            return jsonify({'guesses': guesses, 'feedbacks': feedbacks})
        else:
            return ''
    else:
        return 'Request is not in JSON format.'


if __name__ == '__main__':
    app.run(debug=True)
