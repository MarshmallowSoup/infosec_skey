from flask import Flask, request, jsonify, redirect, url_for, session
import requests
import logging
import json


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VERIFY_CREDENTIALS_URL = 'http://key_generator:5000/verify_credentials'

# Set of routes that do not require authentication
# Add more routes to this set as needed
PUBLIC_ROUTES = {'/'}

def is_authenticated():
    # Add your authentication logic here
    # For simplicity, assume user is authenticated if 'user_authenticated' is in the session
    return 'user_authenticated' in session

@app.before_request
def check_authentication():
    # Skip authentication check for public routes
    if request.endpoint != '/login':
        return

    # Check if the user is authenticated
    if not is_authenticated():
        # Redirect to the login page if not authenticated
        return redirect(url_for('login'))

@app.route('/')
def hello_world():
    return 'Hello, World! This is your Flask server.'


@app.route('/login', methods=['POST'])
def login():
    # Get the password from the request
    password = request.form.get('password')

    data = {
        "pass": password
    }
    headers = {
        "Content-Type": "application/json"
    }

    # Validate the password by making a request to the verification endpoint
    verification_response = requests.post(VERIFY_CREDENTIALS_URL, data=json.dumps(data), headers=headers)

    # Check if the verification was successful
    if verification_response.status_code == 200:
        return 'Login successful!'
    else:
        return 'Login failed. Invalid credentials.'
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)