from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from pearson import pearson



ENGINE = create_engine("sqlite:///ratings.db", echo=True)
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

    def get_user_by_email(self, email):
        user = Session.query(User).filter_by(email=email).one()
        return user

    def similarity(self, user2):
        u_ratings = {}
        paired_ratings = []
        for r in self.rating:
            u_ratings[r.movie_id] = r

        for r in user2.rating:
            u_r = u_ratings.get(r.movie_id)
            if u_r:
                paired_ratings.append((u_r.rating, r.rating))

        if paired_ratings:
            return pearson(paired_ratings)
        else:
            return 0.0

    def predict_rating(self, movie):
        ratings = self.rating
        other_ratings = movie.rating
        similarities = [(self.similarity(r.user), r) for r in other_ratings]
        similarities.sort(reverse = True)
        similarities = [ sim for sim in similarities if sim[0] > 0 ]
        if not similarities:
            return None
        numerator = sum([r.rating * similarity for similarity, r in similarities])
        denominator = sum([similarity[0] for similarity in similarities])
        return numerator/denominator



class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable=False)
    released_at = Column(DateTime(timezone=False), nullable=True)
    imdb_url = Column(String(200), nullable=True)


    def __repr__(self):
        return "Movie_id: %d, name: %s, release_date: %r, imdb_url: %s" %(self.id, self.name, self.released_at, self.imdb_url)

    def ave(self):
        total_sum=0
        count=0
        for individual_rating in self.rating:
            total_sum = total_sum + individual_rating.rating
            count = count + 1

        count=float(count)
        return total_sum/count 

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
def get_user_by_email(email):
    user = Session.query(User).filter_by(email=email).first()
    return user

def get_user_by_id(id):
    user = Session.query(User).filter_by(id=id).first()
    return user

def insert_new_user(new_user):
    Session.add(new_user)
    Session.commit()

def get_rating_history(user):
    ratings = Session.query(Rating).filter_by(user_id=user.id).all()
    return ratings

def get_movie_history(user):
    ratings = get_rating_history(user)
    movies = []
    for rating in ratings:
        movies.append(rating.movies)
    return movies


def get_movies():
    movies = Session.query(Movie).all()
    return movies

def get_movie_by_id(id):
    movie = Session.query(Movie).filter_by(id=id).first()
    return movie

def add_rating(movie, rating, user):
    new_rating = Rating(movie_id=movie, user_id=user.id, rating=rating)
    Session.add(new_rating)
    Session.commit()

def update_rating(movie, rating, user):
    rating_object = Session.query(Rating).filter_by(movie_id=movie, user_id=user.id).first()
    rating_object.rating = rating

def exclude_rated(user):
    rated_movies = get_movie_history(user)
    all_movies = get_movies()
    unrated_movies = []
    for movie in all_movies:
        if movie not in rated_movies:
            unrated_movies.append(movie)
        else:
            pass

    return unrated_movies

def get_all_users():
    users = Session.query(User).all()
    return users





# def exclude_rated(user):
#     rated_movies = get_rating_history(user)
#     all_movies = Session.query(Movie.id).all()
#     not_rated = []
#     for movie_id in rated_movies.movies.id:
#         if movie_id not in all_movies:
#             not_rated.append(movie_id)
#     return not_rated

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
