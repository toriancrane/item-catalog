import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    """ Corresponds to the User table """
    # Table information
    __tablename__ = 'user'

    # Mappers
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)    
    email = Column(String(250), nullable = False)
    picture = Column(String(250))

class Game(Base):
    """ Corresponds to the Game table """
    # Table information
    __tablename__ = 'game'

    # Mappers
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    description = Column(String(250), nullable = False)
    genre = Column(String(250), nullable = False)
    price = Column(String(8))
    picture = Column(String(250))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

engine = create_engine(
    'sqlite:///gamecatalog.db')

Base.metadata.create_all(engine)