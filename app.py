from flask import Flask, render_template, request
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
        # Get form data from the user
        name = request.form["name"]  # Assuming you add a name field in the form
        email = request.form["email"]  # Assuming you add an email field in the form
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

        # Pass data to the travel buddy page
        return render_template("buddy.html", name=name, destination=destination, dates=travel_dates)

    return render_template("index.html")

@app.route("/buddy", methods=["GET", "POST"])
def travel_buddy():
    return render_template("buddy.html")

if __name__ == "__main__":
    app.run(debug=True)
