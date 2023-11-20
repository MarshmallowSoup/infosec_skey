from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
import hashlib
from classes.session import Session
from classes.user import User

app = Flask(__name__)
auth = HTTPBasicAuth()

user = User()

@auth.verify_password
def verify_password(username, password):

    return username == USERNAME and password == PASSWORD



@app.route('/save_key', methods=['POST'])
@auth.login_required
def save_key():
    global counter_docker

    # Generate a random key
    generated_key = 
    # Write the generated key to a file
    with open('generated_key.txt', 'a') as file:
        file.write(f"{counter_docker}: {generated_key}\n")

    return jsonify({'success': True, 'generated_key': generated_key}), 200, generated_key


counter_docker = 1  # Initialize the counter for the Docker container

@app.route('/authenticate', methods=['POST'])
def authenticate():
    global counter_docker

    data = request.get_json()
    received_key = data.get('key')
    received_counter = data.get('counter')
    received_one_time_password = data.get('one_time_password')

    # Verify received key
    expected_key = generate_one_time_password(secret_key_docker, counter_docker)[:6]
    if received_key == expected_key:
        # Authentication successful
        counter_docker += 1  # Increment the counter for the next authentication
        return jsonify({'success': True}), 200
    else:
        # Authentication failed
        return jsonify({'success': False}), 401

if __name__ == '__main__':
    app.run(port=5000)