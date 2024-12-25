from flask import jsonify, request
import re
import csv
import os

# In-memory waitlist database
waitlist = []

# File path for CSV (optional, for external storage in Vercel environment)
csv_file = "/mnt/data/waitlist.csv"

def handler(request):
    # Ensure the method is POST
    if request.method != "POST":
        return jsonify({"error": "Method not allowed"}), 405

    try:
        # Parse JSON data from the request
        data = request.json
        wallet = data.get("wallet")
        email = data.get("email")

        # Validation
        if not wallet or not re.match(r"^0\.0\.\d+$", wallet):
            return jsonify({"error": "Invalid wallet address format."}), 400
        if not email or not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            return jsonify({"error": "Invalid email address."}), 400

        # Add entry to the in-memory database
        waitlist.append({"wallet": wallet, "email": email})

        # Save to CSV file
        try:
            # Ensure CSV directory exists (especially in Vercel's ephemeral file system)
            os.makedirs(os.path.dirname(csv_file), exist_ok=True)

            with open(csv_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([wallet, email])
        except Exception as e:
            return jsonify({"error": f"Failed to write to CSV: {str(e)}"}), 500

        return jsonify({"message": "Successfully joined the waitlist!"}), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
