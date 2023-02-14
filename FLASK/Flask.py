# archivo: app.py
from flask import Flask, request, render_template
import random

app = Flask(__name__)
number = random.randint(1, 100)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        guess = int(request.form["guess"])
        if guess == number:
            message = "¡Adivinaste! El número era {}.".format(number)
        elif guess < number:
            message = "El número es mayor que {}.".format(guess)
        else:
            message = "El número es menor que {}.".format(guess)
        return render_template("index.html", message=message)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
