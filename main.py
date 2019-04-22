from flask import Flask, render_template, request, make_response
import random

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    secret = request.cookies.get("secret")
    response = make_response(render_template("index.html"))
    if not secret:
        secret_number = str(random.randint(1, 30))
        response.set_cookie("secret", str(secret_number))
    return response


@app.route("/result", methods=["POST"])
def result():
    secret = int(request.cookies.get("secret"))
    guess = int(request.form.get("guess"))

    if guess == secret:
        message = ("You've guessed it - congratulations! It's number {0}").format(secret)
        response = make_response(render_template("result.html", message=message))
        response.set_cookie("secret", str(random.randint(1, 30)))
        return response
    elif guess < 1 or guess > 30:
        message = ("Choose number between 1 and 30")
        return render_template("result.html", message=message)
    elif guess > secret :
        message = ("Your guess is not correct... try something smaller")
        return render_template("result.html", message=message)
    elif guess < secret:
        message = ("Your guess is not correct... try something bigger")
        return render_template("result.html", message=message)


if __name__ == '__main__':
    app.run()