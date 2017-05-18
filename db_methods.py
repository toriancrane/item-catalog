from flask import flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Game, Genre

engine = create_engine('sqlite:///gamecatalog.db?check_same_thread=False')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

def addNewUser(name, email, picture):
    new_user = User(name = name, email = email, picture = picture)
    session.add(new_user)
    session.commit()

def getUserIDByEmail(email):
    try:
        user = session.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None

def getUserIDByGameID(game_id):
    game = session.query(Game).filter_by(id = game_id).one()
    return game.user_id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id = user_id).one()
    return user

def getAllGames():
    """ Query all games """
    games = session.query(Game).all()
    return games

def getAllGenres():
    genres = session.query(Genre).all()
    return genres

def searchGenreIDByName(name):
    genre = session.query(Genre).filter_by(name = name).one()
    return genre.id

def searchGenreByID(genre_id):
    genre = session.query(Genre).filter_by(id = genre_id).one()
    return genre

def getRecentGames():
    """ Query all games and return most recently added, max of 12 """
    recent_games = session.query(Game).order_by(Game.time_created.desc()).limit(12).all()
    return recent_games

def searchGamesByGenreID(genre_id):
    games = session.query(Game).filter_by(genre_id = genre_id).all()
    return games

def addNewGame(name, desc, genre_id, price, picture, user_id):
    new_game = Game(name = name, description = desc, genre_id = genre_id,
                    price = price, picture = picture, user_id = user_id)
    session.add(new_game)
    session.commit()

def editGame(name, desc, genre_id, price, picture, game_id):
    game = session.query(Game).filter_by(id = game_id).one()
    game.name = name
    game.description = desc
    game.genre_id = genre_id
    game.price = price
    game.picture = picture
    session.add(game)
    session.commit()

def deleteGame(game_id):
    game = session.query(Game).filter_by(id = game_id).one()
    session.delete(game)
    session.commit()

def searchGameByName(name):
    game = session.query(Game).filter_by(name = name).one()
    return game

def searchGameByID(game_id):
    game = session.query(Game).filter_by(id = game_id).one()
    return game