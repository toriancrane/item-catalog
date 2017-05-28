from flask import(
    session as login_session,
    Flask,
    flash,
    request,
    redirect,
    url_for,
    render_template as flask_render,
    make_response,
    jsonify)
from functools import wraps
import random
import string
import requests
import jinja2
import httplib2
import db_methods
import time
import os
import json

# Additional imports
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Wild Game Catalog"


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('signin.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current ' +
                                            'user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = db_methods.getUserIDByEmail(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    print "done!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect/')
def gdisconnect():
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current ' +
                                 'user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(redirect('/'))
        response.headers['Content-Type'] = 'text/html'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke ' +
                                 'token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# User Login Decorator


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


def createUser(login_session):
    user_name = login_session['username']
    user_email = login_session['email']
    user_pic = login_session['picture']
    db_methods.addNewUser(user_name, user_email, user_pic)

    user_id = db_methods.getUserIDByEmail(user_email)
    return user_id


def render_template(template_name, **params):
    if 'username' in login_session:
        params['user_id'] = login_session['username']
    return flask_render(template_name, **params)


@app.route('/')
def frontPage():
    """ Front Page Function """
    genres = db_methods.getAllGenres()
    if 'username' not in login_session:
        return flask_render('front.html', genres=genres)
    else:
        return render_template('front.html', genres=genres)


@app.route('/games/')
def gamesPage():
    """ View Recent Games Function """
    games_list = db_methods.getRecentGames()
    genres = db_methods.getAllGenres()
    if 'username' not in login_session:
        return render_template('publicgames.html', games=games_list,
                               genres=genres)
    else:
        return render_template('games.html', games=games_list,
                               genres=genres)


@app.route('/games/genre/<int:genre_id>/')
def gamesByGenrePage(genre_id):
    """ View Games by Genre Function """
    games_list = db_methods.searchGamesByGenreID(genre_id)
    all_genres = db_methods.getAllGenres()
    genre = db_methods.searchGenreByID(genre_id)
    if 'username' not in login_session:
        return render_template('publicgamesbygenre.html', games=games_list,
                               genres=all_genres, genre=genre)
    else:
        return render_template('gamesbygenre.html', games=games_list,
                               genres=all_genres, genre=genre)


@app.route('/games/new/', methods=['GET', 'POST'])
@login_required
def newGamePage():
    """ Create New Game Function """
    if request.method == 'POST':
        game_name = request.form['game_name']
        game_desc = request.form['game_desc']
        game_genre = request.form['game_genre']
        game_price = request.form['game_price']
        game_pic = request.form['game_pic']
        game_user = login_session['user_id']

        # Retrieve genre id from genre name
        genre_id = db_methods.searchGenreIDByName(game_genre)

        db_methods.addNewGame(game_name, game_desc, genre_id,
                              game_price, game_pic, game_user)
        time.sleep(0.1)
        game = db_methods.searchGameByName(game_name)

        return redirect('/games/%s/info' % game.id)
    else:
        genres = db_methods.getAllGenres()
        return render_template('newgame.html', genres=genres)


@app.route('/games/<int:game_id>/info/')
def viewGamePage(game_id):
    """ View Game Info Function """
    genres = db_methods.getAllGenres()
    game = db_methods.searchGameByID(game_id)
    if 'username' not in login_session:
        return flask_render('publicinfo.html', game=game, genres=genres)
    else:
        user_id = login_session['user_id']
        return flask_render('info.html', game=game, 
                            user_id=user_id, genres=genres)


@app.route('/games/<int:game_id>/edit/', methods=['GET', 'POST'])
@login_required
def editGamePage(game_id):
    """ Edit Game Function """
    genres = db_methods.getAllGenres()
    game = db_methods.searchGameByID(game_id)
    user_id = login_session['user_id']

    if user_id != game.user_id:
        flash('You do not have permission to edit games that you did not create.')
        return redirect('/games/')

    if request.method == 'POST':
        game_name = request.form['game_name']
        game_desc = request.form['game_desc']
        game_genre = request.form['game_genre']
        game_price = request.form['game_price']
        game_pic = request.form['game_pic']

        # Retrieve genre id from genre name
        genre_id = db_methods.searchGenreIDByName(game_genre)

        db_methods.editGame(game_name, game_desc, genre_id,
                            game_price, game_pic, game_id)
        time.sleep(0.1)
        return redirect('/games/%s/info' % game.id)
    else:
        return flask_render('editgame.html', game=game,
                            user_id=user_id, genres=genres)


@app.route('/games/<int:game_id>/delete/', methods=['GET', 'POST'])
@login_required
def deleteGamePage(game_id):
    genres = db_methods.getAllGenres()
    game = db_methods.searchGameByID(game_id)
    user_id = login_session['user_id']

    if user_id != game.user_id:
        flash('You do not have permission to delete games that you did not create.')
        return redirect('/games/')

    if request.method == 'POST':
        error = game.name + " has been deleted from the database."
        db_methods.deleteGame(game_id)
        return render_template('deleteconfirmation.html', error=error, genres=genres)
    else:
        error = "Are you sure you want to delete this game?"
        return render_template('deletegame.html', error=error,
                               game=game, genres=genres)

# JSON API Endpoints


@app.route('/games/JSON/')
def allGamesJSON():
    games = db_methods.getAllGames()
    return jsonify(Game=[g.serialize for g in games])


@app.route('/games/<int:game_id>/info/JSON/')
def gameInfoJSON(game_id):
    game = db_methods.searchGameByID(game_id)
    return jsonify(Game=[game.serialize])


@app.route('/games/genre/<int:genre_id>/JSON/')
def gamesByGenreJSON(genre_id):
    games = db_methods.searchGamesByGenreID(genre_id)
    return jsonify(Game=[g.serialize for g in games])

if __name__ == '__main__':
    app.secret_key = 'gDI1tL5OC54UiTF3g18a-bWg'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
    # app.run(host = '0.0.0.0', port = int(os.environ.get('PORT', 33507)))
