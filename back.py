from flask import Flask, request, jsonify, render_template, send_file
import re
import csv
import os

app = Flask(__name__)  # Initialize Flask app

# Simple in-memory database (replace with real DB later)
waitlist = []

# Utility function to validate wallet and email
def is_valid_wallet(wallet):
    return re.match(r'^0\.0\.\d+$', wallet)  # Example Hedera wallet format

def is_valid_email(email):
    return re.match(r'^[^@]+@[^@]+\.[^@]+$', email)

@app.route('/')
def home():
    return render_template('index.html')  # Serve the main page

@app.route('/join-waitlist', methods=['POST'])
def join_waitlist():
    data = request.json
    wallet = data.get('wallet')
    email = data.get('email')

    if not is_valid_wallet(wallet):
        return jsonify({'error': 'Invalid wallet address format.'}), 400
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email address.'}), 400

    waitlist.append({'wallet': wallet, 'email': email})
    return jsonify({'message': 'Successfully joined the waitlist!'})

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', waitlist=waitlist)

@app.route('/download-csv')
def download_csv():
    filename = "waitlist.csv"

    # Generate the CSV file
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Wallet Address', 'Email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in waitlist:
            writer.writerow({'Wallet Address': entry['wallet'], 'Email': entry['email']})

    # Serve the CSV file for download
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
