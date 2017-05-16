from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Game

engine = create_engine('sqlite:///gamecatalog.db')
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


# Create dummy users
User1 = User(name="Leroy Jenkins", email="leroooy@jenkins.com",
             picture='http://i.imgur.com/pDANICc.png')
session.add(User1)
session.commit()

User2 = User(name="Torian Crane", email="toriancrane@gmail.com",
             picture='https://scontent.xx.fbcdn.net/v/t1.0-9/15590210_1222450577834404_6774373928245773084_n.jpg?oh=98df2afb741137205e3274986d670aaf&oe=59B50004')
session.add(User2)
session.commit()

# Games by Leroy Jenkins #1
game1 = Game(user_id = 1, name = "World of Warcraft", description = "World of Warcraft (WoW) is a massively multiplayer online role-playing game (MMORPG) released in 2004 by Blizzard Entertainment.",
              genre = "MMORPG", price = "$19.99", picture = "https://upload.wikimedia.org/wikipedia/en/9/91/WoW_Box_Art1.jpg")
session.add(game1)
session.commit()

game2 = Game(user_id = 1, name = "Overwatch", description = "Overwatch is a team-based online multiplayer first-person shooter video game developed and published by Blizzard Entertainment.",
              genre = "First-person shooter", price = "$39.99", picture = "https://upload.wikimedia.org/wikipedia/en/8/8f/Overwatch_cover_art_%28PC%29.jpg")
session.add(game2)
session.commit()

game5 = Game(user_id = 1, name = "Heroes of the Storm", description = "Heroes of the Storm (HotS) is a multiplayer online battle arena video game developed and published by Blizzard Entertainment for Microsoft Windows and macOS.",
		genre = "MOBA", price = "Free", picture = "https://upload.wikimedia.org/wikipedia/en/4/44/Heroes_of_the_Storm_logo_2016.png")


# Games by Torian Crane #2
game3 = Game(user_id = 2, name = "Destiny", description = "Destiny is an online-only multiplayer first-person shooter video game developed by Bungie and published by Activision.",
              genre = "Action role-playing", price = "$29.99", picture = "https://upload.wikimedia.org/wikipedia/en/b/be/Destiny_box_art.png")
session.add(game3)
session.commit()

game4 = Game(user_id = 2, name = "Final Fantasy XV", description = "Final Fantasy XV[b] is an open world action role-playing video game developed and published by Square Enix for the PlayStation 4 and Xbox One home consoles.",
              genre = "Action role-playing", price = "$39.99", picture = "https://upload.wikimedia.org/wikipedia/en/5/5a/FF_XV_cover_art.jpg")
session.add(game4)
session.commit()


print "added games!"