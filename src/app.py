from flask import Flask, render_template

from database import Database

"""
Flask app for email verification and the embedded algorithm info website.
Run directly or via subprocess from main.py.
"""

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/opt")
def two_opt():
    return render_template("opt.html")

@app.route("/antcolony")
def ant_colony():
    return render_template("antColony.html")

@app.route("/heldkarp")
def held_karp():
    return render_template("heldkarp.html")

@app.route("/linkernighan")
def lin_kernighan():
    return render_template("linKernighan.html")

@app.route("/insertionalgorithms")
def insertion_algorithms():
    return render_template("insertionAlgorithms.html")

@app.route("/nearestNeighbour")
def nearest_neighbour():
    return render_template("nearestNeighbour.html")

@app.route("/randomisedLocalSearch")
def randomised_local_search():
    return render_template("randomisedLocalSearch.html")

@app.route("/verify/<int:user_id>/<string:verification_code>")
def verify_account(user_id, verification_code):
    db = Database()
    if db.verify_account(user_id, verification_code):
        return render_template("verification.html")
    return render_template("verification.html", error="Invalid or expired link.")

if __name__ == "__main__":
    app.run(debug=True)
