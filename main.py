from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User
import random

app = Flask(__name__)
attempts = 0

@app.route("/", methods=["GET"])
def index():

    user_name = request.cookies.get("name")

    if user_name:
        user = User.fetch_one(query=["name", "==", user_name])
    else:
        user = None

    return render_template("index.html", user=user)

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    secret = random.randint(1, 30)
    user = User.fetch_one(query=["name", "==", name])

    if not user:
        user = User(name=name, secret=secret)
        user.create()

    response = make_response(redirect(url_for('index')))
    response.set_cookie("name", name)

    return response

@app.route("/result", methods=["POST"])
def result():
    while True:
        try:
            global attempts
            attempts += 1
            guess = int(request.form.get("guess"))
            user_name = request.cookies.get("name")
            new_secret = random.randint(1, 30)
            user = User.fetch_one(query=["name", "==", user_name])

            if guess == user.secret:
                message = ("You've guessed it {1} - congratulations! It's number {0}. Attempts {2}").format(guess, user.name, attempts)
                response = make_response(render_template("new-game.html", message=message))
                response.delete_cookie("name")
                User.edit(obj_id=user.id, secret=new_secret, attempts=attempts)
                attempts = 0
                return response
                break
            elif guess < 1 or guess > 30:
                message = ("You didn't enter a number between 1 and 30")
                return render_template("result.html", message=message)
            elif guess > user.secret:
                message = ("Your guess is not correct... try something smaller")
                return render_template("result.html", message=message)
            elif guess < user.secret:
                message = ("Your guess is not correct... try something bigger")
                return render_template("result.html", message=message)
        except ValueError:
            message = ("You didn't enter a number")
            return render_template("result.html", message=message)
            continue


@app.route("/end-game")
def end_game():
    return render_template("end-game.html")

@app.route("/top-score-table")
def top_score_table():
    return render_template("top-score-table.html")

if __name__ == '__main__':
    app.run()