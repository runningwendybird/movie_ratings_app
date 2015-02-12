from flask import Flask, render_template, redirect, request, session, flash
import model
import jinja2


app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def log_in():
    return render_template("log_in.html")


@app.route("/create_user") 
def create_user():
    return render_template("create_user.html")


@app.route("/new_user_welcome", methods=["POST"])
def new_user_welcome():
    email = request.form.get("email")
    password = request.form.get("password")
    age = (request.form.get("age"))
    age = int(age)
    zipcode = request.form.get("zipcode")

    new_user = model.User(email=email, password=password, age=age, zipcode=zipcode)
    model.insert_new_user(new_user)
    flash("Please, log in here.")
    return redirect("/")


@app.route("/returning_user_welcome", methods=["POST"])
def returning_user_welcome():
    email = request.form.get("email")
    password = request.form.get("password")
    user = model.get_user_by_email(email)
    if user.email == None:
        flash("Please, sign up.")
        return redirect("/create_user")
    else:
        if user.password == password:
            session['email'] = user.email
            flash ("Welcome back!")
            return redirect("/user_profile")
        else:
            flash("There is a problem with the email or password you entered. Try Again.")
            return redirect("/log_in")


@app.route("/select_user")
def select_user():
    return render_template("selected_user_ratings.html")


@app.route("/user_list")
def index():
    user_list = model.Session.query(model.User).limit(5).all()

    return render_template("user_list.html", users=user_list)

@app.route("/user_profile")
def user_profile():
    user=model.get_user_by_email(session["email"])
    ratings_list = model.get_rating_history(user)
    return render_template("user_history.html", user=user, ratings_list=ratings_list)

@app.route("/rating_view")
def rating_view():
    user = model.get_user_by_email(session["email"])
    unrated_movies = model.exclude_rated(user)
    rated_movies = model.get_rating_history(user)
    return render_template("rating_view.html", movies=unrated_movies, rated_movies=rated_movies)

@app.route("/update_ratings")
def update_rating():
    movie = request.args.get("movie_to_rate")
    rating = request.args.get("current_rating")
    user = model.get_user_by_email(session["email"])
    model.update_rating(movie, rating, user) 
    return redirect("/user_profile")

@app.route("/add_rating")   
def add_rating():
    movie = request.args.get("movie_to_rate")
    rating = request.args.get("current_rating")
    user = model.get_user_by_email(session["email"])
    # previously_rated=model.get_rating_history(user)
    # print previously_rated
    # for rating in previously_rated:
    #     if movie == rating.movies.id:
    #         flash("You already rated that.")
    #         return redirect("/user_profile")
    #     else:
    #         pass
    model.add_rating(movie, rating, user)

    return redirect("/user_profile")
if __name__ == "__main__":
    app.run(debug = True)