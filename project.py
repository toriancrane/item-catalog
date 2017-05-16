from flask import(
    session as login_session,
    Flask,
    flash,
    request,
    redirect,
    url_for,
    render_template,
    make_response)
from functools import wraps
import random, string
import requests
import jinja2
import httplib2
import db_methods
import time
import os
import json

#Additional imports
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

app = Flask(__name__)

# CLIENT_ID = json.loads(
#     open('client_secrets.json', 'r').read())['web']['client_id']
# APPLICATION_NAME = "Restaurant Menu Application"

#####   User Login Decorator    #####
def login_required(func):
    """
    A decorator to confirm a user is logged in or redirect as needed.
    """
    @wraps(func)
    def check_login(*args, **kwargs):
        # Redirect to login if user not logged in, else execute func.
        if 'username' not in login_session:
            return redirect('/login')
        else:
            return func(*args, **kwargs)
    return check_login


@app.route('/')
def frontPage():
    """ Front Page Function """
    return render_template('front.html')

@app.route('/games/')
def gamesPage():
    """ View Recent Games Function """
    games_list = db_methods.getRecentGames()
    genres = db_methods.getAllGenres()
    return render_template('games.html', games = games_list, genres = genres)

@app.route('/games/new/', methods=['GET', 'POST'])
def newGamePage():
    """ Create New Game Function """
    if request.method == 'POST':
        game_name = request.form['game_name']
        game_desc = request.form['game_desc']
        game_genre = request.form['game_genre']
        game_price = request.form['game_price']
        game_pic = request.form['game_pic']
        #Hardcoding user_id for testing purposes until auth functionality implemented
        game_user = 2
        db_methods.addNewGame(game_name, game_desc, game_genre,
                            game_price, game_pic, game_user)
        time.sleep(0.1)
        game = db_methods.searchGameByName(game_name)

        return redirect('/games/%s/info' % game.id)
    else:
        return render_template('newgame.html')

@app.route('/games/<int:game_id>/info/')
def viewGamePage(game_id):
    """ View Game Info Function """
    game = db_methods.searchGameByID(game_id)
    return render_template('info.html', game = game)

if __name__ == '__main__':
    app.secret_key = 'gDI1tL5OC54UiTF3g18a-bWg'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
    #Change this back to be pushed to heroku