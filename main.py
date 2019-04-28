from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User
import random

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    email_address = request.cookies.get("email")

    if email_address:
        user = User.fetch_one(query=["email", "==", email_address])
    else:
        user = None

    return render_template("index.html", user=user)

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")
    secret = random.randint(1, 30)

    user = User.fetch_one(query=["email", "==", email])

    if not user:
        user = User(name=name, email=email, secret=secret)
        user.create()

    response = make_response(redirect(url_for('index')))
    response.set_cookie("email", email)

    return response

@app.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("guess"))
    email_address = request.cookies.get("email")

    user = User.fetch_one(query=["email", "==", email_address])

    if guess == user.secret:
        message = ("You've guessed it {1} - congratulations! It's number {0}").format(guess, user.name)
        User.edit(obj_id=user.id, email=None)
        return render_template("new-game.html", message=message)
    elif guess < 1 or guess > 30:
        message = ("You didn't enter a number between 1 and 30")
        return render_template("result.html", message=message)
    elif guess > user.secret:
        message = ("Your guess is not correct... try something smaller")
        return render_template("result.html", message=message)
    elif guess < user.secret:
        message = ("Your guess is not correct... try something bigger")
        return render_template("result.html", message=message)


if __name__ == '__main__':
    app.run()