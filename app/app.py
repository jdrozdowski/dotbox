from flask import Flask, flash, redirect, render_template, request, session, url_for
from ComputerPlayer import ComputerPlayer
from Game import Game
from Player import Player
from uuid import uuid4
from wtforms import Form, StringField, RadioField, validators
import os

app = Flask(__name__)
games = {}


@app.route('/')
def index():
    """
    A view that displays the homepage.
    :return render_template():
    """
    return render_template('index.html')


@app.route('/rules')
def rules():
    """
    A view that displays rules of the game.
    :return render_template():
    """
    return render_template('rules.html')


@app.route('/start', methods=['GET', 'POST'])
def start():
    """
    A view that displays the creating game page.
    :return render_template():
    """
    form = GameSettingsForm(request.form)
    if request.method == 'POST' and form.validate():
        if 'player_id' not in session:
            session['player_id'] = uuid4()

        global games
        games = {i: instance for i, instance in games.items() if not instance.is_time_up()}

        if form.opponent.data == 'cpu':
            game_instance = Game('Gra z komputerem', int(form.size.data[0]), int(form.size.data[1]), [Player(session['player_id']), ComputerPlayer()], False)
            game_id = id(game_instance)
            games[game_id] = game_instance

            if games[game_id].turn is 0:
                return redirect(url_for('game', game_id=game_id))
            else:
                cpu_move = games[game_id].players[games[game_id].turn].find_best_move(games[game_id].board)
                return redirect(url_for('move', game_id=game_id, direction=cpu_move['direction'], row=cpu_move['row'], col=cpu_move['col']))

        elif form.opponent.data == 'player':
            game_instance = Game('Gra na 2 graczy', int(form.size.data[0]), int(form.size.data[1]), [Player(session['player_id']), Player(session['player_id'])], False)
            game_id = id(game_instance)
            games[game_id] = game_instance

            return redirect(url_for('game', game_id=game_id))

    return render_template('start.html', form=form)


@app.route('/games', methods=['GET', 'POST'])
def online_games():
    """
    A view that displays available games and creating online game form.
    :return render_template():
    """
    global games
    games = {i: instance for i, instance in games.items() if not instance.is_time_up()}

    form = OnlineGameSettingsForm(request.form)
    if request.method == 'POST' and form.validate():
        if 'player_id' not in session:
            session['player_id'] = uuid4()

        game_instance = Game(form.name.data, int(form.size.data[0]), int(form.size.data[1]), [Player(session['player_id'])], True)
        game_id = id(game_instance)
        games[game_id] = game_instance

        return redirect(url_for('game', game_id=game_id))

    game_list = []
    for game_id, game_instance in games.items():
        if game_instance.availability:
            game_list.append(
                {
                    'game_id': game_id,
                    'name': game_instance.name,
                    'board_size': '%sx%s' % (str(game_instance.board.rows), str(game_instance.board.cols))
                }
            )

    return render_template('games.html', form=form, games=game_list)


@app.route('/game/<int:game_id>')
def game(game_id):
    """
    A view that displays the game page.
    :return render_template():
    """
    global games
    games = {i: instance for i, instance in games.items() if not instance.is_time_up()}

    if game_id in games.keys():
        if 'player_id' in session:
            if session['player_id'] in [player.get_player_id() for player in games[game_id].players if isinstance(player, Player)]:
                return render_template('game.html', game_id=game_id, board=games[game_id].board, players=games[game_id].players, turn=games[game_id].turn)
    else:
        flash('Rozgrywka, z którą chcesz sie połączyć, nie istnieje.', 'danger')

    return redirect(url_for('online_games'))


@app.route('/game/<int:game_id>/join')
def join(game_id):
    global games
    games = {i: instance for i, instance in games.items() if not instance.is_time_up()}

    if game_id in games.keys():
        if games[game_id].availability:

            if 'player_id' in session:
                if session['player_id'] == games[game_id].players[0].get_player_id():
                    flash('Nie możesz dołączyć do gry, w której już jesteś graczem.', 'danger')

                    return redirect(url_for('game', game_id=game_id))
            else:
                session['player_id'] = uuid4()

            games[game_id].players.append(Player(session['player_id']))
            games[game_id].availability = False

            return redirect(url_for('game', game_id=game_id))

    flash('Rozgrywka, z którą chcesz sie połączyć, nie istnieje.', 'danger')

    return redirect(url_for('online_games'))


@app.route('/game/<int:game_id>/<string:direction>/<int:row>/<int:col>')
def move(game_id, direction=None, row=None, col=None):
    global games
    games = {i: instance for i, instance in games.items() if not instance.is_time_up()}

    if game_id in games.keys():
        if not games[game_id].availability and games[game_id].turn is not None:
            if 'player_id' in session:
                if session['player_id'] == games[game_id].players[games[game_id].turn].get_player_id() or games[game_id].players[games[game_id].turn].get_player_id() is None:

                    if isinstance(games[game_id].players[games[game_id].turn], ComputerPlayer):
                        cpu_move = games[game_id].players[games[game_id].turn].find_best_move(games[game_id].board)

                        if cpu_move:
                            direction = cpu_move['direction']
                            row = cpu_move['row']
                            col = cpu_move['col']

                    if direction == 'horizontal' and row in range(games[game_id].board.rows + 1) and col in range(games[game_id].board.cols):
                        if games[game_id].board.horizontal_edges[row][col]:
                            return redirect(url_for('game', game_id=game_id))
                    elif direction == 'vertical' and row in range(games[game_id].board.rows) and col in range(games[game_id].board.cols + 1):
                        if games[game_id].board.vertical_edges[row][col]:
                            return redirect(url_for('game', game_id=game_id))
                    else:
                        return redirect(url_for('game', game_id=game_id))

                    games[game_id].board.last_move = {'player': games[game_id].turn, 'direction': direction, 'row': row, 'col': col}
                    scored = games[game_id].draw_edge(direction, row, col)

                    if scored:
                        if games[game_id].is_game_over():
                            games[game_id].turn = None
                    else:
                        games[game_id].change_turn()

                    return render_template('game.html', game_id=game_id, board=games[game_id].board, players=games[game_id].players, turn=games[game_id].turn)

                return redirect(url_for('game', game_id=game_id))
            else:
                flash('Rozgrywka, z którą chcesz sie połączyć, nie istnieje.', 'danger')

                return redirect(url_for('online_games'))

        else:
            flash('Poczekaj na przeciwnika.', 'danger')

            return redirect(url_for('game', game_id=game_id))
    else:
        flash('Rozgrywka, z którą chcesz sie połączyć, nie istnieje.', 'danger')

        return redirect(url_for('online_games'))


@app.route('/game/<int:game_id>/leave')
def leave(game_id):
    global games

    if game_id in games:
        if 'player_id' in session:
            for i in range(len(games[game_id].players)):
                if games[game_id].players[i] != 'left':
                    if games[game_id].players[i].player_id == session['player_id']:
                        games[game_id].players[i] = 'left'

                        if games[game_id].is_no_players():
                            del games[game_id]

                        return redirect(url_for('index'))

        flash('Nie możesz opuścić rozgrywki, w której nie uczestniczysz.', 'danger')

        return redirect(url_for('index'))
    else:
        flash('Rozgrywka, z którą chcesz sie połączyć, nie istnieje.', 'danger')

        return redirect(url_for('online_games'))


class GameSettingsForm(Form):
    """
    Class GameSettingsForm
    """
    opponent = RadioField('Przeciwnik', default='cpu', choices=[
        ('cpu', 'Komputer'),
        ('player', 'Drugi gracz')
    ], validators=[validators.InputRequired(message='Musisz wybrać przeciwnika')])
    size = RadioField('Rozmiar planszy', default='33', choices=[
        ('33', '3x3'),
        ('45', '4x5'),
        ('65', '6x5'),
        ('75', '7x5'),
        ('87', '8x7')
    ], validators=[validators.InputRequired(message='Musisz podać rozmiar planszy.')])


class OnlineGameSettingsForm(Form):
    """
    Class OnlineGameSettingsForm
    """
    name = StringField('Nazwa rozgrywki', validators=[
        validators.InputRequired(message='Nazwa rozgrywki jest wymagana.'),
        validators.length(min=2, max=128, message='Nazwa rozgrywki może zawierać od 2 do 128 znaków.')
    ])
    size = RadioField('Rozmiar planszy', default='33', choices=[
        ('33', '3x3'),
        ('45', '4x5'),
        ('65', '6x5'),
        ('75', '7x5'),
        ('87', '8x7')
    ], validators=[validators.InputRequired(message='Musisz podać rozmiar planszy.')])


if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(host="0.0.0.0", port=5007, debug=True)
