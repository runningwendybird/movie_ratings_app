from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref



ENGINE = create_engine("sqlite:///ratings.db", echo=False)
Session = scoped_session(sessionmaker(bind=ENGINE, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = Session.query_property()

### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)

    def __repr__(self):
        return "User_id: %d, Email: %s, Age: %d, Zip: %s" % (self.id, self.email, self.age, self.zipcode)


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable=False)
    released_at = Column(DateTime(timezone=False), nullable=True)
    imdb_url = Column(String(200), nullable=True)


    def __repr__(self):
        return "Movie_id: %d, name: %s, release_date: %r, imdb_url: %s" %(self.id, self.name, self.released_at, self.imdb_url)

class Rating(Base):
    __tablename__ = "rating"
    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer, nullable = False)

    user = relationship("User",
        backref=backref("rating", order_by=id))

    movies = relationship("Movie",
        backref=backref("rating", order_by=id))
    
    def __repr__(self):
        return "Rating id: %d, Movie_id: %d, User_id: %d, Rating: %d" %(self.id, self.movie_id, self.user_id, self.rating)


### End class declarations


# def connect():
#     global ENGINE
#     global Session

#     # ENGINE = create_engine("sqlite:///ratings.db", echo=True)
#     # Session = sessionmaker(bind=ENGINE)

#     return Session()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
