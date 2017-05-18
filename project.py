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

@app.route('/games/genre/<int:genre_id>/')
def gamesByGenrePage(genre_id):
    """ View Games by Genre Function """
    games_list = db_methods.searchGamesByGenreID(genre_id)
    all_genres = db_methods.getAllGenres()
    genre = db_methods.searchGenreByID(genre_id)
    return render_template('gamesbygenre.html', games = games_list,
                            genres = all_genres, genre = genre)


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

        #Retrieve genre id from genre name
        genre_id = db_methods.searchGenreIDByName(game_genre)

        db_methods.addNewGame(game_name, game_desc, genre_id,
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

@app.route('/games/<int:game_id>/edit/', methods=['GET', 'POST'])
def editGamePage(game_id):
    """ Edit Game Function """
    game = db_methods.searchGameByID(game_id)
    if request.method == 'POST':
        game_name = request.form['game_name']
        game_desc = request.form['game_desc']
        game_genre = request.form['game_genre']
        game_price = request.form['game_price']
        game_pic = request.form['game_pic']

        #Retrieve genre id from genre name
        genre_id = db_methods.searchGenreIDByName(game_genre)

        db_methods.editGame(game_name, game_desc, genre_id,
                            game_price, game_pic, game_id)
        time.sleep(0.1)
        return redirect('/games/%s/info' % game.id)
    else:
        return render_template('editgame.html', game = game)

@app.route('/games/<int:game_id>/delete/', methods=['GET', 'POST'])
def deleteGamePage(game_id):
    game = db_methods.searchGameByID(game_id)
    if request.method == 'POST':
        error = game.name + " has been deleted from the database."
        db_methods.deleteGame(game_id)
        return render_template('deleteconfirmation.html', error = error)
    else:
        error = "Are you sure you want to delete this game?"
        return render_template('deletegame.html', error = error, game = game)

if __name__ == '__main__':
    app.secret_key = 'gDI1tL5OC54UiTF3g18a-bWg'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
    #Change this back to be pushed to heroku