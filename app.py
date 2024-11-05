from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import random
import time

app = Flask(__name__, static_folder="static")
socketio = SocketIO(app)

game_started = False
roulette_numbers = list(range(0, 37))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/frames/<filename>')
def serve_video(filename):
    return send_from_directory(app.static_folder + '/frames', filename)

@socketio.on('start_game')
def handle_start_game():
    global game_started
    if not game_started:
        game_started = True
        emit('game_started', broadcast=True)
        result = random.choice(roulette_numbers)
        emit('game_result', {'result': result}, broadcast=True)
        game_started = False

if __name__ == '__main__':
    socketio.run(app, debug=True)