from flask import Flask, render_template, redirect, request, session, flash
import model
import jinja2

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    user_list = model.Session.query(model.User).limit(5).all()
    return render_template("user_list.html", users=user_list)

@app.route("/create_user") 
def create_user():
    # email = request.form.get("email")
    # password = request.form.get("password")
    # age = (request.form.get("age"))
    # age = int(age)
    # zipcode = request.form.get("zipcode")

    # new_user = model.User(email=email, password=password, age=age, zipcode=zipcode)
    # model.insert_new_user(new_user)
    # flash("Please, log in here.")
    return render_template("create_user.html")

@app.route("/log_in")
def log_in():
    # email = request.form.get("email")
    # password = request.form.get("password")
    # user = model.get_user_by_email(email)
    # if user.email == None:
    #     flash("Please, sign up.")
    #     return redirect("/create_user")
    # else:
    #     if user.password == password:
    #         session['email'] = user.email
    #         flash ("Successful signin!")
    #         return redirect("/user_history")
    #     else:
    #         flash("There is a problem with the email or password you entered. Try Again.")
    #         return redirect("/log_in")
    return render_template("log_in.html")

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
    return redirect("/log_in")

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
            flash ("Successful signin!")
            return redirect("/user_history")
        else:
            flash("There is a problem with the email or password you entered. Try Again.")
            return redirect("/log_in")

# @app.route("/user_history")
# def user_history():

# @app.route("/rating_view")
# def rating_view():



if __name__ == "__main__":
    app.run(debug = True)