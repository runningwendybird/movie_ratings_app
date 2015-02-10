import model
import csv
from datetime import datetime

def load_users(session):
    # use u.user
    file = open("seed_data/u.user")
    for line in file:
        clean_line = line.strip()
        parsed_line = clean_line.split("|")
        temp_user = model.User(id=parsed_line[0], age=parsed_line[1], zipcode=parsed_line[4])
        # temp_user.id = parsed_line[0]
        # temp_user.email = null
        # temp_user.password = null
        # temp_user.age = parsed_line[1]
        # temp_user.zipcode = parsed_line[4]
        session.add(temp_user)
    session.commit()
    file.close()



def load_movies(session):
    # use u.item
    file = open("seed_data/u.item")
    for line in file:
        clean_line = line.strip()
        parsed_line = clean_line.split("|")
        temp_movie = model.Movie()
        temp_movie.id = parsed_line[0]
        name = parsed_line[1]
        temp_movie.name = name.decode("latin-1")
        if parsed_line[2]=="":
            temp_movie.released_at = None
        else:
            temp_movie.released_at = datetime.strptime(parsed_line[2], '%d-%b-%Y')
        temp_movie.imdb_url = parsed_line[4]
        session.add(temp_movie)
    session.commit()
    file.close()
def load_ratings(session):
    # use u.data
    # file = open("seed_data/u.data")
    with open("seed_data/u.data", "rb") as file:
        our_reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
        for line in our_reader:
            print line
            temp_rating = model.Rating() 
            temp_rating.movie_id = line[1]
            temp_rating.user_id = line[0]
            temp_rating.rating = line[2]
            session.add(temp_rating)
    session.commit()
    file.close()


def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    load_movies(session)
    load_ratings(session)

if __name__ == "__main__":
    s= model.connect()
    main(s)
