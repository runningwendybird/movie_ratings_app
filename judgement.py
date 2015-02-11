from flask import Flask, render_template, redirect, request, session, flash
import model
import jinja2

app = Flask(__name__)

@app.route("/")
def index():
    user_list = model.Session.query(model.User).limit(5).all()
    return render_template("user_list.html", users=user_list)

@app.route("/create_user", methods=["GET", "POST"]) 
def create_user():
    email = request.form.get("email")
    password = request.form.get("password")
    age = (request.form.get("age"))
    age = int(age)
    zipcode = request.form.get("zipcode")

    new_user = model.User(email=email, password=password, age=age, zipcode=zipcode)
    model.insert_new_user(new_user)
    flash("Please, log in here.")
    return redirect("/log_in")

@app.route("/log_in", methods=["Get", "POST"])
def log_in():
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