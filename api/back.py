from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# Global variable for total signups (server-side storage)
total_signups = 10  # Starting value for progress bar

@app.route("/join-waitlist", methods=["POST"])
def join_waitlist():
    global total_signups
    data = request.json
    wallet = data.get("wallet")
    email = data.get("email")

    # Validate wallet and email
    if not re.match(r"^0\.0\.\d+$", wallet):
        return jsonify({"error": "Invalid wallet address"}), 400
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
        return jsonify({"error": "Invalid email address"}), 400

    # Increment total signups
    total_signups += 1

    return jsonify({
        "message": "Successfully joined the waitlist!",
        "totalSignups": total_signups
    })

if __name__ == "__main__":
    app.run(debug=True)
