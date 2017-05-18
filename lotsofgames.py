from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Game, Genre

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

print "Added users..."

# Enter genres into Genre table
genre1 = Genre(name = "Action role-playing")
session.add(genre1)
session.commit()

genre2 = Genre(name = "Fighting")
session.add(genre2)
session.commit()

genre3 = Genre(name = "First-person shooter")
session.add(genre3)
session.commit()

genre4 = Genre(name = "MMORPG")
session.add(genre4)
session.commit()

genre5 = Genre(name = "MOBA")
session.add(genre5)
session.commit()

genre6 = Genre(name = "Other")
session.add(genre6)
session.commit()

genre7 = Genre(name = "Racing")
session.add(genre7)
session.commit()

genre8 = Genre(name = "Real-time strategy")
session.add(genre8)
session.commit()

genre9 = Genre(name = "RPG")
session.add(genre9)
session.commit()

genre10 = Genre(name = "Simulation")
session.add(genre10)
session.commit()

genre11 = Genre(name = "Sports")
session.add(genre11)
session.commit()

genre12 = Genre(name = "Survival")
session.add(genre12)
session.commit()

genre13 = Genre(name = "Turn-based strategy")
session.add(genre13)
session.commit()

genre14 = Genre(name = "Visual Novel")
session.add(genre14)
session.commit()

print "Added genres..."

# Games by Leroy Jenkins #1
game1 = Game(user_id = 1, name = "World of Warcraft", description = "World of Warcraft (WoW) is a massively multiplayer online role-playing game (MMORPG) released in 2004 by Blizzard Entertainment.",
              genre_id = 4, price = "$19.99", picture = "https://upload.wikimedia.org/wikipedia/en/9/91/WoW_Box_Art1.jpg")
session.add(game1)
session.commit()

game2 = Game(user_id = 1, name = "Overwatch", description = "Overwatch is a team-based online multiplayer first-person shooter video game developed and published by Blizzard Entertainment.",
              genre_id = 3, price = "$39.99", picture = "https://upload.wikimedia.org/wikipedia/en/8/8f/Overwatch_cover_art_%28PC%29.jpg")
session.add(game2)
session.commit()

game5 = Game(user_id = 1, name = "Heroes of the Storm", description = "Heroes of the Storm (HotS) is a multiplayer online battle arena video game developed and published by Blizzard Entertainment for Microsoft Windows and macOS.",
		genre_id = 5, price = "Free", picture = "https://upload.wikimedia.org/wikipedia/en/4/44/Heroes_of_the_Storm_logo_2016.png")
session.add(game5)
session.commit()

# Games by Torian Crane #2
game3 = Game(user_id = 2, name = "Destiny", description = "Destiny is an online-only multiplayer first-person shooter video game developed by Bungie and published by Activision.",
              genre_id = 1, price = "$29.99", picture = "https://upload.wikimedia.org/wikipedia/en/b/be/Destiny_box_art.png")
session.add(game3)
session.commit()

game4 = Game(user_id = 2, name = "Final Fantasy XV", description = "Final Fantasy XV[b] is an open world action role-playing video game developed and published by Square Enix for the PlayStation 4 and Xbox One home consoles.",
              genre_id = 1, price = "$39.99", picture = "https://upload.wikimedia.org/wikipedia/en/5/5a/FF_XV_cover_art.jpg")
session.add(game4)
session.commit()

game6 = Game(user_id = 2, name = "Rainbow Six: Siege", description = "Tom Clancy's Rainbow Six Siege is a first-person tactical shooter video game developed by Ubisoft Montreal and published by Ubisoft. Considered as a successor to the now cancelled Tom Clancy's Rainbow 6: Patriots, Siege puts heavy emphasis on environmental destruction and cooperation between players. Unlike previous entries in the series, the title has no campaign and only offers an online mode.",
			genre_id = 3, price = "$39.99", picture = "https://upload.wikimedia.org/wikipedia/en/4/47/Tom_Clancy%27s_Rainbow_Six_Siege_cover_art.jpg")
session.add(game6)
session.commit()

print "Added games..."
print "Database initialized!"