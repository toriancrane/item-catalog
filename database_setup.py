import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

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

class Item(Base):
    """ Corresponds to the Item table """
    # Table information
    __tablename__ = 'item'

    # Mappers
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    description = Column(String(250))
    price = Column(String(8))
    


engine = create_engine(
    'sqlite:///restaurantmenuwithusers.db')

Base.metadata.create_all(engine)