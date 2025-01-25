from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get form data
        interest = request.form["interest"]
        destination = request.form["destination"]
        dates = request.form["dates"]
        # Pass data to the travel buddy page
        return render_template("buddy.html", interest=interest, destination=destination, dates=dates)
    return render_template("index.html")

@app.route("/buddy", methods=["GET", "POST"])
def travel_buddy():
    return render_template("buddy.html")

if __name__ == "__main__":
    app.run(debug=True)
