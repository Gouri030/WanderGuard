from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("database/serviceAccountKey.json")  # Update the path
firebase_admin.initialize_app(cred)

# Access Firestore database
db = firestore.client()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        interest = request.form["interest"]
        destination = request.form["destination"]
        travel_dates = request.form["dates"]  # e.g., "2025-03-01 to 2025-03-15"

        # Parse travel dates into start_date and end_date
        start_date, end_date = map(str.strip, travel_dates.split("to"))

        # Firestore document structure
        user_data = {
            "name": name,
            "email": email,
            "destination": destination,
            "interest": interest,
            "travel_dates": {
                "start_date": start_date,
                "end_date": end_date
            }
        }

        # Save data to Firestore under the 'users' collection
        db.collection("users").add(user_data)

        return render_template("buddy.html", name=name, destination=destination, dates=travel_dates)

    return render_template("index.html")

@app.route("/buddy", methods=["GET", "POST"])
def travel_buddy():
    return render_template("buddy.html")

# User Registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        email = request.form["email"]
        destination = request.form["destination"]
        interest = request.form["interest"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        # Store user in Firestore
        user_ref = db.collection("users").document(email)
        user_ref.set({
            "name": name,
            "age": age,
            "email": email,
            "destination": destination,
            "interest": interest,
            "travel_dates": {
                "start_date": start_date,
                "end_date": end_date
            }
        })

        return redirect(url_for("home"))
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
