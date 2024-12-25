from flask import jsonify, request
import re
import csv

# Simple in-memory database
waitlist = []

# File path for CSV (optional, for external storage)
csv_file = "/mnt/data/waitlist.csv"

def handler(request):
    if request.method != "POST":
        return jsonify({"error": "Method not allowed"}), 405

    data = request.json
    wallet = data.get("wallet")
    email = data.get("email")

    # Validation
    if not re.match(r"^0\.0\.\d+$", wallet):
        return jsonify({"error": "Invalid wallet address format."}), 400
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
        return jsonify({"error": "Invalid email address."}), 400

    # Save to in-memory database
    waitlist.append({"wallet": wallet, "email": email})

    # Optionally save to CSV
    with open(csv_file, "a") as f:
        writer = csv.writer(f)
        writer.writerow([wallet, email])

    return jsonify({"message": "Successfully joined the waitlist!"})
